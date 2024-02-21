import datetime
import logging
import meilisearch

from endi.compute.math_utils import integer_to_amount

from endi.utils.strings import format_amount
from endi.utils.datetimes import date_to_timestamp

from endi.views.task.utils import get_task_url

from .client import configure_meilisearch_index, get_meilisearch_client

logger = logging.getLogger(__name__)


INVOICES_SETTINGS = {
    "displayedAttributes": ["*"],
    "searchableAttributes": [
        "customer.label",
        "company.label",
        "company.code_compta",
        "official_number",
        "ttc_label",
    ],
    "filterableAttributes": [
        "official_number",
        "status",
        "paid_status",
        "type_",
        "ht",
        "ttc",
        "customer.label",
        "date",
        "company",
        "business_type",
        "customer",
    ],
    "sortableAttributes": ["date", "status_date", "customer.label", "company.label"],
    "rankingRules": ["words", "typo", "proximity", "attribute", "sort", "exactness"],
    "stopWords": [],
    "nonSeparatorTokens": [],
    "separatorTokens": [],
    "dictionary": [],
    "synonyms": {},
    "distinctAttribute": None,
    "typoTolerance": {
        "enabled": True,
        "minWordSizeForTypos": {"oneTypo": 5, "twoTypos": 9},
        "disableOnWords": [],
        "disableOnAttributes": [],
    },
    "faceting": {"maxValuesPerFacet": 100, "sortFacetValuesBy": {"*": "alpha"}},
    "pagination": {"maxTotalHits": 10000},
}


def serialize_invoice(request, invoice) -> dict:
    """
    Build the invoice representation used in the meilisearch "invoices" index
    """
    result = {
        "id": invoice.id,
        "type_": invoice.type_,
        "name": invoice.name,
        "date": date_to_timestamp(invoice.date),
        "financial_year": invoice.financial_year,
        "status": invoice.status,
        "status_date": datetime.datetime.timestamp(invoice.status_date),
        "ht": invoice.ht,
        "tva": invoice.tva,
        "ttc": invoice.ttc,
        "ht_label": format_amount(invoice.ht, precision=5),
        "tva_label": format_amount(invoice.tva, precision=5),
        "ttc_label": format_amount(invoice.ttc, precision=5),
        "customer": {
            "id": invoice.customer_id,
            "label": invoice.customer.label,
        },
        "company": {
            "id": invoice.company_id,
            "name": invoice.company.name,
            "code_compta": invoice.company.code_compta,
        },
        "business_type": {
            "id": invoice.business_type_id,
            "label": invoice.business_type.label,
            "name": invoice.business_type.name,
        },
        "url": get_task_url(request, invoice),
        "paid_status": getattr(invoice, "paid_status", "resulted"),
        "payments": [
            {
                "id": payment.id,
                "url": f"/payments/{payment.id}",
                "date": date_to_timestamp(payment.date),
                "amount": payment.amount,
            }
            for payment in invoice.payments
        ],
        "files": [
            {
                "url": f"/files/{file.id}",
                "name": file.name,
            }
            for file in invoice.files
        ],
        "cancelinvoices": [
            {
                "id": cancelinvoice.id,
                "url": f"/cancelinvoices/{cancelinvoice.id}",
                "date": date_to_timestamp(cancelinvoice.date),
                "ttc": cancelinvoice.ttc,
                "official_number": cancelinvoice.official_number,
            }
            for cancelinvoice in getattr(invoice, "cancelinvoices", [])
            if cancelinvoice.status == "valid"
        ],
        "global_status": invoice.global_status,
        "official_number": invoice.official_number,
        "__acl__": invoice.__acl__,
    }
    if hasattr(invoice, "topay"):
        result["topay"] = integer_to_amount(invoice.topay(), precision=5)
    if callable(result["__acl__"]):
        result["__acl__"] = invoice.__acl__()
    return result


def push_invoice(request, invoice):
    """
    Add/update an invoice in the meilisearch "invoices" index
    """
    serialized = serialize_invoice(request, invoice)
    client = get_meilisearch_client(request)
    client.index("invoices").add_documents([serialized])


def push_invoices(request, invoices):
    """
    Add invoices to the meilisearch "invoices" index
    """
    documents = []
    for invoice in invoices:
        documents.append(serialize_invoice(request, invoice))

    client = get_meilisearch_client(request)
    client.index("invoices").add_documents(documents)


def configure_index(request) -> meilisearch.Client:
    """
    Configure the meilisearch index using the given settings
    """
    return configure_meilisearch_index(request, "invoices", INVOICES_SETTINGS)
