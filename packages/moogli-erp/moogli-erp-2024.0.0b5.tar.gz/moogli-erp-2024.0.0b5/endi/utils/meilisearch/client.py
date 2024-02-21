import logging
import meilisearch


logger = logging.getLogger(__name__)


def get_meilisearch_client_url(request) -> str:
    return request.registry.settings.get(
        "meilisearch.client.url", "http://meilisearch:7700"
    )


def get_meilisearch_client_public_url(request) -> str:
    return request.registry.settings.get(
        "meilisearch.client.public_url", "http://localhost:7700"
    )


def get_meilisearch_client(request) -> meilisearch.Client:
    """Build a meilisearch client"""
    client_url = get_meilisearch_client_url(request)
    client_api_key = request.registry.settings.get(
        "meilisearch.client.master_key", "meilisearch"
    )
    logger.debug(f"Connecting to meilisearch at {client_url} {client_api_key}")
    client = meilisearch.Client(client_url, client_api_key)
    return client


def configure_meilisearch_index(
    request, index_name: str, settings: dict
) -> meilisearch.Client:
    """
    Configure the meilisearch index using the given settings
    """
    client = get_meilisearch_client(request)
    client.create_index(index_name, {"primaryKey": "id"})
    client.index(index_name).update_settings(settings)
    return client
