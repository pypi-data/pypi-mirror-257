"""
Views related to payments edition
"""
import logging

from endi.models.supply import (
    SupplierInvoiceSupplierPayment,
)

from endi.utils.widgets import Link

from endi.forms import merge_session_with_post
from endi.forms.supply.supplier_invoice import (
    UserPaymentSchema,
    SupplierPaymentSchema,
)

from endi.views import (
    BaseView,
    TreeMixin,
)
from endi.views.supply.invoices.views import SupplierInvoiceEditView
from endi.views.supply.invoices.routes import ITEM_ROUTE as SUPPLIER_INVOICE_ROUTE

from .base import (
    BasePaymentEditView,
    BasePaymentDeleteView,
    get_delete_confirm_message,
    get_warning_message,
)

logger = logging.getLogger(__name__)


class SupplierInvoicePaymentView(BaseView, TreeMixin):
    route_name = "supplier_payment"

    @property
    def tree_url(self):
        return self.request.route_path(
            self.route_name,
            id=self.context.id,
        )

    @property
    def title(self):
        return "Paiement pour la facture fournisseur {0}".format(
            self.context.parent.official_number
        )

    def stream_actions(self):
        parent_url = self.request.route_path(
            SUPPLIER_INVOICE_ROUTE,
            id=self.context.parent.id,
        )
        if self.request.has_permission("edit.payment"):
            _query = dict(action="edit")
            if self.request.is_popup:
                _query["popup"] = "1"
            edit_url = self.request.route_path(
                self.route_name, id=self.context.id, _query=_query
            )

            yield Link(
                edit_url,
                label="Modifier",
                title="Modifier les informations du paiement",
                icon="pen",
                css="btn btn-primary",
            )
        if self.request.has_permission("delete.payment"):
            del_url = self.request.route_path(
                self.route_name,
                id=self.context.id,
                _query=dict(action="delete", come_from=parent_url),
            )
            confirm = get_delete_confirm_message(self.context, "décaissement", "ce")
            yield Link(
                del_url,
                label="Supprimer",
                title="Supprimer le paiement",
                icon="trash-alt",
                confirm=confirm,
                css="negative",
            )

    def get_export_button(self):
        if self.request.has_permission("admin_treasury"):
            if self.context.exported:
                label = "Forcer l'export des écritures de ce paiement"
            else:
                label = "Exporter les écritures de ce paiement"
            return Link(
                self.request.route_path(
                    "/export/treasury/supplier_payments/{id}",
                    id=self.context.id,
                    _query=dict(come_from=self.tree_url, force=True),
                ),
                label=label,
                title=label,
                icon="file-export",
                css="btn btn-primary",
            )

    def __call__(self):
        self.populate_navigation()
        return dict(
            title=self.title,
            actions=self.stream_actions(),
            export_button=self.get_export_button(),
            document_number=f"Facture fournisseur {self.context.parent.official_number}",
            money_flow_type="Ce décaissement",
        )


class SupplierPaymentEdit(BasePaymentEditView):
    route_name = "supplier_payment"

    def get_schema(self):
        payment = self.context
        if isinstance(payment, SupplierInvoiceSupplierPayment):
            schema = SupplierPaymentSchema()
        else:
            schema = UserPaymentSchema()
        return schema

    @property
    def warn_message(self):
        return get_warning_message(self.context, "décaissement", "ce")

    def get_default_redirect(self):
        return self.request.route_path("supplier_payment", id=self.context.id)

    def edit_payment(self, appstruct):
        invoice = self.context.supplier_invoice
        payment_obj = self.context
        # update the payment
        merge_session_with_post(payment_obj, appstruct)
        self.dbsession.merge(payment_obj)
        invoice.check_resulted()
        self.dbsession.merge(invoice)
        return payment_obj


class SupplierPaymentDeleteView(BasePaymentDeleteView):
    def delete_payment(self):
        invoice = self.context.supplier_invoice
        self.dbsession.delete(self.context)
        invoice.check_resulted()
        self.dbsession.merge(invoice)

    def parent_url(self, parent_id):
        return self.request.route_path(SUPPLIER_INVOICE_ROUTE, id=parent_id)


def includeme(config):
    config.add_tree_view(
        SupplierInvoicePaymentView,
        parent=SupplierInvoiceEditView,
        permission="view.payment",
        renderer="/payment.mako",
    )
    config.add_tree_view(
        SupplierPaymentEdit,
        parent=SupplierInvoicePaymentView,
        permission="edit.payment",
        request_param="action=edit",
        renderer="/base/formpage.mako",
    )
    config.add_view(
        SupplierPaymentDeleteView,
        route_name="supplier_payment",
        permission="delete.payment",
        request_param="action=delete",
    )
