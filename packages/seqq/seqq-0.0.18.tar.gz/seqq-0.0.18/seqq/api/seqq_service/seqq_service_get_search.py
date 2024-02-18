from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.v1_alpha_search import V1AlphaSearch
from ...types import Response


def _get_kwargs(
    name_2: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/v1alpha/{name_2}",
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[V1AlphaSearch]:
    if response.status_code == HTTPStatus.OK:
        response_200 = V1AlphaSearch.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[V1AlphaSearch]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    name_2: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[V1AlphaSearch]:
    """Get a Search by name.

    Args:
        name_2 (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[V1AlphaSearch]
    """

    kwargs = _get_kwargs(
        name_2=name_2,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    name_2: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[V1AlphaSearch]:
    """Get a Search by name.

    Args:
        name_2 (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        V1AlphaSearch
    """

    return sync_detailed(
        name_2=name_2,
        client=client,
    ).parsed


async def asyncio_detailed(
    name_2: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[V1AlphaSearch]:
    """Get a Search by name.

    Args:
        name_2 (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[V1AlphaSearch]
    """

    kwargs = _get_kwargs(
        name_2=name_2,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    name_2: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[V1AlphaSearch]:
    """Get a Search by name.

    Args:
        name_2 (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        V1AlphaSearch
    """

    return (
        await asyncio_detailed(
            name_2=name_2,
            client=client,
        )
    ).parsed
