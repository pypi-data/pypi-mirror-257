"""
View related to admin configuration
"""
import logging
import os

from endi.forms.admin import get_config_schema
from endi.views.admin.tools import (
    BaseConfigView,
)
from endi.views.admin.main import (
    MainIndexView,
    MAIN_ROUTE,
)

MAIN_CONTACT_ROUTE = os.path.join(MAIN_ROUTE, "contact")


logger = logging.getLogger(__name__)


class AdminContactView(BaseConfigView):
    """
    Admin welcome page
    """

    title = "Adresse e-mail de contact de MooGLi"
    description = "Configurer l'adresse utilisée par de MooGLi pour vous \
envoyer des messages (traitement des fichiers…)"

    route_name = MAIN_CONTACT_ROUTE
    keys = ("cae_admin_mail",)
    schema = get_config_schema(keys)


def includeme(config):
    config.add_route(MAIN_CONTACT_ROUTE, MAIN_CONTACT_ROUTE)
    config.add_admin_view(
        AdminContactView,
        parent=MainIndexView,
    )
