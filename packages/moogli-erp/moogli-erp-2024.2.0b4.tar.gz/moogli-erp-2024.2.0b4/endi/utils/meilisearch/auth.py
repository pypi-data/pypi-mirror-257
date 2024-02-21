"""
Meilisearch authentication stuff

Meilisearch uses 3 levels of authentication : 

    - Master key : set once (in the ini file)
    - Api keys : (two are created by default 'admin' and 'search')
    - Tokens : Token with specific rights


"""
import datetime
from typing import Optional
from .client import get_meilisearch_client


def get_user_token(request, company_id: Optional[int] = None) -> str:
    """
    Get the current connected user's token
    """
    api_key = get_or_create_user_api_key(request)

    if company_id is not None:
        search_rules = {"invoices": {"filter": f"company.id = {company_id}"}}
    elif request.has_permission("admin_invoices"):
        search_rules = {"invoices": {"filter": "status = 'valid'"}}
    else:
        raise Exception("You don't have permission to access this endpoint")

    client = get_meilisearch_client(request)
    expires_at = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(
        days=3
    )
    return client.generate_tenant_token(
        api_key_uid=api_key.uid,
        search_rules=search_rules,
        api_key=api_key.key,
        expires_at=expires_at,
    )


def get_admin_key(request):
    """Collect the Meilisearch client key"""
    client = get_meilisearch_client(request)
    api_keys = client.get_keys()
    return api_keys.results[1]


def get_or_create_user_api_key(request):
    """
    Get or create a user api key for the current user
    """
    return get_admin_key(request)
