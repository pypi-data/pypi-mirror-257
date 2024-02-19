import logging

from pyramid.csrf import get_csrf_token

from endi import package_version
from endi.resources import main_group, opa_group, opa_vue_group, notification_js


logger = logging.getLogger(__name__)


class DefaultLayout:
    endi_version = package_version
    js_resource_group = main_group

    def __init__(self, context, request):
        self.js_resource_group.need()
        if not getattr(request, "is_popup", True):
            notification_js.need()
        self.context = context
        self.request = request


class OpaLayout(DefaultLayout):
    js_resource_group = opa_group

    @property
    def js_app_options(self):
        return {
            "csrf_token": get_csrf_token(self.request),
            "static_path": self.request.static_path("endi:static/"),
        }


class VueOpaLayout(OpaLayout):
    js_resource_group = opa_vue_group


def includeme(config):
    config.add_layout(DefaultLayout, template="endi:templates/layouts/default.mako")
    config.add_layout(
        DefaultLayout,
        template="endi:templates/layouts/default.mako",
        name="default",
    )
    config.add_layout(
        OpaLayout, template="endi:templates/layouts/default.mako", name="opa"
    )
    config.add_layout(
        OpaLayout, template="endi:templates/layouts/default.mako", name="vue_opa"
    )
    config.add_layout(
        DefaultLayout,
        template="endi:templates/layouts/login.mako",
        name="login",
    )
