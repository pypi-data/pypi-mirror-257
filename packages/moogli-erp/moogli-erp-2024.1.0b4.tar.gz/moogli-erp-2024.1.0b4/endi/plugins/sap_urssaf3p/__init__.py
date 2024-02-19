import endi


def includeme(config):
    config.include(".populate")
    config.include(".endi_admin_commands")  # Ugly
    # add_view fails in an hard to debug way within testing context.
    if not endi._called_from_test:
        config.include(".views")
