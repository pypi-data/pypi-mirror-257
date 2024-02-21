import colander
import deform
import logging
import io
from cgi import FieldStorage

from sqlalchemy.orm import load_only

from pyramid_deform import SessionFileUploadTempStore

from endi.utils.datetimes import format_date
from endi.models.project.project import Project
from endi.models.node import Node
from endi.models.task import Task
from endi.models.files import (
    File,
    FileType,
)
from endi.models.career_path import CareerPath
from endi.models.project.business import Business
from endi.models.project.file_types import BusinessTypeFileType

from endi.compute.math_utils import convert_to_int
from endi.utils.strings import human_readable_filesize
from endi import forms
from endi.forms.validators import validate_image_mime

logger = logging.getLogger(__name__)


class CustomFileUploadWidget(deform.widget.FileUploadWidget):
    """
    File upload widget that handles:
      - filters when deserializing
      - file deletion (via a checkbox)

        filters

            An optionnal list (or simple filter) that will be fired on the datas
            (for example in order to reduce image sizes)

       show_delete_control (default :False)

           Display a checkbox to allow deleting the file from form ("clearing"
           file field).

    """

    template = "fileupload.pt"

    def __init__(self, *args, **kwargs):
        self.show_delete_control = kwargs.pop("show_delete_control", False)
        super(CustomFileUploadWidget, self).__init__(*args, **kwargs)

    @property
    def _pstruct_schema(self):
        # Overrides a private attribute form FileUploadWidget
        pstruct_schema = deform.widget.FileUploadWidget._pstruct_schema.clone()
        delete_field_node = colander.SchemaNode(
            colander.String(allow_empty=True),
            name="delete",
            missing=None,
        )
        pstruct_schema.add(delete_field_node)
        return pstruct_schema

    def deserialize(self, field, pstruct):
        data = deform.widget.FileUploadWidget.deserialize(self, field, pstruct)
        # We're returning the datas in the appstruct dict, we format the file if
        # needed
        uid = self._pstruct_schema.deserialize(pstruct).get("uid")

        if pstruct.get("delete") and uid and self.show_delete_control:
            data = {"delete": True}
            return data

        if isinstance(data, dict) and "fp" in data:
            data["fp"].seek(0)
            data["size"] = len(data["fp"].read())
            data["fp"].seek(0)
            if hasattr(self.tmpstore, "filter_data"):
                data["fp"] = self.tmpstore.filter_data(data["fp"])

        return data


class SessionDBFileUploadTempStore(SessionFileUploadTempStore):
    """
    A session based File upload temp store

    Is necessary for deform's upload widget to be able to keep the datas when
    there are errors on form validation

        request

            The current request object
    """

    def __init__(self, request, filters=None):
        SessionFileUploadTempStore.__init__(self, request)

        if filters and not hasattr(filters, "__iter__"):
            filters = [filters]
        self.filters = filters or []

    def filter_data(self, fbuf):
        """
        Pass file datas through filters
        """
        if self.filters:
            # Use an intermediary buffer
            fdata = io.BytesIO(fbuf.read())
            try:
                for filter_ in self.filters:
                    fdata = filter_(fdata)
                    fdata.seek(0)
            except IOError:  # Raised when it's not an image file
                fbuf.seek(0)
                fdata = fbuf
            return fdata
        else:
            return fbuf


class FileNode(colander.SchemaNode):
    """
    A main file upload node class

    Use this node in a custom schema.
    Then, on submit :

        >>> class Schema(colander.Schema):
                filenodename = FileNode(title="Fichier")

        # You need to pass the name before merging the appstruct
        >>> f_object = File(
            parent=parent_obj, name=appstruct['filenodename']['name']
        )
        >>> merge_session_with_post(f_object, appstruct)
        >>> dbsession.add(f_object)

    """

    schema_type = deform.FileData
    title = "Choix du fichier"
    default_max_size = 1048576
    _max_allowed_file_size = None

    def validator(self, node, value):
        """
        Build a file size validator
        """
        request = self.bindings["request"]
        max_filesize = self._get_max_allowed_file_size(request)
        if value is not None:
            if isinstance(value, FieldStorage):
                file_obj = value.fp
            else:
                file_obj = value.get("fp")
            if file_obj:
                file_obj.seek(0)
                size = len(file_obj.read())
                file_obj.seek(0)
                if size > max_filesize:
                    message = "Ce fichier est trop volumineux"
                    raise colander.Invalid(node, message)

    def _get_max_allowed_file_size(self, request) -> int:
        """
        Return the max allowed filesize configured in de MooGLi
        """
        if self._max_allowed_file_size is None:
            settings = request.registry.settings
            size = settings.get("endi.maxfilesize", self.default_max_size)
            self._max_allowed_file_size = convert_to_int(size, self.default_max_size)

        return self._max_allowed_file_size

    @colander.deferred
    def widget(self, kw):
        request = kw["request"]
        tmpstore = SessionDBFileUploadTempStore(request)
        return CustomFileUploadWidget(tmpstore)

    def after_bind(self, node, kw):
        size = self._get_max_allowed_file_size(kw["request"])
        if not getattr(self, "description", ""):
            self.description = ""

        self.description += " Taille maximale : {0}".format(
            human_readable_filesize(size)
        )


class ImageNode(FileNode):
    def validator(self, node, value):
        FileNode.validator(self, node, value)
        validate_image_mime(node, value)

    def after_bind(self, node, kw):
        if not getattr(self, "description", ""):
            self.description = ""

        self.description += "Charger un fichier de type image (*.png, *.jpeg ou *.jpg)"


class FileTypeNode(colander.SchemaNode):
    title = "Type de document"
    schema_type = colander.Int

    def __init__(self, *args, **kwargs):
        colander.SchemaNode.__init__(self, *args, **kwargs)
        self.types = []

    @colander.deferred
    def widget(self, kw):
        request = kw["request"]
        context = request.context
        available_types = self._collect_available_types(request, context)
        if available_types:
            choices = [(t.id, t.label) for t in available_types]
            choices.insert(0, ("", ""))
            widget = deform.widget.SelectWidget(values=choices)
        else:
            widget = deform.widget.HiddenWidget()
        return widget

    def _collect_available_types(self, request, context):
        """
        Collect file types that may be loaded for the given context

        :param obj context: The current object we're attaching a file to
        :returns: A list of FileType instances
        """
        result = []
        if isinstance(context, File):
            context = context.parent

        if isinstance(context, Task) or isinstance(context, Business):
            business_type_id = context.business_type_id

            result = BusinessTypeFileType.get_file_type_options(
                business_type_id, context.type_
            )
        elif isinstance(context, Project):
            result = []
            for business_type in context.get_all_business_types(request):
                result.extend(
                    BusinessTypeFileType.get_file_type_options(
                        business_type.id, requirement_type="project_mandatory"
                    )
                )
        else:
            result = (
                FileType.query()
                .options(load_only("id", "label"))
                .order_by(FileType.label.asc())
                .all()
            )
        return result

    def after_bind(self, node, kw):
        get_params = kw["request"].GET
        if "file_type_id" in get_params:
            self.default = int(get_params["file_type_id"])


@colander.deferred
def deferred_parent_id_validator(node, kw):
    request = kw["request"]

    def validate_node(node, value):
        node_object = request.dbsession.query(Node).get(value)
        if node_object is None:
            raise colander.Invalid(node, "Wrong parent_id")
        if not request.has_permission(
            "edit.file", node_object
        ) and not request.has_permission("add.file", node_object):
            raise colander.Invalid(node, "You don't have permission to edit this node")

    return validate_node


@colander.deferred
def deferred_parent_id_missing(node, kw):
    request = kw["request"]
    context = request.context
    if isinstance(context, (Node, File)):
        return colander.drop
    else:
        # Cas où on ajoute un fichier directement sur /api/v1/files
        return colander.required


class FileUploadSchema(colander.Schema):
    come_from = forms.come_from_node()
    popup = forms.popup_node()

    upload = FileNode()

    description = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(
            min=5,
            max=100,
            min_err="La description ne doit pas être inférieure à 5 caractères",
            max_err="La description ne doit pas être supérieure à 100 caractères",
        ),
    )
    file_type_id = FileTypeNode(missing=colander.drop)
    indicator_id = colander.SchemaNode(
        colander.Integer(),
        missing=colander.drop,
        widget=deform.widget.HiddenWidget(),
    )
    parent_id = colander.SchemaNode(
        colander.Integer(),
        missing=deferred_parent_id_missing,
        widget=deform.widget.HiddenWidget(),
        validator=deferred_parent_id_validator,
    )


def get_template_upload_schema():
    """
    Return the form schema for template upload
    """

    def add_description(node, kw):
        node["upload"].description += " Le fichier doit être au format ODT"
        del node["file_type_id"]
        del node["parent_id"]
        del node["indicator_id"]

    schema = FileUploadSchema(after_bind=add_description)

    return schema


def get_businesstype_filetype_template_upload_schema():
    """
    Return the form schema for business type / file type template upload
    """

    def customize_schema(node, kw):
        node["upload"].description += " Le fichier doit être au format ODT"
        node["business_type_id"] = colander.SchemaNode(
            colander.Integer(),
            widget=deform.widget.HiddenWidget(),
        )
        node["file_type_id"] = colander.SchemaNode(
            colander.Integer(),
            widget=deform.widget.HiddenWidget(),
        )
        del node["parent_id"]

    schema = FileUploadSchema(after_bind=customize_schema)
    return schema


class UserDatasFileUploadSchema(FileUploadSchema):
    """
    Return the specific form schema for userdata's file upload
    """

    # TODO : convertir ces méthodes en statichmethod ou les sortir d'ici
    # cf le message du type checker
    def filter_by_userdata(node, kw):
        if isinstance(kw["request"].context, File):
            return CareerPath.userdatas_id == kw["request"].context.parent.id
        else:
            return CareerPath.userdatas_id == kw["request"].context.id

    def get_career_path_label(node):
        """
        génère un label pour l'étape de parcours

        :param obj node: L'étape de parcours
        """

        label = "{}".format(format_date(node.start_date))
        if node.career_stage is not None:
            label += " : {}".format(node.career_stage.name)

        if node.cae_situation is not None:
            label += " ({})".format(node.cae_situation.label)
        return label

    career_path_id = colander.SchemaNode(
        colander.Integer(),
        title="Attacher à une étape du parcours de l'entrepreneur",
        widget=forms.get_deferred_model_select(
            CareerPath,
            multi=False,
            mandatory=False,
            keys=("id", get_career_path_label),
            filters=[filter_by_userdata],
            empty_filter_msg="Non",
        ),
        missing=colander.drop,
    )


def get_file_upload_schema():
    schema = FileUploadSchema()
    return schema


def get_deferred_filtered_image_upload_widget(filters: list):
    """Build a deferrred returning a file upload widget filtering the incoming images

    >>> from endi.utils.image import ImageResizer, ImageRatio
    >>> filters = [ ImageRatio(4,1), ImageResizer(400, 100),]
    >>> class MySchema(colander.Schema):
    ...     image = ImageNode(
    ...         widget=get_deferred_filtered_image_upload_widget(filters)
    ...     )

    """

    @colander.deferred
    def deferred_upload_widget(node, kw):
        request = kw["request"]
        tmpstore = SessionDBFileUploadTempStore(
            request,
            filters=filters,
        )
        return CustomFileUploadWidget(
            tmpstore,
            show_delete_control=True,
        )

    return deferred_upload_widget
