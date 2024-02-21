import colander
from colanderalchemy import SQLAlchemySchemaNode
from endi.models.status import StatusLogEntry
from endi.utils.html import strip_html_tags
from endi.forms import force_iterable_preparer


def get_status_log_schema():
    schema = SQLAlchemySchemaNode(
        StatusLogEntry, includes=("label", "comment", "visibility", "pinned")
    )
    schema["visibility"].validator = colander.OneOf(("public", "private", "management"))
    schema["label"].missing = colander.required
    schema["comment"].preparer = strip_html_tags
    schema.add(
        colander.SchemaNode(
            colander.Boolean(),
            missing=False,
            title="Notifier les utilisateurs ?",
            name="notify",
        )
    )
    schema.add(
        colander.SchemaNode(
            colander.Set(),
            missing=False,
            title="Utilisateurs à notifier",
            name="notification_recipients",
            preparer=force_iterable_preparer,
        )
    )
    return schema
