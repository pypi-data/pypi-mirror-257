from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.seqq_service_batch_create_sequences_body import SeqqServiceBatchCreateSequencesBody
from ...models.v1_alpha_batch_create_sequences_response import V1AlphaBatchCreateSequencesResponse
from ...types import Response


def _get_kwargs(
    collection: str,
    *,
    body: SeqqServiceBatchCreateSequencesBody,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": f"/v1alpha/{collection}/sequences:batchCreate",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[V1AlphaBatchCreateSequencesResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = V1AlphaBatchCreateSequencesResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[V1AlphaBatchCreateSequencesResponse]:
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
    body: SeqqServiceBatchCreateSequencesBody,
) -> Response[V1AlphaBatchCreateSequencesResponse]:
    """Create a batch of Sequences in a Collection.

    Args:
        collection (str):
        body (SeqqServiceBatchCreateSequencesBody): BatchCreateSequencesRequest specifies how to
            create a batch of sequences at once.
            Sequences in requests that already exist are ignored and not returned in the response.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[V1AlphaBatchCreateSequencesResponse]
    """

    kwargs = _get_kwargs(
        collection=collection,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    collection: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: SeqqServiceBatchCreateSequencesBody,
) -> Optional[V1AlphaBatchCreateSequencesResponse]:
    """Create a batch of Sequences in a Collection.

    Args:
        collection (str):
        body (SeqqServiceBatchCreateSequencesBody): BatchCreateSequencesRequest specifies how to
            create a batch of sequences at once.
            Sequences in requests that already exist are ignored and not returned in the response.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        V1AlphaBatchCreateSequencesResponse
    """

    return sync_detailed(
        collection=collection,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    collection: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: SeqqServiceBatchCreateSequencesBody,
) -> Response[V1AlphaBatchCreateSequencesResponse]:
    """Create a batch of Sequences in a Collection.

    Args:
        collection (str):
        body (SeqqServiceBatchCreateSequencesBody): BatchCreateSequencesRequest specifies how to
            create a batch of sequences at once.
            Sequences in requests that already exist are ignored and not returned in the response.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[V1AlphaBatchCreateSequencesResponse]
    """

    kwargs = _get_kwargs(
        collection=collection,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    collection: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: SeqqServiceBatchCreateSequencesBody,
) -> Optional[V1AlphaBatchCreateSequencesResponse]:
    """Create a batch of Sequences in a Collection.

    Args:
        collection (str):
        body (SeqqServiceBatchCreateSequencesBody): BatchCreateSequencesRequest specifies how to
            create a batch of sequences at once.
            Sequences in requests that already exist are ignored and not returned in the response.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        V1AlphaBatchCreateSequencesResponse
    """

    return (
        await asyncio_detailed(
            collection=collection,
            client=client,
            body=body,
        )
    ).parsed
