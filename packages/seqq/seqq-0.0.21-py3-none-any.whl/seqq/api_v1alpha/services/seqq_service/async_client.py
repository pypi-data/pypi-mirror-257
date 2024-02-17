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
from collections import OrderedDict
import functools
import re
from typing import Dict, Mapping, MutableMapping, MutableSequence, Optional, Sequence, Tuple, Type, Union

from seqq.api_v1alpha import gapic_version as package_version

from google.api_core.client_options import ClientOptions
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry_async as retries
from google.auth import credentials as ga_credentials   # type: ignore
from google.oauth2 import service_account              # type: ignore

try:
    OptionalRetry = Union[retries.AsyncRetry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.AsyncRetry, object, None]  # type: ignore

from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
from seqq.api_v1alpha.services.seqq_service import pagers
from seqq.api_v1alpha.types import collection
from seqq.api_v1alpha.types import collection as sa_collection
from seqq.api_v1alpha.types import integration
from seqq.api_v1alpha.types import integration as sa_integration
from seqq.api_v1alpha.types import search
from seqq.api_v1alpha.types import search as sa_search
from seqq.api_v1alpha.types import sequence
from seqq.api_v1alpha.types import sequence as sa_sequence
from .transports.base import SeqqServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import SeqqServiceGrpcAsyncIOTransport
from .client import SeqqServiceClient


class SeqqServiceAsyncClient:
    """Handles user interactions with the service."""

    _client: SeqqServiceClient

    # Copy defaults from the synchronous client for use here.
    # Note: DEFAULT_ENDPOINT is deprecated. Use _DEFAULT_ENDPOINT_TEMPLATE instead.
    DEFAULT_ENDPOINT = SeqqServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = SeqqServiceClient.DEFAULT_MTLS_ENDPOINT
    _DEFAULT_ENDPOINT_TEMPLATE = SeqqServiceClient._DEFAULT_ENDPOINT_TEMPLATE
    _DEFAULT_UNIVERSE = SeqqServiceClient._DEFAULT_UNIVERSE

    collection_path = staticmethod(SeqqServiceClient.collection_path)
    parse_collection_path = staticmethod(SeqqServiceClient.parse_collection_path)
    integration_path = staticmethod(SeqqServiceClient.integration_path)
    parse_integration_path = staticmethod(SeqqServiceClient.parse_integration_path)
    search_path = staticmethod(SeqqServiceClient.search_path)
    parse_search_path = staticmethod(SeqqServiceClient.parse_search_path)
    sequence_path = staticmethod(SeqqServiceClient.sequence_path)
    parse_sequence_path = staticmethod(SeqqServiceClient.parse_sequence_path)
    common_billing_account_path = staticmethod(SeqqServiceClient.common_billing_account_path)
    parse_common_billing_account_path = staticmethod(SeqqServiceClient.parse_common_billing_account_path)
    common_folder_path = staticmethod(SeqqServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(SeqqServiceClient.parse_common_folder_path)
    common_organization_path = staticmethod(SeqqServiceClient.common_organization_path)
    parse_common_organization_path = staticmethod(SeqqServiceClient.parse_common_organization_path)
    common_project_path = staticmethod(SeqqServiceClient.common_project_path)
    parse_common_project_path = staticmethod(SeqqServiceClient.parse_common_project_path)
    common_location_path = staticmethod(SeqqServiceClient.common_location_path)
    parse_common_location_path = staticmethod(SeqqServiceClient.parse_common_location_path)

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            SeqqServiceAsyncClient: The constructed client.
        """
        return SeqqServiceClient.from_service_account_info.__func__(SeqqServiceAsyncClient, info, *args, **kwargs)  # type: ignore

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            SeqqServiceAsyncClient: The constructed client.
        """
        return SeqqServiceClient.from_service_account_file.__func__(SeqqServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @classmethod
    def get_mtls_endpoint_and_cert_source(cls, client_options: Optional[ClientOptions] = None):
        """Return the API endpoint and client cert source for mutual TLS.

        The client cert source is determined in the following order:
        (1) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is not "true", the
        client cert source is None.
        (2) if `client_options.client_cert_source` is provided, use the provided one; if the
        default client cert source exists, use the default one; otherwise the client cert
        source is None.

        The API endpoint is determined in the following order:
        (1) if `client_options.api_endpoint` if provided, use the provided one.
        (2) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is "always", use the
        default mTLS endpoint; if the environment variable is "never", use the default API
        endpoint; otherwise if client cert source exists, use the default mTLS endpoint, otherwise
        use the default API endpoint.

        More details can be found at https://google.aip.dev/auth/4114.

        Args:
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. Only the `api_endpoint` and `client_cert_source` properties may be used
                in this method.

        Returns:
            Tuple[str, Callable[[], Tuple[bytes, bytes]]]: returns the API endpoint and the
                client cert source to use.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If any errors happen.
        """
        return SeqqServiceClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> SeqqServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            SeqqServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    @property
    def api_endpoint(self):
        """Return the API endpoint used by the client instance.

        Returns:
            str: The API endpoint used by the client instance.
        """
        return self._client._api_endpoint

    @property
    def universe_domain(self) -> str:
        """Return the universe domain used by the client instance.

        Returns:
            str: The universe domain used
                by the client instance.
        """
        return self._client._universe_domain

    get_transport_class = functools.partial(type(SeqqServiceClient).get_transport_class, type(SeqqServiceClient))

    def __init__(self, *,
            credentials: Optional[ga_credentials.Credentials] = None,
            transport: Union[str, SeqqServiceTransport] = "grpc_asyncio",
            client_options: Optional[ClientOptions] = None,
            client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
            ) -> None:
        """Instantiates the seqq service async client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.SeqqServiceTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (Optional[Union[google.api_core.client_options.ClientOptions, dict]]):
                Custom options for the client.

                1. The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client when ``transport`` is
                not explicitly provided. Only if this property is not set and
                ``transport`` was not explicitly provided, the endpoint is
                determined by the GOOGLE_API_USE_MTLS_ENDPOINT environment
                variable, which have one of the following values:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto-switch to the
                default mTLS endpoint if client certificate is present; this is
                the default value).

                2. If the GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide a client certificate for mTLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.

                3. The ``universe_domain`` property can be used to override the
                default "googleapis.com" universe. Note that ``api_endpoint``
                property still takes precedence; and ``universe_domain`` is
                currently not supported for mTLS.

            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        self._client = SeqqServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,

        )

    async def create_collection(self,
            request: Optional[Union[sa_collection.CreateCollectionRequest, dict]] = None,
            *,
            collection: Optional[sa_collection.Collection] = None,
            collection_id: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> sa_collection.Collection:
        r"""Create a Collection.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from seqq import api_v1alpha

            async def sample_create_collection():
                # Create a client
                client = api_v1alpha.SeqqServiceAsyncClient()

                # Initialize request argument(s)
                request = api_v1alpha.CreateCollectionRequest(
                    collection_id="collection_id_value",
                )

                # Make the request
                response = await client.create_collection(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[seqq.api_v1alpha.types.CreateCollectionRequest, dict]]):
                The request object. CreateCollectionRequest is used to
                create a collection.
            collection (:class:`seqq.api_v1alpha.types.Collection`):
                Collection to create. Provide ``collection`` when
                setting ``display_name``.

                This corresponds to the ``collection`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            collection_id (:class:`str`):
                ID of the collection to create. Must
                be unique within the parent project.
                Must be between 3 and 64 characters long
                and can only contain alphanumeric
                characters and hyphens.

                This corresponds to the ``collection_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            seqq.api_v1alpha.types.Collection:
                Collections contain Sequences,
                Searches, and Integration.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([collection, collection_id])
        if request is not None and has_flattened_params:
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        request = sa_collection.CreateCollectionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if collection is not None:
            request.collection = collection
        if collection_id is not None:
            request.collection_id = collection_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_collection,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_collection(self,
            request: Optional[Union[collection.GetCollectionRequest, dict]] = None,
            *,
            name: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> collection.Collection:
        r"""Get a Collection by its name.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from seqq import api_v1alpha

            async def sample_get_collection():
                # Create a client
                client = api_v1alpha.SeqqServiceAsyncClient()

                # Initialize request argument(s)
                request = api_v1alpha.GetCollectionRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_collection(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[seqq.api_v1alpha.types.GetCollectionRequest, dict]]):
                The request object. GetCollectionRequest is the request
                message for GetCollection.
            name (:class:`str`):
                The name of the Collection to retrieve. Format:
                ``collections/{collection_id}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            seqq.api_v1alpha.types.Collection:
                Collections contain Sequences,
                Searches, and Integration.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        request = collection.GetCollectionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_collection,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("name", request.name),
            )),
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def list_collections(self,
            request: Optional[Union[collection.ListCollectionsRequest, dict]] = None,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> pagers.ListCollectionsAsyncPager:
        r"""List Collections.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from seqq import api_v1alpha

            async def sample_list_collections():
                # Create a client
                client = api_v1alpha.SeqqServiceAsyncClient()

                # Initialize request argument(s)
                request = api_v1alpha.ListCollectionsRequest(
                )

                # Make the request
                page_result = client.list_collections(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[seqq.api_v1alpha.types.ListCollectionsRequest, dict]]):
                The request object. ListCollectionsRequest is a request
                to list collections.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            seqq.api_v1alpha.services.seqq_service.pagers.ListCollectionsAsyncPager:
                ListCollectionsResponse is the
                response message for ListCollections.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        request = collection.ListCollectionsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_collections,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListCollectionsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def delete_collection(self,
            request: Optional[Union[collection.DeleteCollectionRequest, dict]] = None,
            *,
            name: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> None:
        r"""Delete a Collection by name.

        This will only delete the Collection if it is empty. To delete a
        Collection and all its child resources, set ``force`` to true.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from seqq import api_v1alpha

            async def sample_delete_collection():
                # Create a client
                client = api_v1alpha.SeqqServiceAsyncClient()

                # Initialize request argument(s)
                request = api_v1alpha.DeleteCollectionRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_collection(request=request)

        Args:
            request (Optional[Union[seqq.api_v1alpha.types.DeleteCollectionRequest, dict]]):
                The request object. DeleteCollectionRequest is the
                request message for DeleteCollection.
            name (:class:`str`):
                The name of the collection to delete. Format:
                ``collections/{collection_id}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        request = collection.DeleteCollectionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_collection,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("name", request.name),
            )),
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def create_sequence(self,
            request: Optional[Union[sa_sequence.CreateSequenceRequest, dict]] = None,
            *,
            collection: Optional[str] = None,
            sequence: Optional[sa_sequence.Sequence] = None,
            sequence_id: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> sa_sequence.Sequence:
        r"""Create a Sequence in a Collection.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from seqq import api_v1alpha

            async def sample_create_sequence():
                # Create a client
                client = api_v1alpha.SeqqServiceAsyncClient()

                # Initialize request argument(s)
                sequence = api_v1alpha.Sequence()
                sequence.sequence = "sequence_value"

                request = api_v1alpha.CreateSequenceRequest(
                    collection="collection_value",
                    sequence_id="sequence_id_value",
                    sequence=sequence,
                )

                # Make the request
                response = await client.create_sequence(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[seqq.api_v1alpha.types.CreateSequenceRequest, dict]]):
                The request object. CreateSequenceRequest is the request
                message for CreateSequence.
            collection (:class:`str`):
                The ``name`` of the Collection to create Sequences in.
                Format: ``collections/{collection_id}``.

                This corresponds to the ``collection`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            sequence (:class:`seqq.api_v1alpha.types.Sequence`):
                The Sequence to create.
                This corresponds to the ``sequence`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            sequence_id (:class:`str`):
                The ID of the Sequence to create.

                This is appended to the Collection name and
                ``/sequences/`` to create the Sequence name.

                For example, if ``collection`` is
                ``collections/my-collection``, and ``sequence_id`` is
                ``my-prefix/my-sequence``, the Sequence name will be
                ``collections/my-collection/sequences/my-prefix/my-sequence``.

                The ``/`` delimiter is encouraged to group Sequences by
                prefix. This is useful in both the UI, where Sequences
                are grouped by folders by ``/``-delimited prefixes, and
                in Searches where a Search can be limited to a subset of
                Sequences by prefix.

                This corresponds to the ``sequence_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            seqq.api_v1alpha.types.Sequence:
                Sequence is a single entry containing
                nucleotides or amino acids and other
                optional metadata like a description,
                creation time, and taxonomy ID.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([collection, sequence, sequence_id])
        if request is not None and has_flattened_params:
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        request = sa_sequence.CreateSequenceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if collection is not None:
            request.collection = collection
        if sequence is not None:
            request.sequence = sequence
        if sequence_id is not None:
            request.sequence_id = sequence_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_sequence,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("collection", request.collection),
            )),
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def batch_create_sequences(self,
            request: Optional[Union[sequence.BatchCreateSequencesRequest, dict]] = None,
            *,
            collection: Optional[str] = None,
            requests: Optional[MutableSequence[sequence.CreateSequenceRequest]] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> sequence.BatchCreateSequencesResponse:
        r"""Create a batch of Sequences in a Collection.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from seqq import api_v1alpha

            async def sample_batch_create_sequences():
                # Create a client
                client = api_v1alpha.SeqqServiceAsyncClient()

                # Initialize request argument(s)
                requests = api_v1alpha.CreateSequenceRequest()
                requests.collection = "collection_value"
                requests.sequence_id = "sequence_id_value"
                requests.sequence.sequence = "sequence_value"

                request = api_v1alpha.BatchCreateSequencesRequest(
                    requests=requests,
                )

                # Make the request
                response = await client.batch_create_sequences(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[seqq.api_v1alpha.types.BatchCreateSequencesRequest, dict]]):
                The request object. BatchCreateSequencesRequest specifies
                how to create a batch of sequences at
                once. Sequences in requests that already
                exist are ignored and not returned in
                the response.
            collection (:class:`str`):
                The ``name`` of the Collection to create Sequences in.
                Format: ``collections/{collection_id}``.

                This corresponds to the ``collection`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            requests (:class:`MutableSequence[seqq.api_v1alpha.types.CreateSequenceRequest]`):
                The request message specifying the
                sequences to create. The maximum length
                is 100.

                This corresponds to the ``requests`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            seqq.api_v1alpha.types.BatchCreateSequencesResponse:
                BatchCreateSequencesResponse is the
                response message for
                BatchCreateSequences.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([collection, requests])
        if request is not None and has_flattened_params:
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        request = sequence.BatchCreateSequencesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if collection is not None:
            request.collection = collection
        if requests:
            request.requests.extend(requests)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.batch_create_sequences,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("collection", request.collection),
            )),
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def create_sequences_from_file(self,
            request: Optional[Union[sequence.CreateSequencesFromFileRequest, dict]] = None,
            *,
            collection: Optional[str] = None,
            contents: Optional[bytes] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> sequence.CreateSequencesFromFileResponse:
        r"""Create Sequences in a Collection by parsing a FASTA
        or GenBank file.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from seqq import api_v1alpha

            async def sample_create_sequences_from_file():
                # Create a client
                client = api_v1alpha.SeqqServiceAsyncClient()

                # Initialize request argument(s)
                request = api_v1alpha.CreateSequencesFromFileRequest(
                    collection="collection_value",
                    encoding="GENBANK",
                    contents=b'contents_blob',
                )

                # Make the request
                response = await client.create_sequences_from_file(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[seqq.api_v1alpha.types.CreateSequencesFromFileRequest, dict]]):
                The request object. CreateSequencesFromFileRequest
                accepts a file and creates sequences
                from it.
            collection (:class:`str`):
                The ``name`` of the Collection to create Sequences in.
                Format: ``collections/{collection_id}``.

                This corresponds to the ``collection`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            contents (:class:`bytes`):
                Content of the file to parse to
                sequences.

                This corresponds to the ``contents`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            seqq.api_v1alpha.types.CreateSequencesFromFileResponse:
                Contains the sequences that were
                created from the file.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([collection, contents])
        if request is not None and has_flattened_params:
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        request = sequence.CreateSequencesFromFileRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if collection is not None:
            request.collection = collection
        if contents is not None:
            request.contents = contents

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_sequences_from_file,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_sequence(self,
            request: Optional[Union[sequence.GetSequenceRequest, dict]] = None,
            *,
            name: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> sequence.Sequence:
        r"""Get a Sequence by name.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from seqq import api_v1alpha

            async def sample_get_sequence():
                # Create a client
                client = api_v1alpha.SeqqServiceAsyncClient()

                # Initialize request argument(s)
                request = api_v1alpha.GetSequenceRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_sequence(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[seqq.api_v1alpha.types.GetSequenceRequest, dict]]):
                The request object. GetSequenceRequest is the request
                message for GetSequence.
            name (:class:`str`):
                The ``name`` of the Sequence to retrieve. Format:
                ``collections/{collection_id}/sequences/{sequence_id}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            seqq.api_v1alpha.types.Sequence:
                Sequence is a single entry containing
                nucleotides or amino acids and other
                optional metadata like a description,
                creation time, and taxonomy ID.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        request = sequence.GetSequenceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_sequence,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("name", request.name),
            )),
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def list_sequences(self,
            request: Optional[Union[sequence.ListSequencesRequest, dict]] = None,
            *,
            collection: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> pagers.ListSequencesAsyncPager:
        r"""List Sequences in a Collection.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from seqq import api_v1alpha

            async def sample_list_sequences():
                # Create a client
                client = api_v1alpha.SeqqServiceAsyncClient()

                # Initialize request argument(s)
                request = api_v1alpha.ListSequencesRequest(
                    collection="collection_value",
                )

                # Make the request
                page_result = client.list_sequences(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[seqq.api_v1alpha.types.ListSequencesRequest, dict]]):
                The request object. ListSequencesRequest is a request to
                list sequences.
            collection (:class:`str`):
                The ``name`` of the Collection to list Sequences from.
                Format: ``collections/{collection_id}``.

                This corresponds to the ``collection`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            seqq.api_v1alpha.services.seqq_service.pagers.ListSequencesAsyncPager:
                ListSequencesResponse is the response
                message for ListSequences.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([collection])
        if request is not None and has_flattened_params:
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        request = sequence.ListSequencesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if collection is not None:
            request.collection = collection

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_sequences,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("collection", request.collection),
            )),
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListSequencesAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def delete_sequence(self,
            request: Optional[Union[sequence.DeleteSequenceRequest, dict]] = None,
            *,
            name: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> None:
        r"""Delete a Sequence by name.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from seqq import api_v1alpha

            async def sample_delete_sequence():
                # Create a client
                client = api_v1alpha.SeqqServiceAsyncClient()

                # Initialize request argument(s)
                request = api_v1alpha.DeleteSequenceRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_sequence(request=request)

        Args:
            request (Optional[Union[seqq.api_v1alpha.types.DeleteSequenceRequest, dict]]):
                The request object. DeleteSequenceRequest is the request
                message for DeleteSequence.
            name (:class:`str`):
                The name of the Sequence to delete. Format:
                ``collections/{collection_id}/sequences/{sequence_id}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        request = sequence.DeleteSequenceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_sequence,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("name", request.name),
            )),
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def start_search(self,
            request: Optional[Union[sa_search.StartSearchRequest, dict]] = None,
            *,
            collection: Optional[str] = None,
            search: Optional[sa_search.Search] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> sa_search.Search:
        r"""Start a Search asynchronously.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from seqq import api_v1alpha

            async def sample_start_search():
                # Create a client
                client = api_v1alpha.SeqqServiceAsyncClient()

                # Initialize request argument(s)
                search = api_v1alpha.Search()
                search.query = "query_value"

                request = api_v1alpha.StartSearchRequest(
                    collection="collection_value",
                    search=search,
                )

                # Make the request
                response = await client.start_search(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[seqq.api_v1alpha.types.StartSearchRequest, dict]]):
                The request object. StartSearchRequest is the request
                message for Search.
            collection (:class:`str`):
                The ``name`` of the Collection to search against. Only
                Sequences in this Collection are queried. Format:
                ``collections/{collection_id}``.

                This corresponds to the ``collection`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            search (:class:`seqq.api_v1alpha.types.Search`):
                The search parameters to use.
                This corresponds to the ``search`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            seqq.api_v1alpha.types.Search:
                A Search of the Sequences in a Collection.

                   On creation, Searches direct seqq to start a query
                   against a Collection using a chosen program. On
                   reads, Searches contain the results of the query,
                   including its current state and any hits.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([collection, search])
        if request is not None and has_flattened_params:
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        request = sa_search.StartSearchRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if collection is not None:
            request.collection = collection
        if search is not None:
            request.search = search

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.start_search,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("collection", request.collection),
            )),
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_search(self,
            request: Optional[Union[search.GetSearchRequest, dict]] = None,
            *,
            name: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> search.Search:
        r"""Get a Search by name.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from seqq import api_v1alpha

            async def sample_get_search():
                # Create a client
                client = api_v1alpha.SeqqServiceAsyncClient()

                # Initialize request argument(s)
                request = api_v1alpha.GetSearchRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_search(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[seqq.api_v1alpha.types.GetSearchRequest, dict]]):
                The request object. GetSearchRequest gets a currently
                ongoing search.
            name (:class:`str`):
                The name of the Search to retrieve. Format:
                ``collections/{collection_id}/searches/{search_id}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            seqq.api_v1alpha.types.Search:
                A Search of the Sequences in a Collection.

                   On creation, Searches direct seqq to start a query
                   against a Collection using a chosen program. On
                   reads, Searches contain the results of the query,
                   including its current state and any hits.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        request = search.GetSearchRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_search,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("name", request.name),
            )),
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def list_searches(self,
            request: Optional[Union[search.ListSearchesRequest, dict]] = None,
            *,
            collection: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> pagers.ListSearchesAsyncPager:
        r"""List Searches in a Collection.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from seqq import api_v1alpha

            async def sample_list_searches():
                # Create a client
                client = api_v1alpha.SeqqServiceAsyncClient()

                # Initialize request argument(s)
                request = api_v1alpha.ListSearchesRequest(
                    collection="collection_value",
                )

                # Make the request
                page_result = client.list_searches(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[seqq.api_v1alpha.types.ListSearchesRequest, dict]]):
                The request object. ListSearchesRequest lists searches.
            collection (:class:`str`):
                The ``name`` of the Collection to list Searches from.
                Format: ``collections/{collection_id}``.

                This corresponds to the ``collection`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            seqq.api_v1alpha.services.seqq_service.pagers.ListSearchesAsyncPager:
                ListSearchesResponse is the response
                message for ListSequences.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([collection])
        if request is not None and has_flattened_params:
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        request = search.ListSearchesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if collection is not None:
            request.collection = collection

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_searches,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("collection", request.collection),
            )),
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListSearchesAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def delete_search(self,
            request: Optional[Union[search.DeleteSearchRequest, dict]] = None,
            *,
            name: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> None:
        r"""Delete a Search by name.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from seqq import api_v1alpha

            async def sample_delete_search():
                # Create a client
                client = api_v1alpha.SeqqServiceAsyncClient()

                # Initialize request argument(s)
                request = api_v1alpha.DeleteSearchRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_search(request=request)

        Args:
            request (Optional[Union[seqq.api_v1alpha.types.DeleteSearchRequest, dict]]):
                The request object. DeleteSearchRequest deletes a search.
            name (:class:`str`):
                The name of the Search to delete. Format:
                ``collections/{collection_id}/searches/{search_id}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        request = search.DeleteSearchRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_search,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("name", request.name),
            )),
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def create_integration(self,
            request: Optional[Union[sa_integration.CreateIntegrationRequest, dict]] = None,
            *,
            collection: Optional[str] = None,
            integration: Optional[sa_integration.Integration] = None,
            integration_id: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> sa_integration.Integration:
        r"""Create an Integration.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from seqq import api_v1alpha

            async def sample_create_integration():
                # Create a client
                client = api_v1alpha.SeqqServiceAsyncClient()

                # Initialize request argument(s)
                integration = api_v1alpha.Integration()
                integration.ncbi.manifest = "manifest_value"
                integration.collection = "collection_value"

                request = api_v1alpha.CreateIntegrationRequest(
                    collection="collection_value",
                    integration=integration,
                )

                # Make the request
                response = await client.create_integration(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[seqq.api_v1alpha.types.CreateIntegrationRequest, dict]]):
                The request object. CreateIntegrationRequest is a request
                to create a new integration.
            collection (:class:`str`):
                The name of the integration to
                create.

                This corresponds to the ``collection`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            integration (:class:`seqq.api_v1alpha.types.Integration`):
                The integration to create.
                This corresponds to the ``integration`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            integration_id (:class:`str`):
                ID of the integration to create.
                This corresponds to the ``integration_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            seqq.api_v1alpha.types.Integration:
                Integrations instruct seqq to import
                Sequences from external sources.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([collection, integration, integration_id])
        if request is not None and has_flattened_params:
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        request = sa_integration.CreateIntegrationRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if collection is not None:
            request.collection = collection
        if integration is not None:
            request.integration = integration
        if integration_id is not None:
            request.integration_id = integration_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_integration,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("collection", request.collection),
            )),
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_integration(self,
            request: Optional[Union[integration.GetIntegrationRequest, dict]] = None,
            *,
            name: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> integration.Integration:
        r"""Get an Integration by name.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from seqq import api_v1alpha

            async def sample_get_integration():
                # Create a client
                client = api_v1alpha.SeqqServiceAsyncClient()

                # Initialize request argument(s)
                request = api_v1alpha.GetIntegrationRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_integration(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[seqq.api_v1alpha.types.GetIntegrationRequest, dict]]):
                The request object. GetIntegrationRequest is the request
                message for getting an integration.
            name (:class:`str`):
                The name of the integration to
                retrieve.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            seqq.api_v1alpha.types.Integration:
                Integrations instruct seqq to import
                Sequences from external sources.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        request = integration.GetIntegrationRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_integration,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("name", request.name),
            )),
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def update_integration(self,
            request: Optional[Union[sa_integration.UpdateIntegrationRequest, dict]] = None,
            *,
            integration: Optional[sa_integration.Integration] = None,
            update_mask: Optional[field_mask_pb2.FieldMask] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> sa_integration.Integration:
        r"""Update an Integration.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from seqq import api_v1alpha

            async def sample_update_integration():
                # Create a client
                client = api_v1alpha.SeqqServiceAsyncClient()

                # Initialize request argument(s)
                integration = api_v1alpha.Integration()
                integration.ncbi.manifest = "manifest_value"
                integration.collection = "collection_value"

                request = api_v1alpha.UpdateIntegrationRequest(
                    integration=integration,
                )

                # Make the request
                response = await client.update_integration(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[seqq.api_v1alpha.types.UpdateIntegrationRequest, dict]]):
                The request object. UpdateIntegrationRequest is a request
                to update an integration.
            integration (:class:`seqq.api_v1alpha.types.Integration`):
                The integration to update.
                This corresponds to the ``integration`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                The list of fields to update.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            seqq.api_v1alpha.types.Integration:
                Integrations instruct seqq to import
                Sequences from external sources.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([integration, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        request = sa_integration.UpdateIntegrationRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if integration is not None:
            request.integration = integration
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_integration,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("integration.name", request.integration.name),
            )),
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def list_integrations(self,
            request: Optional[Union[integration.ListIntegrationsRequest, dict]] = None,
            *,
            collection: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> pagers.ListIntegrationsAsyncPager:
        r"""List Integrations in a Collection.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from seqq import api_v1alpha

            async def sample_list_integrations():
                # Create a client
                client = api_v1alpha.SeqqServiceAsyncClient()

                # Initialize request argument(s)
                request = api_v1alpha.ListIntegrationsRequest(
                    collection="collection_value",
                )

                # Make the request
                page_result = client.list_integrations(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[seqq.api_v1alpha.types.ListIntegrationsRequest, dict]]):
                The request object. ListIntegrationsRequest is a request
                to list integrations.
            collection (:class:`str`):
                The collection collection of the
                integrations to retrieve.

                This corresponds to the ``collection`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            seqq.api_v1alpha.services.seqq_service.pagers.ListIntegrationsAsyncPager:
                ListIntegrationsResponse holds a list
                of integrations.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([collection])
        if request is not None and has_flattened_params:
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        request = integration.ListIntegrationsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if collection is not None:
            request.collection = collection

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_integrations,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("collection", request.collection),
            )),
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListIntegrationsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def delete_integration(self,
            request: Optional[Union[integration.DeleteIntegrationRequest, dict]] = None,
            *,
            name: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> None:
        r"""Delete an Integration by name.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from seqq import api_v1alpha

            async def sample_delete_integration():
                # Create a client
                client = api_v1alpha.SeqqServiceAsyncClient()

                # Initialize request argument(s)
                request = api_v1alpha.DeleteIntegrationRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_integration(request=request)

        Args:
            request (Optional[Union[seqq.api_v1alpha.types.DeleteIntegrationRequest, dict]]):
                The request object. DeleteIntegrationRequest is the
                request message for DeleteIntegration.
            name (:class:`str`):
                The name of the Integration to delete. Format is
                ``collections/{collection_id}/integrations/{integration_id}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        request = integration.DeleteIntegrationRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_integration,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("name", request.name),
            )),
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def __aenter__(self) -> "SeqqServiceAsyncClient":
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(gapic_version=package_version.__version__)


__all__ = (
    "SeqqServiceAsyncClient",
)
