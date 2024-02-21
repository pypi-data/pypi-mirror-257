def includeme(config):
    config.include(".layout")
    config.include(".routes")
    config.include(".lists")
    config.include(".supplier")
    config.include(".rest_api")
    config.include("endi.views.admin.supplier")
