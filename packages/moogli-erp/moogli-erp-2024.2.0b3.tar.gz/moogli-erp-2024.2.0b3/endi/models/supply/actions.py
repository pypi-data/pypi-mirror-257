import logging
from endi_base.models.base import DBSESSION

from endi.models.action_manager import get_validation_state_manager
from endi.models.config import Config

from .services.supplierinvoice_official_number import (
    SupplierInvoiceNumberService,
    InternalSupplierInvoiceNumberService,
)

logger = logging.getLogger(__name__)


def internalsupplier_order_valid_callback(request, supplier_order, *args, **kwargs):
    """
    Callback launched after an internal supplier order is validated
    send an email to the supplier
    """
    supplier_order.source_estimation.set_signed_status("signed", request)
    from endi.utils.notification.internal_supply import (
        send_supplier_order_validated_mail,
    )

    send_supplier_order_validated_mail(request, supplier_order)
    DBSESSION().merge(supplier_order.source_estimation)
    DBSESSION().flush()


def _set_supplier_invoice_official_number(request, supplier_invoice, *args, **kwargs):
    """
    Callback for when sheet turns into valid status
    """
    template = Config.get_value("supplierinvoice_number_template", None)

    assert template is not None, "supplierinvoice_number_template setting should be set"

    if supplier_invoice.official_number is None:
        SupplierInvoiceNumberService.assign_number(request, supplier_invoice, template)


def _set_internalsupplier_invoice_official_number(
    request, supplier_invoice, *args, **kwargs
):
    """
    Callback for when sheet turns into valid status
    """
    template = Config.get_value("internalsupplierinvoice_number_template", None)

    assert (
        template is not None
    ), "internalsupplierinvoice_number_template setting should be set"

    if supplier_invoice.official_number is None:
        InternalSupplierInvoiceNumberService.assign_number(
            request, supplier_invoice, template
        )


def _set_negative_internalsupplier_invoice_resulted(
    request, supplier_invoice, *args, **kwargs
):
    """
    Set the negative supplier invoices as resulted
    """
    if supplier_invoice.total <= 0:
        logger.info(
            f"Setting the negative supplier invoice {supplier_invoice.official_number} as resulted"
        )
        supplier_invoice.worker_paid_status = (
            supplier_invoice.supplier_paid_status
        ) = supplier_invoice.paid_status = "resulted"


def supplier_invoice_valid_callback(request, supplier_invoice, *args, **kwargs):
    """Called when a supplier invoice is validated"""
    _set_supplier_invoice_official_number(request, supplier_invoice, *args, **kwargs)


def internalsupplier_invoice_valid_callback(request, supplier_invoice, *args, **kwargs):
    _set_internalsupplier_invoice_official_number(
        request, supplier_invoice, *args, **kwargs
    )
    _set_negative_internalsupplier_invoice_resulted(
        request, supplier_invoice, *args, **kwargs
    )


def get_internal_supplier_order_state_manager():
    manager = get_validation_state_manager(
        "supplier_order",
        callbacks=dict(valid=internalsupplier_order_valid_callback),
    )
    for item in manager.items:
        item.options["help_text"] = (
            "La validation de cette commande vaut acceptation du devis "
            "associé. Un e-mail de confirmation sera envoyé au fournisseur."
        )
    return manager


ACTION_MANAGER = {
    "supplier_order": get_validation_state_manager(
        "supplier_order",
    ),
    "internalsupplier_order": get_internal_supplier_order_state_manager(),
    "supplier_invoice": get_validation_state_manager(
        "supplier_invoice",
        callbacks=dict(valid=supplier_invoice_valid_callback),
    ),
    "internalsupplier_invoice": get_validation_state_manager(
        "supplier_invoice",
        callbacks=dict(valid=internalsupplier_invoice_valid_callback),
    ),
}
