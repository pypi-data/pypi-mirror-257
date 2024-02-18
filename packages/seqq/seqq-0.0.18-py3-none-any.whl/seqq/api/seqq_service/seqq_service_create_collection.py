from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.v1_alpha_collection import V1AlphaCollection
from ...types import UNSET, Response


def _get_kwargs(
    *,
    body: V1AlphaCollection,
    collection_id: str,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    params: Dict[str, Any] = {}

    params["collectionId"] = collection_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/v1alpha/collections",
        "params": params,
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[V1AlphaCollection]:
    if response.status_code == HTTPStatus.OK:
        response_200 = V1AlphaCollection.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[V1AlphaCollection]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: V1AlphaCollection,
    collection_id: str,
) -> Response[V1AlphaCollection]:
    """Create a Collection.

    Args:
        collection_id (str):
        body (V1AlphaCollection): Collections contain Sequences, Searches, and Integration.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[V1AlphaCollection]
    """

    kwargs = _get_kwargs(
        body=body,
        collection_id=collection_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: V1AlphaCollection,
    collection_id: str,
) -> Optional[V1AlphaCollection]:
    """Create a Collection.

    Args:
        collection_id (str):
        body (V1AlphaCollection): Collections contain Sequences, Searches, and Integration.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        V1AlphaCollection
    """

    return sync_detailed(
        client=client,
        body=body,
        collection_id=collection_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: V1AlphaCollection,
    collection_id: str,
) -> Response[V1AlphaCollection]:
    """Create a Collection.

    Args:
        collection_id (str):
        body (V1AlphaCollection): Collections contain Sequences, Searches, and Integration.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[V1AlphaCollection]
    """

    kwargs = _get_kwargs(
        body=body,
        collection_id=collection_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: V1AlphaCollection,
    collection_id: str,
) -> Optional[V1AlphaCollection]:
    """Create a Collection.

    Args:
        collection_id (str):
        body (V1AlphaCollection): Collections contain Sequences, Searches, and Integration.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        V1AlphaCollection
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            collection_id=collection_id,
        )
    ).parsed
