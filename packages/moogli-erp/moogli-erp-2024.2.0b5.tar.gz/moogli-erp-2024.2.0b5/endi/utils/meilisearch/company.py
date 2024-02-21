import logging
import meilisearch

from endi.utils.datetimes import datetime_to_timestamp

from .client import get_meilisearch_client, configure_meilisearch_index

logger = logging.getLogger(__name__)


COMPANIES_SETTINGS = {
    "displayedAttributes": ["*"],
    "searchableAttributes": ["name", "email", "city", "zip_code", "employees"],
    "filterableAttributes": [
        "name",
        "employees",
        "follower",
        "antenne",
        "city",
        "active",
        "zip_code",
        "code_compta",
    ],
    "sortableAttributes": ["name", "created_at", "updated_at", "zip_code", "city"],
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


def serialize_company(request, company) -> dict:
    """
    Build the company representation used in the meilisearch "companies" index
    """
    result = {
        "id": company.id,
        "name": company.name,
        "created_at": datetime_to_timestamp(company.created_at),
        "updated_at": datetime_to_timestamp(company.updated_at),
        "archived": company.active,
        "code_compta": company.code_compta,
        "city": company.city,
        "zip_code": company.zip_code,
        "address": company.address,
        "contribution": company.contribution,
        "antenne": {},
        "follower": {},
        "employees": [
            {
                "id": employee.id,
                "label": employee.label,
                "active": employee.active,
            }
            for employee in company.employees
        ],
        "url": f"/companies/{company.id}",
        "__acl__": company.__acl__,
    }
    if company.follower:
        result["follower"] = {
            "id": company.follower_id,
            "label": company.follower.label,
        }
    if company.antenne:
        result["antenne"] = {"id": company.antenne_id, "label": company.antenne.label}
    if callable(result["__acl__"]):
        result["__acl__"] = company.__acl__()
    return result


def push_company(request, company):
    """
    Add/update a company in the meilisearch "company" index
    """
    serialized = serialize_company(request, company)
    client = get_meilisearch_client(request)
    client.index("companies").add_documents([serialized])


def push_companies(request, companies):
    """
    Add companies to the meilisearch "companies" index
    """
    documents = []
    for company in companies:
        documents.append(serialize_company(request, company))

    client = get_meilisearch_client(request)
    client.index("companies").add_documents(documents)


def configure_index(request) -> meilisearch.Client:
    """
    Configure the meilisearch index using the given settings
    """
    return configure_meilisearch_index(request, "companies", COMPANIES_SETTINGS)
