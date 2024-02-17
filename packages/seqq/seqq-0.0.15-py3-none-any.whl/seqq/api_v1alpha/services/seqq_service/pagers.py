# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from typing import Any, AsyncIterator, Awaitable, Callable, Sequence, Tuple, Optional, Iterator

from seqq.api_v1alpha.types import collection
from seqq.api_v1alpha.types import integration
from seqq.api_v1alpha.types import search
from seqq.api_v1alpha.types import sequence


class ListCollectionsPager:
    """A pager for iterating through ``list_collections`` requests.

    This class thinly wraps an initial
    :class:`seqq.api_v1alpha.types.ListCollectionsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``collections`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListCollections`` requests and continue to iterate
    through the ``collections`` field on the
    corresponding responses.

    All the usual :class:`seqq.api_v1alpha.types.ListCollectionsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """
    def __init__(self,
            method: Callable[..., collection.ListCollectionsResponse],
            request: collection.ListCollectionsRequest,
            response: collection.ListCollectionsResponse,
            *,
            metadata: Sequence[Tuple[str, str]] = ()):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (seqq.api_v1alpha.types.ListCollectionsRequest):
                The initial request object.
            response (seqq.api_v1alpha.types.ListCollectionsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = collection.ListCollectionsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[collection.ListCollectionsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[collection.Collection]:
        for page in self.pages:
            yield from page.collections

    def __repr__(self) -> str:
        return '{0}<{1!r}>'.format(self.__class__.__name__, self._response)


class ListCollectionsAsyncPager:
    """A pager for iterating through ``list_collections`` requests.

    This class thinly wraps an initial
    :class:`seqq.api_v1alpha.types.ListCollectionsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``collections`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListCollections`` requests and continue to iterate
    through the ``collections`` field on the
    corresponding responses.

    All the usual :class:`seqq.api_v1alpha.types.ListCollectionsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """
    def __init__(self,
            method: Callable[..., Awaitable[collection.ListCollectionsResponse]],
            request: collection.ListCollectionsRequest,
            response: collection.ListCollectionsResponse,
            *,
            metadata: Sequence[Tuple[str, str]] = ()):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (seqq.api_v1alpha.types.ListCollectionsRequest):
                The initial request object.
            response (seqq.api_v1alpha.types.ListCollectionsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = collection.ListCollectionsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[collection.ListCollectionsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response
    def __aiter__(self) -> AsyncIterator[collection.Collection]:
        async def async_generator():
            async for page in self.pages:
                for response in page.collections:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return '{0}<{1!r}>'.format(self.__class__.__name__, self._response)


class ListSequencesPager:
    """A pager for iterating through ``list_sequences`` requests.

    This class thinly wraps an initial
    :class:`seqq.api_v1alpha.types.ListSequencesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``sequences`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListSequences`` requests and continue to iterate
    through the ``sequences`` field on the
    corresponding responses.

    All the usual :class:`seqq.api_v1alpha.types.ListSequencesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """
    def __init__(self,
            method: Callable[..., sequence.ListSequencesResponse],
            request: sequence.ListSequencesRequest,
            response: sequence.ListSequencesResponse,
            *,
            metadata: Sequence[Tuple[str, str]] = ()):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (seqq.api_v1alpha.types.ListSequencesRequest):
                The initial request object.
            response (seqq.api_v1alpha.types.ListSequencesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = sequence.ListSequencesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[sequence.ListSequencesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[sequence.Sequence]:
        for page in self.pages:
            yield from page.sequences

    def __repr__(self) -> str:
        return '{0}<{1!r}>'.format(self.__class__.__name__, self._response)


class ListSequencesAsyncPager:
    """A pager for iterating through ``list_sequences`` requests.

    This class thinly wraps an initial
    :class:`seqq.api_v1alpha.types.ListSequencesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``sequences`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListSequences`` requests and continue to iterate
    through the ``sequences`` field on the
    corresponding responses.

    All the usual :class:`seqq.api_v1alpha.types.ListSequencesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """
    def __init__(self,
            method: Callable[..., Awaitable[sequence.ListSequencesResponse]],
            request: sequence.ListSequencesRequest,
            response: sequence.ListSequencesResponse,
            *,
            metadata: Sequence[Tuple[str, str]] = ()):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (seqq.api_v1alpha.types.ListSequencesRequest):
                The initial request object.
            response (seqq.api_v1alpha.types.ListSequencesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = sequence.ListSequencesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[sequence.ListSequencesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response
    def __aiter__(self) -> AsyncIterator[sequence.Sequence]:
        async def async_generator():
            async for page in self.pages:
                for response in page.sequences:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return '{0}<{1!r}>'.format(self.__class__.__name__, self._response)


class ListSearchesPager:
    """A pager for iterating through ``list_searches`` requests.

    This class thinly wraps an initial
    :class:`seqq.api_v1alpha.types.ListSearchesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``searches`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListSearches`` requests and continue to iterate
    through the ``searches`` field on the
    corresponding responses.

    All the usual :class:`seqq.api_v1alpha.types.ListSearchesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """
    def __init__(self,
            method: Callable[..., search.ListSearchesResponse],
            request: search.ListSearchesRequest,
            response: search.ListSearchesResponse,
            *,
            metadata: Sequence[Tuple[str, str]] = ()):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (seqq.api_v1alpha.types.ListSearchesRequest):
                The initial request object.
            response (seqq.api_v1alpha.types.ListSearchesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = search.ListSearchesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[search.ListSearchesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[search.Search]:
        for page in self.pages:
            yield from page.searches

    def __repr__(self) -> str:
        return '{0}<{1!r}>'.format(self.__class__.__name__, self._response)


class ListSearchesAsyncPager:
    """A pager for iterating through ``list_searches`` requests.

    This class thinly wraps an initial
    :class:`seqq.api_v1alpha.types.ListSearchesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``searches`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListSearches`` requests and continue to iterate
    through the ``searches`` field on the
    corresponding responses.

    All the usual :class:`seqq.api_v1alpha.types.ListSearchesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """
    def __init__(self,
            method: Callable[..., Awaitable[search.ListSearchesResponse]],
            request: search.ListSearchesRequest,
            response: search.ListSearchesResponse,
            *,
            metadata: Sequence[Tuple[str, str]] = ()):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (seqq.api_v1alpha.types.ListSearchesRequest):
                The initial request object.
            response (seqq.api_v1alpha.types.ListSearchesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = search.ListSearchesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[search.ListSearchesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response
    def __aiter__(self) -> AsyncIterator[search.Search]:
        async def async_generator():
            async for page in self.pages:
                for response in page.searches:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return '{0}<{1!r}>'.format(self.__class__.__name__, self._response)


class ListIntegrationsPager:
    """A pager for iterating through ``list_integrations`` requests.

    This class thinly wraps an initial
    :class:`seqq.api_v1alpha.types.ListIntegrationsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``integrations`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListIntegrations`` requests and continue to iterate
    through the ``integrations`` field on the
    corresponding responses.

    All the usual :class:`seqq.api_v1alpha.types.ListIntegrationsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """
    def __init__(self,
            method: Callable[..., integration.ListIntegrationsResponse],
            request: integration.ListIntegrationsRequest,
            response: integration.ListIntegrationsResponse,
            *,
            metadata: Sequence[Tuple[str, str]] = ()):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (seqq.api_v1alpha.types.ListIntegrationsRequest):
                The initial request object.
            response (seqq.api_v1alpha.types.ListIntegrationsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = integration.ListIntegrationsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[integration.ListIntegrationsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[integration.Integration]:
        for page in self.pages:
            yield from page.integrations

    def __repr__(self) -> str:
        return '{0}<{1!r}>'.format(self.__class__.__name__, self._response)


class ListIntegrationsAsyncPager:
    """A pager for iterating through ``list_integrations`` requests.

    This class thinly wraps an initial
    :class:`seqq.api_v1alpha.types.ListIntegrationsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``integrations`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListIntegrations`` requests and continue to iterate
    through the ``integrations`` field on the
    corresponding responses.

    All the usual :class:`seqq.api_v1alpha.types.ListIntegrationsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """
    def __init__(self,
            method: Callable[..., Awaitable[integration.ListIntegrationsResponse]],
            request: integration.ListIntegrationsRequest,
            response: integration.ListIntegrationsResponse,
            *,
            metadata: Sequence[Tuple[str, str]] = ()):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (seqq.api_v1alpha.types.ListIntegrationsRequest):
                The initial request object.
            response (seqq.api_v1alpha.types.ListIntegrationsResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = integration.ListIntegrationsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[integration.ListIntegrationsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response
    def __aiter__(self) -> AsyncIterator[integration.Integration]:
        async def async_generator():
            async for page in self.pages:
                for response in page.integrations:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return '{0}<{1!r}>'.format(self.__class__.__name__, self._response)
