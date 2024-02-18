from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.v1_alpha_integration import V1AlphaIntegration
from ...types import UNSET, Response, Unset


def _get_kwargs(
    collection: str,
    *,
    body: V1AlphaIntegration,
    integration_id: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    params: Dict[str, Any] = {}

    params["integrationId"] = integration_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": f"/v1alpha/{collection}/integrations",
        "params": params,
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[V1AlphaIntegration]:
    if response.status_code == HTTPStatus.OK:
        response_200 = V1AlphaIntegration.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[V1AlphaIntegration]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    collection: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: V1AlphaIntegration,
    integration_id: Union[Unset, str] = UNSET,
) -> Response[V1AlphaIntegration]:
    """Create an Integration.

    Args:
        collection (str):
        integration_id (Union[Unset, str]):
        body (V1AlphaIntegration): Integrations instruct seqq to import Sequences from external
            sources.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[V1AlphaIntegration]
    """

    kwargs = _get_kwargs(
        collection=collection,
        body=body,
        integration_id=integration_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    collection: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: V1AlphaIntegration,
    integration_id: Union[Unset, str] = UNSET,
) -> Optional[V1AlphaIntegration]:
    """Create an Integration.

    Args:
        collection (str):
        integration_id (Union[Unset, str]):
        body (V1AlphaIntegration): Integrations instruct seqq to import Sequences from external
            sources.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        V1AlphaIntegration
    """

    return sync_detailed(
        collection=collection,
        client=client,
        body=body,
        integration_id=integration_id,
    ).parsed


async def asyncio_detailed(
    collection: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: V1AlphaIntegration,
    integration_id: Union[Unset, str] = UNSET,
) -> Response[V1AlphaIntegration]:
    """Create an Integration.

    Args:
        collection (str):
        integration_id (Union[Unset, str]):
        body (V1AlphaIntegration): Integrations instruct seqq to import Sequences from external
            sources.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[V1AlphaIntegration]
    """

    kwargs = _get_kwargs(
        collection=collection,
        body=body,
        integration_id=integration_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    collection: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: V1AlphaIntegration,
    integration_id: Union[Unset, str] = UNSET,
) -> Optional[V1AlphaIntegration]:
    """Create an Integration.

    Args:
        collection (str):
        integration_id (Union[Unset, str]):
        body (V1AlphaIntegration): Integrations instruct seqq to import Sequences from external
            sources.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        V1AlphaIntegration
    """

    return (
        await asyncio_detailed(
            collection=collection,
            client=client,
            body=body,
            integration_id=integration_id,
        )
    ).parsed
