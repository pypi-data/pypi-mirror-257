import logging
import meilisearch

from endi.utils.datetimes import datetime_to_timestamp

from .client import get_meilisearch_client, configure_meilisearch_index

logger = logging.getLogger(__name__)


CUSTOMERS_SETTINGS = {
    "displayedAttributes": ["*"],
    "searchableAttributes": [
        "label",
        "code",
        "registration",
        "city",
        "zip_code",
        "address",
        "compte_cg",
        "compte_tiers",
        "company",
    ],
    "filterableAttributes": [
        "label",
        "code",
        "city",
        "zip_code",
        "type",
        "compte_cg",
        "compte_tiers",
        "archived",
    ],
    "sortableAttributes": ["label", "created_at", "updated_at", "company.label"],
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


def serialize_customer(request, customer) -> dict:
    """
    Build the customer representation used in the meilisearch "customers" index
    """
    result = {
        "id": customer.id,
        "type": customer.type,
        "label": customer.label,
        "created_at": datetime_to_timestamp(customer.created_at),
        "updated_at": datetime_to_timestamp(customer.updated_at),
        "archived": customer.archived,
        "code": customer.code,
        "registration": customer.registration,
        "city": customer.city,
        "zip_code": customer.zip_code,
        "address": f"{customer.address}\n{customer.additional_address}",
        "compte_cg": customer.compte_cg,
        "compte_tiers": customer.compte_tiers,
        "company": {
            "id": customer.company_id,
            "name": customer.company.name,
        },
        "url": f"/customers/{customer.id}",
        "__acl__": customer.__acl__,
    }

    if callable(result["__acl__"]):
        result["__acl__"] = customer.__acl__()
    return result


def push_customer(request, customer):
    """
    Add/update a customer in the meilisearch "customer" index
    """
    serialized = serialize_customer(request, customer)
    client = get_meilisearch_client(request)
    client.index("customers").add_documents([serialized])


def push_customers(request, customers):
    """
    Add customers to the meilisearch "customers" index
    """
    documents = []
    for customer in customers:
        documents.append(serialize_customer(request, customer))

    client = get_meilisearch_client(request)
    client.index("customers").add_documents(documents)


def configure_index(request) -> meilisearch.Client:
    """
    Configure the meilisearch index using the given settings
    """
    return configure_meilisearch_index(request, "customers", CUSTOMERS_SETTINGS)
