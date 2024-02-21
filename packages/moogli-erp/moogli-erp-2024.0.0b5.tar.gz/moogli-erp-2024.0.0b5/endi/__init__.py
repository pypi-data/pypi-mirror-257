"""
Main file for our pyramid application
"""
# flake8: noqa: E402
import logging
import locale
import pkg_resources

from endi.utils.sys_environment import (
    collect_envvars_as_settings,
    package_name,  # Imported here for easy import in the app
    package_version,
)


locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")
locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")

from sqlalchemy import engine_from_config
from pyramid.config import Configurator
from pyramid_beaker import set_cache_regions_from_settings
from endi.utils.session import get_session_factory
from endi.utils.filedepot import (
    configure_filedepot,
)
from endi.utils.renderer import customize_renderers
from endi.utils.rest import add_rest_service
from endi.resources import lib_endi as fanstatic_endi_library
from endi_base.models.initialize import (
    configure_warnings,
    initialize_sql,
)


logger = logging.getLogger(__name__)
_called_from_test = False


ENDI_MANDATORY_MODULES = (
    "endi.views.auth",
    "endi.views.business",
    "endi.views.company",
    "endi.views.third_party.customer",
    "endi.views.estimations",
    "endi.views.expenses",
    "endi.views.files",
    "endi.views.indicators",
    "endi.views.invoices",
    "endi.views.job",
    "endi.views.manage",
    "endi.views.payment",
    "endi.views.sale_product",
    "endi.views.project",
    "endi.views.index",
    "endi.views.export.routes",
    "endi.views.export.invoice",
    "endi.views.export.expense",
    "endi.views.export.payment",
    "endi.views.export.expense_payment",
    "endi.views.static",
    "endi.views.user",
    "endi.views.rest_consts",
    "endi.views.release_notes",
    "endi.views.notification",
)

ENDI_OTHER_MODULES = (
    "endi.views.accompagnement",
    "endi.views.accounting",
    "endi.views.commercial",
    "endi.views.competence",
    "endi.views.csv_import",
    "endi.views.holiday",
    "endi.views.price_study",
    "endi.views.progress_invoicing",
    "endi.views.export.bpf",
    "endi.views.export.supplier_invoice",
    "endi.views.export.supplier_payment",
    "endi.views.internal_invoicing",
    "endi.views.management",
    "endi.views.statistics",
    "endi.views.dataqueries",
    "endi.views.supply.orders",
    "endi.views.supply.invoices",
    "endi.views.third_party.supplier",
    "endi.views.training",
    "endi.views.treasury_files",
    "endi.views.userdatas",
    "endi.views.validation",
    "endi.views.workshops",
    "endi.views.custom_documentation",
)

ENDI_LAYOUTS_MODULES = (
    "endi.default_layouts",
    "endi.views.user.layout",
)

ENDI_PANELS_MODULES = (
    "endi.panels.activity",
    "endi.panels.company_index",
    "endi.panels.files",
    "endi.panels.form",
    "endi.panels.indicators",
    "endi.panels.manage",
    "endi.panels.menu",
    "endi.panels.navigation",
    "endi.panels.project",
    "endi.panels.sidebar",
    "endi.panels.supply",
    "endi.panels.third_party",
    "endi.panels.tabs",
    "endi.panels.task",
    "endi.panels.widgets",
    "endi.panels.workshop",
)

ENDI_EVENT_MODULES = (
    "endi.events.model_events",
    "endi.events.status_changed",
    "endi.events.files",
    "endi.events.indicators",
    "endi.events.business",
)
ENDI_REQUEST_SUBSCRIBERS = (
    "endi.subscribers.new_request",
    "endi.subscribers.before_render",
)

ENDI_SERVICE_FACTORIES = (
    (
        "services.treasury_invoice_producer",
        "endi.compute.sage.InvoiceExportProducer",
        "endi.interfaces.ITreasuryProducer",
        "endi.models.task.Invoice",
    ),
    (
        "services.treasury_invoice_producer",
        "endi.compute.sage.InvoiceExportProducer",
        "endi.interfaces.ITreasuryProducer",
        "endi.models.task.CancelInvoice",
    ),
    (
        "services.treasury_internalinvoice_producer",
        "endi.compute.sage.InternalInvoiceExportProducer",
        "endi.interfaces.ITreasuryProducer",
        "endi.models.task.InternalInvoice",
    ),
    (
        "services.treasury_internalinvoice_producer",
        "endi.compute.sage.InternalInvoiceExportProducer",
        "endi.interfaces.ITreasuryProducer",
        "endi.models.task.InternalCancelInvoice",
    ),
    (
        "services.treasury_invoice_writer",
        "endi.export.sage.SageInvoiceCsvWriter",
        "endi.interfaces.ITreasuryInvoiceWriter",
        None,
    ),
    (
        "services.treasury_payment_producer",
        "endi.compute.sage.PaymentExportProducer",
        "endi.interfaces.ITreasuryProducer",
        "endi.models.task.Payment",
    ),
    (
        "services.treasury_internalpayment_producer",
        "endi.compute.sage.InternalPaymentExportProducer",
        "endi.interfaces.ITreasuryProducer",
        "endi.models.task.InternalPayment",
    ),
    (
        "services.treasury_payment_writer",
        "endi.export.sage.SagePaymentCsvWriter",
        "endi.interfaces.ITreasuryPaymentWriter",
        None,
    ),
    (
        "services.treasury_expense_producer",
        "endi.compute.sage.ExpenseExportProducer",
        "endi.interfaces.ITreasuryProducer",
        "endi.models.expense.sheet.ExpenseSheet",
    ),
    (
        "services.treasury_expense_writer",
        "endi.export.sage.SageExpenseCsvWriter",
        "endi.interfaces.ITreasuryExpenseWriter",
        None,
    ),
    (
        "services.treasury_expense_payment_producer",
        "endi.compute.sage.ExpensePaymentExportProducer",
        "endi.interfaces.ITreasuryProducer",
        "endi.models.expense.payment.ExpensePayment",
    ),
    (
        "services.treasury_expense_payment_writer",
        "endi.export.sage.SageExpensePaymentCsvWriter",
        "endi.interfaces.ITreasuryExpensePaymentWriter",
        None,
    ),
    (
        "services.treasury_supplier_invoice_producer",
        "endi.compute.sage.SupplierInvoiceExportProducer",
        "endi.interfaces.ITreasuryProducer",
        "endi.models.supply.supplier_invoice.SupplierInvoice",
    ),
    (
        "services.treasury_internalsupplier_invoice_producer",
        "endi.compute.sage.InternalSupplierInvoiceExportProducer",
        "endi.interfaces.ITreasuryProducer",
        "endi.models.supply.internalsupplier_invoice.InternalSupplierInvoice",
    ),
    (
        "services.treasury_supplier_invoice_writer",
        "endi.export.sage.SageSupplierInvoiceCsvWriter",
        "endi.interfaces.ITreasurySupplierInvoiceWriter",
        None,
    ),
    (
        "services.treasury_supplier_payment_producer",
        "endi.compute.sage.SupplierPaymentExportProducer",
        "endi.interfaces.ITreasuryProducer",
        "endi.models.supply.SupplierInvoiceSupplierPayment",
    ),
    (
        "services.treasury_supplier_payment_user_producer",
        "endi.compute.sage.SupplierUserPaymentExportProducer",
        "endi.interfaces.ITreasuryProducer",
        "endi.models.supply.SupplierInvoiceUserPayment",
    ),
    (
        "services.treasury_internalsupplier_payment_producer",
        "endi.compute.sage.InternalSupplierPaymentExportProducer",
        "endi.interfaces.ITreasuryProducer",
        "endi.models.supply.InternalSupplierInvoiceSupplierPayment",
    ),
    (
        "services.treasury_supplier_payment_writer",
        "endi.export.sage.SageSupplierPaymentCsvWriter",
        "endi.interfaces.ITreasurySupplierPaymentWriter",
        None,
    ),
    (
        "services.task_pdf_rendering_service",
        "endi.views.task.pdf_rendering_service.TaskPdfFromHtmlService",
        "endi.interfaces.ITaskPdfRenderingService",
        "endi.models.task.Task",
    ),
    (
        "services.task_pdf_storage_service",
        "endi.views.task.pdf_storage_service.PdfFileDepotStorageService",
        "endi.interfaces.ITaskPdfStorageService",
        "endi.models.task.Task",
    ),
    (
        "services.payment_record_service",
        "endi_payment.public.PaymentService",
        "endi.interfaces.IPaymentRecordService",
        (
            "endi.models.task.Invoice",
            "endi.models.task.Payment",
        ),
    ),
    (
        "services.internalpayment_record_service",
        "endi.models.task.services.InternalPaymentRecordService",
        "endi.interfaces.IPaymentRecordService",
        (
            "endi.models.task.InternalInvoice",
            "endi.models.task.InternalPayment",
        ),
    ),
    (
        "services.waiting_documents_service",
        "endi.models.status.ValidationStatusHolderService",
        "endi.interfaces.IValidationStatusHolderService",
        None,
    ),
    (
        "services.payment_groupper_service",
        "endi.compute.sage.payment.PaymentExportGroupper",
        "endi.interfaces.ITreasuryGroupper",
        "endi.models.task.payment.BaseTaskPayment",
    ),
    (
        "services.payment_groupper_service",
        "endi.compute.sage.invoice.InvoiceExportGroupper",
        "endi.interfaces.ITreasuryGroupper",
        "endi.models.task.invoice.Invoice",
    ),
)
# (key, callable, interface, context, params)
# key : The setting key
# callable : The callable returning the object (global to the wsgi context)
# interface : The interface it implements
# context : The context it should be used for
# params : tuple of params passed to the callable as *params
ENDI_SERVICES = (
    # Statut de validation des Task
    (
        "services.validation_state_manager.invoice",
        "endi.controllers.state_managers.validation.get_default_validation_state_manager",
        "endi.interfaces.IValidationStateManager",
        "endi.models.task.invoice.Invoice",
        ("invoice",),
    ),
    (
        "services.validation_state_manager.cancelinvoice",
        "endi.controllers.state_managers.validation.get_default_validation_state_manager",
        "endi.interfaces.IValidationStateManager",
        "endi.models.task.invoice.CancelInvoice",
        ("cancelinvoice",),
    ),
    (
        "services.validation_state_manager.estimation",
        "endi.controllers.state_managers.validation.get_default_validation_state_manager",
        "endi.interfaces.IValidationStateManager",
        "endi.models.task.estimation.Estimation",
        ("estimation",),
    ),
    (
        "services.validation_state_manager.internalinvoice",
        "endi.controllers.state_managers.validation.get_default_validation_state_manager",
        "endi.interfaces.IValidationStateManager",
        "endi.models.task.internalinvoice.InternalInvoice",
        ("internalinvoice",),
    ),
    (
        "services.validation_state_manager.internalcancelinvoice",
        "endi.controllers.state_managers.validation.get_default_validation_state_manager",
        "endi.interfaces.IValidationStateManager",
        "endi.models.task.internalinvoice.InternalCancelInvoice",
        ("internalcancelinvoice",),
    ),
    (
        "services.validation_state_manager.internalestimation",
        "endi.controllers.state_managers.validation.get_default_validation_state_manager",
        "endi.interfaces.IValidationStateManager",
        "endi.models.task.internalestimation.InternalEstimation",
        ("internalestimation",),
    ),
    # Status de validation des NDDs
    (
        "services.validation_state_manager.expense",
        "endi.controllers.state_managers.validation.get_default_validation_state_manager",
        "endi.interfaces.IValidationStateManager",
        "endi.models.expense.sheet.ExpenseSheet",
        ("expense",),
    ),
    # Statut de validation des factures/avoirs fournisseurs
    (
        "services.validation_state_manager.supplier_order",
        "endi.controllers.state_managers.validation.get_default_validation_state_manager",
        "endi.interfaces.IValidationStateManager",
        "endi.models.supply.supplier_order.SupplierOrder",
        ("supplier_order",),
    ),
    (
        "services.validation_state_manager.supplier_invoice",
        "endi.controllers.state_managers.validation.get_default_validation_state_manager",
        "endi.interfaces.IValidationStateManager",
        "endi.models.supply.supplier_invoice.SupplierInvoice",
        ("supplier_invoice",),
    ),
    (
        "services.validation_state_manager.internalsupplier_order",
        "endi.controllers.state_managers.validation.get_default_validation_state_manager",
        "endi.interfaces.IValidationStateManager",
        "endi.models.supply.internalsupplier_order.InternalSupplierOrder",
        ("internalsupplier_order",),
    ),
    (
        "services.validation_state_manager.internalsupplier_invoice",
        "endi.controllers.state_managers.validation.get_default_validation_state_manager",
        "endi.interfaces.IValidationStateManager",
        "endi.models.supply.internalsupplier_invoice.InternalSupplierInvoice",
        ("internalsupplier_invoice",),
    ),
    # Statut des jusitificatifs de NDD
    (
        "services.justified_state_manager.expense",
        "endi.controllers.state_managers.justified.get_default_justified_state_manager",
        "endi.interfaces.IJustifiedStateManager",
        [
            "endi.models.expense.sheet.ExpenseSheet",
            "endi.models.expense.sheet.ExpenseLine",
        ],
        ("expense",),
    ),
    # Statut de signature des Devis
    (
        "services.signed_state_manager.estimation",
        "endi.controllers.state_managers.signed.get_default_signed_status_manager",
        "endi.interfaces.ISignedStateManager",
        "endi.models.task.Estimation",
        ("estimation",),
    ),
    # Statut de paiement des factures/factures frns / NDDs
    (
        "services.payment_state_manager.invoice",
        "endi.controllers.state_managers.payment.get_default_payment_state_manager",
        "endi.interfaces.IPaymentStateManager",
        "endi.models.task.invoice.Invoice",
        ("invoice",),
    ),
    (
        "services.payment_state_manager.expense",
        "endi.controllers.state_managers.payment.get_default_payment_state_manager",
        "endi.interfaces.IPaymentStateManager",
        "endi.models.expense.sheet.ExpenseSheet",
        ("expense",),
    ),
    (
        "services.payment_state_manager.supplier_invoice",
        "endi.controllers.state_managers.payment.get_default_payment_state_manager",
        "endi.interfaces.IPaymentStateManager",
        "endi.models.supply.SupplierInvoice",
        ("supplier_invoice",),
    ),
)


def get_groups(login, request):
    """
    return the current user's groups
    """
    import logging

    logger = logging.getLogger(__name__)
    user = request.identity
    if user is None:
        logger.debug("User is None")
        principals = None

    elif getattr(request, "principals", []):
        principals = request.principals

    else:
        logger.debug(" + Building principals")
        principals = [f"user:{user.id}"]
        for group in user.login.groups:
            principals.append("group:{0}".format(group))

        for company in user.companies:
            if company.active:
                principals.append("company:{}".format(company.id))

        request.principals = principals
        logger.debug(" -> Principals Built : caching")

    return principals


def prepare_config(**settings):
    """
    Prepare the configuration object to setup the main application elements
    """
    session_factory = get_session_factory(settings)
    set_cache_regions_from_settings(settings)

    # Evite les imports circulaires avec endi_celery
    from endi.utils.security import SessionSecurityPolicy

    config = Configurator(
        settings=settings,
        # authentication_policy=auth_policy,
        # authorization_policy=acl_policy,
        session_factory=session_factory,
        security_policy=SessionSecurityPolicy(),
    )
    return config


def hack_endi_static_path(settings):
    if "endi.fanstatic_path" in settings:
        path_name = settings.get("endi.fanstatic_path")
        print(("Hacking fanstatic's source path with %s" % path_name))
        fanstatic_endi_library.path = path_name


def setup_bdd(settings):
    """
    Configure the database:

        - Intialize tables
        - populate database with default values

    :param obj settings: The ConfigParser object
    :returns: The dbsession
    :rtype: obj
    """
    from endi.models import adjust_for_engine

    engine = engine_from_config(settings, "sqlalchemy.")
    adjust_for_engine(engine)
    dbsession = initialize_sql(engine)
    return dbsession


def config_views(config):
    """
    Configure endi views
    """
    logger.debug("Loading views")

    # On register le module views.admin car il contient des outils spécifiques
    # pour les vues administrateurs (Ajout autonomatisé d'une arborescence,
    # ajout de la directive config.add_admin_view
    # Il s'occupe également d'intégrer toutes les vues, layouts... spécifiques
    # à l'administration
    config.include("endi.views.admin")

    config.include("endi.views.export.log_list")

    for module in ENDI_MANDATORY_MODULES:
        config.add_module(module)

    # Ici on permet la configuration des modules complémentaires depuis le .ini
    settings = config.registry.settings
    if "endi.modules" not in settings:
        modules = ENDI_OTHER_MODULES
    else:
        modules = settings.get("endi.modules", "").split()

    # Commit the configuration to allow overrides of core module views/routes
    # by optional modules views/routes
    config.commit()
    for module in modules:
        config.add_module(module)


def setup_request_methods(config, dbsession):
    from endi.models.config import get_config

    # Adding some usefull properties to the request object
    config.add_request_method(
        lambda _: dbsession(), "dbsession", property=True, reify=True
    )
    config.add_request_method(
        lambda _: get_config(), "config", property=True, reify=True
    )


def config_layouts(config):
    logger.debug("  + Adding layouts")
    for module in ENDI_LAYOUTS_MODULES:
        config.include(module)


def config_subscribers(config):
    logger.debug("  + Adding subscribers")
    for module in ENDI_REQUEST_SUBSCRIBERS:
        config.include(module)


def config_panels(config):
    logger.debug("  + Adding panels")
    for module in ENDI_PANELS_MODULES:
        config.include(module)


def config_events(config):
    logger.debug("  + Adding event hooks")
    for module in ENDI_EVENT_MODULES:
        config.include(module)


def config_services(config):
    """
    Setup the services (pyramid_services) used in de MooGLi
    """
    logger.debug("  + Adding pyramid_services")
    settings = config.registry.settings
    for service_name, default, interface, contexts, params in ENDI_SERVICES:
        module_path = settings.get("endi." + service_name, default)
        module = config.maybe_dotted(module_path)

        if not isinstance(contexts, (tuple, list)):
            contexts = [contexts]

        for ctx in contexts:
            config.register_service(module(*params), interface, context=ctx)

    for service_name, default, interface, contexts in ENDI_SERVICE_FACTORIES:
        module = settings.get("endi." + service_name, default)

        if not isinstance(contexts, (tuple, list)):
            contexts = [contexts]

        for ctx in contexts:
            config.register_service_factory(module, interface, context=ctx)


def add_static_views(config, settings):
    """
    Add the static views used in de MooGLi
    """
    statics = settings.get("endi.statics", "static")
    config.add_static_view(
        statics,
        "endi:static",
        cache_max_age=3600,
    )

    # Static path for generated files (exports / pdfs ...)
    tmp_static = settings.get("endi.static_tmp", "endi:tmp")
    config.add_static_view("cooked", tmp_static)

    # Allow to specify a custom fanstatic root path
    hack_endi_static_path(settings)


def add_http_error_views(config, settings):
    template_args = {"title": "Page non trouvée (erreur 404)"}
    config.add_notfound_view(
        view=lambda _: template_args,
        renderer="http_404.mako",
    )


def enable_sqla_listeners():
    from endi.models.listeners import SQLAListeners

    logger.debug("  + Enabling sqla listeners")
    SQLAListeners.start_listening()


def include_custom_modules(config):
    """
    Include custom modules using the endi.includes mechanism
    """
    settings = config.registry.settings
    for module in settings.get("endi.includes", "").split():
        if module.strip():
            config.add_plugin(module)


def configure_traversal(config, dbsession) -> Configurator:
    """
    Configure the traversal related informations
    - Set acls on models
    - Setup the root factory
    - Set the default permission
    """
    logger.debug("  + Setting up traversal")
    from endi.utils.security import (
        RootFactory,
        TraversalDbAccess,
        set_models_acl,
    )

    set_models_acl()
    TraversalDbAccess.dbsession = dbsession

    # Application main configuration
    config.set_root_factory(RootFactory)
    config.set_default_permission("view")
    return config


def add_base_directives_and_predicates(config):
    """
    Add custom predicates and directives used in de MooGLi's codebase
    """
    logger.debug("  + Adding predicates and directives")
    from endi.utils.predicates import SettingHasValuePredicate
    from endi.utils.security import ApiKeyAuthenticationPredicate

    # On ajoute le registre 'modules' et ses directives
    config.include("endi.utils.modules")

    # On ajoute le registre 'dataqueries' et ses directives
    config.include("endi.utils.dataqueries")
    # On charge également le module des requêtes
    config.include("endi.dataqueries")

    # Allows to restrict view acces only if a setting is set
    config.add_view_predicate("if_setting_has_value", SettingHasValuePredicate)
    # Allows to authentify a view through hmac api key auth
    config.add_view_predicate("api_key_authentication", ApiKeyAuthenticationPredicate)

    # Shortcut to add rest service (collection + Add / edit delete views)
    config.add_directive("add_rest_service", add_rest_service)

    return config


def prepare_view_config(config, dbsession, from_tests, **settings):
    """
    Prepare view configuration

    Configure all tools used to include views
    """
    logger.debug("Preparing elements before loading views")
    configure_traversal(config, dbsession)
    add_base_directives_and_predicates(config)
    setup_request_methods(config, dbsession)

    # Customize renderers (json, form rendering with i18n ...)
    config.include(customize_renderers)

    # Events and pyramid_services
    config.include(config_subscribers)
    config.include(config_events)
    config.include(config_services)
    config.include("endi.utils.menu")
    config.include("endi.utils.notification")
    if from_tests:
        # add_tree_view_directive attache des classes les unes aux autres et
        # provoquent des problèmes ingérables dans les tests
        # TODO: Il devrait utiliser le registry pour attacher parents et
        # enfants
        def add_tree_view_directive(config, *args, **kwargs):
            if "parent" in kwargs:
                kwargs.pop("parent")
            if "route_name" not in kwargs:
                # Use the route_name set on the view by default
                kwargs["route_name"] = args[0].route_name
            config.add_view(*args, **kwargs)

    else:
        from endi.views import add_tree_view_directive
    config.add_directive("add_tree_view", add_tree_view_directive)

    # Widgets base layout related includes
    add_static_views(config, settings)
    add_http_error_views(config, settings)
    config.include(config_layouts)
    config.include(config_panels)
    return config


def base_configure(config, dbsession, from_tests=False, **settings):
    """
    All plugin and others configuration stuff
    """
    prepare_view_config(config, dbsession, from_tests, **settings)
    config.include(config_views)

    config.commit()
    config.begin()

    config.include(include_custom_modules)

    enable_sqla_listeners()

    return config


def version(strip_suffix=False) -> str:
    """
    Return de MooGLi's version number (as defined in setup.py)

    :param: strip any suffix after patch release (ex: 1.2.3b3 → 1.2.3)
    """
    if strip_suffix:
        return pkg_resources.parse_version(package_version).base_version
    else:
        return package_version


def main(global_config, **settings):
    """
    Main entry function

    :returns: a Pyramid WSGI application.
    """
    configure_warnings()
    # Récupère les variables d'environnement
    settings = collect_envvars_as_settings(settings)
    config = prepare_config(**settings)

    logger.debug("Setting up the bdd")
    dbsession = setup_bdd(settings)
    config = base_configure(config, dbsession, **settings)
    config.include("endi.utils.sqlalchemy_fix")

    logger.debug("Configuring file depot")
    configure_filedepot(settings)

    config.configure_celery(global_config["__file__"])

    return config.make_wsgi_app()
