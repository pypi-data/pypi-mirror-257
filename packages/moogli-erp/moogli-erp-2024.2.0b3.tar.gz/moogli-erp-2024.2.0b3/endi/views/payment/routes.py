INVOICE_PAYMENT_ADD = "/invoices/{id}/addpayment"
EXPENSE_PAYMENT_ADD = "/expenses/{id}/addpayment"


def includeme(config):
    """
    Add module's related routes
    """
    # Invoice payments
    route = INVOICE_PAYMENT_ADD
    pattern = r"{}".format(route.replace("id", r"id:\d+"))

    config.add_route(
        route,
        pattern,
        traverse="/tasks/{id}",
    )
    config.add_route(
        "payment",
        r"/payments/{id:\d+}",
        traverse="/base_task_payments/{id}",
    )
    # Expense payments
    route = EXPENSE_PAYMENT_ADD
    pattern = r"{}".format(route.replace("id", r"id:\d+"))
    config.add_route(
        route,
        pattern,
        traverse="/expenses/{id}",
    )
    config.add_route(
        "expense_payment",
        r"/expense_payments/{id:\d+}",
        traverse="/expense_payments/{id}",
    )

    # Supplier invoice payments
    config.add_route(
        "supplier_payment",
        r"/supplier_payments/{id:\d+}",
        traverse="/supplier_payments/{id}",
    )
