"""
Attached files related views
"""
from endi.views.business.routes import (
    BUSINESS_ITEM_FILE_ROUTE,
    BUSINESS_ITEM_ADD_FILE_ROUTE,
)
from endi.views.project.business import ProjectBusinessListView
from endi.views.project.files import (
    ProjectFileAddView,
    ProjectFilesView,
)
from .business import BusinessOverviewView


class BusinessFileAddView(ProjectFileAddView):
    route_name = BUSINESS_ITEM_ADD_FILE_ROUTE


class BusinessFilesView(ProjectFilesView):
    route_name = BUSINESS_ITEM_FILE_ROUTE

    @property
    def title(self):
        return "Fichiers attachés au dossier {0}".format(self.context.project.name)

    def get_project_id(self):
        return self.context.project_id

    def _get_js_app_options(self):
        result = super()._get_js_app_options()
        result["business_id"] = self.context.id
        return result


def includeme(config):
    config.add_tree_view(
        BusinessFileAddView,
        parent=BusinessOverviewView,
        permission="add.file",
        layout="default",
        renderer="endi:templates/base/formpage.mako",
    )
    config.add_tree_view(
        BusinessFilesView,
        parent=ProjectBusinessListView,
        permission="list.files",
        renderer="endi:templates/business/files.mako",
        layout="business",
    )
