from endi.resources import admin_resources
from endi.utils.sys_environment import package_version


class AdminLayout:
    endi_version = package_version

    def __init__(self, context, request):
        admin_resources.need()


def includeme(config):
    config.add_layout(
        AdminLayout,
        template="endi:templates/admin/layout.mako",
        name="admin",
    )
