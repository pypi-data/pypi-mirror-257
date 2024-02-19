from colanderalchemy import SQLAlchemySchemaNode

from endi.models.accounting.bookeeping import (
    CustomInvoiceBookEntryModule,
)


def get_admin_book_entry_schema():
    schema = SQLAlchemySchemaNode(
        CustomInvoiceBookEntryModule,
        excludes=("doctype", "custom"),
    )
    return schema
