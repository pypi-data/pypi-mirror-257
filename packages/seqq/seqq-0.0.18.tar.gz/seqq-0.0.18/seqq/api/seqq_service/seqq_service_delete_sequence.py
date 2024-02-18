from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.seqq_service_delete_sequence_response_200 import SeqqServiceDeleteSequenceResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    name_1: str,
    *,
    force: Union[Unset, bool] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["force"] = force

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "delete",
        "url": f"/v1alpha/{name_1}",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[SeqqServiceDeleteSequenceResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = SeqqServiceDeleteSequenceResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[SeqqServiceDeleteSequenceResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    name_1: str,
    *,
    client: Union[AuthenticatedClient, Client],
    force: Union[Unset, bool] = UNSET,
) -> Response[SeqqServiceDeleteSequenceResponse200]:
    """Delete a Sequence by name.

    Args:
        name_1 (str):
        force (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SeqqServiceDeleteSequenceResponse200]
    """

    kwargs = _get_kwargs(
        name_1=name_1,
        force=force,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    name_1: str,
    *,
    client: Union[AuthenticatedClient, Client],
    force: Union[Unset, bool] = UNSET,
) -> Optional[SeqqServiceDeleteSequenceResponse200]:
    """Delete a Sequence by name.

    Args:
        name_1 (str):
        force (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SeqqServiceDeleteSequenceResponse200
    """

    return sync_detailed(
        name_1=name_1,
        client=client,
        force=force,
    ).parsed


async def asyncio_detailed(
    name_1: str,
    *,
    client: Union[AuthenticatedClient, Client],
    force: Union[Unset, bool] = UNSET,
) -> Response[SeqqServiceDeleteSequenceResponse200]:
    """Delete a Sequence by name.

    Args:
        name_1 (str):
        force (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SeqqServiceDeleteSequenceResponse200]
    """

    kwargs = _get_kwargs(
        name_1=name_1,
        force=force,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    name_1: str,
    *,
    client: Union[AuthenticatedClient, Client],
    force: Union[Unset, bool] = UNSET,
) -> Optional[SeqqServiceDeleteSequenceResponse200]:
    """Delete a Sequence by name.

    Args:
        name_1 (str):
        force (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SeqqServiceDeleteSequenceResponse200
    """

    return (
        await asyncio_detailed(
            name_1=name_1,
            client=client,
            force=force,
        )
    ).parsed
