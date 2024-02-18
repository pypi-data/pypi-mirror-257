from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.v1_alpha_sequence import V1AlphaSequence
from ...types import UNSET, Response


def _get_kwargs(
    collection: str,
    *,
    body: V1AlphaSequence,
    sequence_id: str,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    params: Dict[str, Any] = {}

    params["sequenceId"] = sequence_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": f"/v1alpha/{collection}/sequences",
        "params": params,
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[V1AlphaSequence]:
    if response.status_code == HTTPStatus.OK:
        response_200 = V1AlphaSequence.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[V1AlphaSequence]:
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
    body: V1AlphaSequence,
    sequence_id: str,
) -> Response[V1AlphaSequence]:
    """Create a Sequence in a Collection.

    Args:
        collection (str):
        sequence_id (str):
        body (V1AlphaSequence): Sequence is a single entry containing nucleotides or amino acids
            and other optional metadata like a description, creation time, and taxonomy ID.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[V1AlphaSequence]
    """

    kwargs = _get_kwargs(
        collection=collection,
        body=body,
        sequence_id=sequence_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    collection: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: V1AlphaSequence,
    sequence_id: str,
) -> Optional[V1AlphaSequence]:
    """Create a Sequence in a Collection.

    Args:
        collection (str):
        sequence_id (str):
        body (V1AlphaSequence): Sequence is a single entry containing nucleotides or amino acids
            and other optional metadata like a description, creation time, and taxonomy ID.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        V1AlphaSequence
    """

    return sync_detailed(
        collection=collection,
        client=client,
        body=body,
        sequence_id=sequence_id,
    ).parsed


async def asyncio_detailed(
    collection: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: V1AlphaSequence,
    sequence_id: str,
) -> Response[V1AlphaSequence]:
    """Create a Sequence in a Collection.

    Args:
        collection (str):
        sequence_id (str):
        body (V1AlphaSequence): Sequence is a single entry containing nucleotides or amino acids
            and other optional metadata like a description, creation time, and taxonomy ID.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[V1AlphaSequence]
    """

    kwargs = _get_kwargs(
        collection=collection,
        body=body,
        sequence_id=sequence_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    collection: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: V1AlphaSequence,
    sequence_id: str,
) -> Optional[V1AlphaSequence]:
    """Create a Sequence in a Collection.

    Args:
        collection (str):
        sequence_id (str):
        body (V1AlphaSequence): Sequence is a single entry containing nucleotides or amino acids
            and other optional metadata like a description, creation time, and taxonomy ID.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        V1AlphaSequence
    """

    return (
        await asyncio_detailed(
            collection=collection,
            client=client,
            body=body,
            sequence_id=sequence_id,
        )
    ).parsed
