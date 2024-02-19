"""
This module contains

    - Action managers handling status changes for Sale documents
    - Callbacks fired when the documents status are changed (official number,
    remote internal document generation ...)
"""
import logging

from endi.utils.datetimes import utcnow
from endi.utils.status_rendering import SIGNED_STATUS_ICON

from endi.models.config import Config
from endi.models.action_manager import (
    Action,
    ActionManager,
    get_validation_state_manager,
)
from .services import (
    InvoiceNumberService,
    InternalInvoiceNumberService,
)

logger = logging.getLogger(__name__)

CELERY_DELAY = 3


def _set_invoice_number(request, task, **kw):
    """
    Set a official number on invoices (or cancelinvoices)

    :param obj request: The current pyramid request
    :param obj task: The current context
    """
    template = Config.get_value("invoice_number_template", None)
    assert template is not None, "invoice_number_template setting should be set"

    if task.official_number is None:
        InvoiceNumberService.assign_number(
            request,
            task,
            template,
        )
    return task


def _set_internalinvoice_number(request, task, **kw):
    """
    Set a official number on internalinvoices (or cancelinvoices)

    :param obj request: The current pyramid request
    :param obj task: The current context
    """
    template = Config.get_value("internalinvoice_number_template", None)
    assert template is not None, "internalinvoice_number_template setting should be set"

    if task.official_number is None:
        InternalInvoiceNumberService.assign_number(
            request,
            task,
            template,
        )
    return task


def _set_invoice_financial_year(request, task, **kw):
    """
    Set financial year on invoices (or cancelinvoices)
    based on task date

    :param obj request: The current pyramid request
    :param obj task: The current context
    """
    task.financial_year = task.date.year
    logger.info(
        "Setting financial year for invoice {} to {} (invoice's date is {})".format(
            task.id, task.financial_year, task.date
        )
    )
    request.dbsession.merge(task)
    return task


def estimation_valid_callback(request, task, **kw):
    """
    Estimation validation callback

    :param obj request: The current pyramid request
    :param obj task: The current context
    """
    return task


def internalestimation_valid_callback(request, task, **kw):
    """
    InternalEstimation validation callback

    :param obj request: The current pyramid request
    :param obj task: The current InternalEstimation
    """
    import endi
    from endi_celery.tasks.utils import check_alive
    from endi_celery.tasks.tasks import (
        async_internalestimation_valid_callback,
    )

    task = estimation_valid_callback(request, task, **kw)
    logger.info("    + InternalEstimation validation callback")
    logger.info("    + Document {}".format(task))

    if not endi._called_from_test:
        service_ok, msg = check_alive()
        if not service_ok:
            logger.error("Celery is not available")
        else:
            request.dbsession.merge(task)
            request.dbsession.flush()
            async_internalestimation_valid_callback.apply_async(
                args=[task.id], eta=utcnow(delay=CELERY_DELAY)
            )
            logger.info("A Celery Task has been delayed")
    return task


def invoice_valid_callback(request, task, **kw):
    """
    Invoice validation callback

    :param obj request: The current pyramid request
    :param obj task: The current context
    """
    import endi
    from endi_celery.tasks.utils import check_alive
    from endi_celery.tasks.tasks import scheduled_render_pdf_task

    _set_invoice_number(request, task, **kw)
    _set_invoice_financial_year(request, task, **kw)

    if not endi._called_from_test:
        service_ok, msg = check_alive()
        if not service_ok:
            logger.error("Celery is not available")
        else:
            request.dbsession.merge(task)
            request.dbsession.flush()
            scheduled_render_pdf_task.apply_async(
                args=[task.id], eta=utcnow(delay=CELERY_DELAY)
            )
            logger.info("A Celery Task has been delayed")
    return task


def internalinvoice_valid_callback(request, task, **kw):
    """
    Invoice validation callback

    :param obj request: The current pyramid request
    :param obj task: The current context
    """
    import endi
    from endi_celery.tasks.utils import check_alive
    from endi_celery.tasks.tasks import (
        async_internalinvoice_valid_callback,
    )

    _set_internalinvoice_number(request, task, **kw)
    _set_invoice_financial_year(request, task, **kw)
    logger.info("    + InternalInvoice validation callback")
    logger.info("    + Document {}".format(task))

    if not endi._called_from_test:
        service_ok, msg = check_alive()
        if not service_ok:
            logger.error("Celery is not available")
        else:
            # Fix #
            async_internalinvoice_valid_callback.apply_async(
                args=[task.id], eta=utcnow(delay=CELERY_DELAY)
            )
            logger.info("A Celery Task has been delayed")

    return task


def get_internalestimation_state_manager() -> ActionManager:
    """
    Renvoie un state manager pour les devis internes
    """
    manager = get_validation_state_manager(
        "estimation",
        callbacks=dict(valid=internalestimation_valid_callback),
    )
    for item in manager.items:
        item.options["help_text"] = (
            "À la validation du devis, celui-ci sera automatiquement transmis "
            "à votre client"
        )
    return manager


def get_internalinvoice_state_manager() -> ActionManager:
    """
    Construit le state manager pour les factures internes
    """
    manager = get_validation_state_manager(
        "invoice",
        callbacks=dict(valid=internalinvoice_valid_callback),
    )
    for item in manager.items:
        item.options["help_text"] = (
            "À la validation de la facture, celle-ci sera automatiquement "
            "transmise à votre client"
        )
    return manager


def get_internalcancelinvoice_state_manager() -> ActionManager:
    """
    Construit le state manager pour les avoirs internes
    """
    manager = get_validation_state_manager(
        "cancelinvoice",
        callbacks=dict(valid=internalinvoice_valid_callback),
    )
    for item in manager.items:
        item.options["help_text"] = (
            "À la validation de l'avoir, celui-ci sera automatiquement "
            "transmis à votre client"
        )
    return manager


DEFAULT_ACTION_MANAGER = {
    "estimation": get_validation_state_manager(
        "estimation",
        callbacks=dict(valid=estimation_valid_callback),
    ),
    "internalestimation": get_internalestimation_state_manager(),
    "invoice": get_validation_state_manager(
        "invoice",
        callbacks=dict(valid=invoice_valid_callback),
    ),
    "internalinvoice": get_internalinvoice_state_manager(),
    "internalcancelinvoice": get_internalcancelinvoice_state_manager(),
    "cancelinvoice": get_validation_state_manager(
        "cancelinvoice",
        callbacks=dict(valid=invoice_valid_callback),
    ),
}


def get_signed_status_actions():
    """
    Return actions available for setting the signed_status attribute on
    Estimation objects
    """
    manager = ActionManager()
    for status, label, title, css in (
        ("waiting", "En attente de réponse", "En attente de réponse du client", "btn"),
        (
            "sent",
            "A été envoyé au client",
            "A bien été envoyé au client",
            "btn",
        ),
        (
            "aborted",
            "Sans suite",
            "Marquer sans suite",
            "btn negative",
        ),
        (
            "signed",
            "Signé par le client",
            "Indiquer que le client a passé commande",
            "btn btn-primary",
        ),
    ):
        action = Action(
            status,
            "set_signed_status.estimation",
            status_attr="signed_status",
            icon=SIGNED_STATUS_ICON[status],
            label=label,
            title=title,
            css=css,
        )
        manager.add(action)
    return manager


SIGNED_ACTION_MANAGER = get_signed_status_actions()
