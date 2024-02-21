from endi.resources import (
    main_group,
)
from endi.utils.sys_environment import package_version
from endi.utils.menu import (
    Menu,
    MenuItem,
)


class SupplierLayout:
    endi_version = package_version

    def __init__(self, context, request):
        self.context = context
        main_group.need()

    @property
    def docs_menu(self):
        DocsMenu.set_current(self.context)
        return DocsMenu


# Tabs headers with supplier-related documents
DocsMenu = Menu(name="supplier_docs_menu")


DocsMenu.add(
    MenuItem(
        name="running_orders",
        label="Commandes en cours",
        route_name="supplier_running_orders",
        icon="file-alt",
        anchor="#subview",
    )
)
DocsMenu.add(
    MenuItem(
        name="invoiced_orders",
        label="Commandes facturées",
        route_name="supplier_invoiced_orders",
        icon="euro-sign",
        anchor="#subview",
    )
)

DocsMenu.add(
    MenuItem(
        name="invoices",
        label="Factures",
        route_name="supplier_invoices",
        icon="file-invoice-euro",
        anchor="#subview",
    )
)

DocsMenu.add(
    MenuItem(
        name="expenselines",
        label="Notes de dépenses",
        route_name="supplier_expenselines",
        icon="file-alt",
        anchor="#subview",
    )
)


def includeme(config):
    config.add_layout(
        SupplierLayout, template="endi:templates/supplier/layout.mako", name="supplier"
    )
