import colander

from endi.forms import files


@colander.deferred
def deferred_upload_digital_signature_widget(node, kw):
    request = kw["request"]
    tmpstore = files.SessionDBFileUploadTempStore(request)
    return files.CustomFileUploadWidget(
        tmpstore,
        show_delete_control=True,
    )


class DigitalSignaturesSchema(colander.MappingSchema):
    """
    Digital signatures form schema
    """

    cae_manager_digital_signature = files.ImageNode(
        widget=deferred_upload_digital_signature_widget,
        title="Signature du gérant",
        missing=colander.drop,
        description="Charger un fichier de type image *.png *.jpeg \
 *.jpg…",
    )
