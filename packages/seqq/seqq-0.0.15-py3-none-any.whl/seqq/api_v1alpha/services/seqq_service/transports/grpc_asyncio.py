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
import warnings
from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple, Union

from google.api_core import gapic_v1
from google.api_core import grpc_helpers_async
from google.auth import credentials as ga_credentials   # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc                        # type: ignore
from grpc.experimental import aio  # type: ignore

from google.protobuf import empty_pb2  # type: ignore
from seqq.api_v1alpha.types import collection
from seqq.api_v1alpha.types import collection as sa_collection
from seqq.api_v1alpha.types import integration
from seqq.api_v1alpha.types import integration as sa_integration
from seqq.api_v1alpha.types import search
from seqq.api_v1alpha.types import search as sa_search
from seqq.api_v1alpha.types import sequence
from seqq.api_v1alpha.types import sequence as sa_sequence
from .base import SeqqServiceTransport, DEFAULT_CLIENT_INFO
from .grpc import SeqqServiceGrpcTransport


class SeqqServiceGrpcAsyncIOTransport(SeqqServiceTransport):
    """gRPC AsyncIO backend transport for SeqqService.

    Handles user interactions with the service.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _grpc_channel: aio.Channel
    _stubs: Dict[str, Callable] = {}

    @classmethod
    def create_channel(cls,
                       host: str = 'api.seqq.io',
                       credentials: Optional[ga_credentials.Credentials] = None,
                       credentials_file: Optional[str] = None,
                       scopes: Optional[Sequence[str]] = None,
                       quota_project_id: Optional[str] = None,
                       **kwargs) -> aio.Channel:
        """Create and return a gRPC AsyncIO channel object.
        Args:
            host (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            aio.Channel: A gRPC AsyncIO channel object.
        """

        return grpc_helpers_async.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            quota_project_id=quota_project_id,
            default_scopes=cls.AUTH_SCOPES,
            scopes=scopes,
            default_host=cls.DEFAULT_HOST,
            **kwargs
        )

    def __init__(self, *,
            host: str = 'api.seqq.io',
            credentials: Optional[ga_credentials.Credentials] = None,
            credentials_file: Optional[str] = None,
            scopes: Optional[Sequence[str]] = None,
            channel: Optional[aio.Channel] = None,
            api_mtls_endpoint: Optional[str] = None,
            client_cert_source: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
            ssl_channel_credentials: Optional[grpc.ChannelCredentials] = None,
            client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
            quota_project_id: Optional[str] = None,
            client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
            always_use_jwt_access: Optional[bool] = False,
            api_audience: Optional[str] = None,
            ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'api.seqq.io').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if ``channel`` is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            channel (Optional[aio.Channel]): A ``Channel`` instance through
                which to make calls.
            api_mtls_endpoint (Optional[str]): Deprecated. The mutual TLS endpoint.
                If provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or application default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for the grpc channel. It is ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure a mutual TLS channel. It is
                ignored if ``channel`` or ``ssl_channel_credentials`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._grpc_channel = None
        self._ssl_channel_credentials = ssl_channel_credentials
        self._stubs: Dict[str, Callable] = {}

        if api_mtls_endpoint:
            warnings.warn("api_mtls_endpoint is deprecated", DeprecationWarning)
        if client_cert_source:
            warnings.warn("client_cert_source is deprecated", DeprecationWarning)

        if channel:
            # Ignore credentials if a channel was passed.
            credentials = False
            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
            self._ssl_channel_credentials = None
        else:
            if api_mtls_endpoint:
                host = api_mtls_endpoint

                # Create SSL credentials with client_cert_source or application
                # default SSL credentials.
                if client_cert_source:
                    cert, key = client_cert_source()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )
                else:
                    self._ssl_channel_credentials = SslCredentials().ssl_credentials

            else:
                if client_cert_source_for_mtls and not ssl_channel_credentials:
                    cert, key = client_cert_source_for_mtls()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )

        # The base transport sets the host, credentials and scopes
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            api_audience=api_audience,
        )

        if not self._grpc_channel:
            self._grpc_channel = type(self).create_channel(
                self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                # Set ``credentials_file`` to ``None`` here as
                # the credentials that we saved earlier should be used.
                credentials_file=None,
                scopes=self._scopes,
                ssl_credentials=self._ssl_channel_credentials,
                quota_project_id=quota_project_id,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )

        # Wrap messages. This must be done after self._grpc_channel exists
        self._prep_wrapped_messages(client_info)

    @property
    def grpc_channel(self) -> aio.Channel:
        """Create the channel designed to connect to this service.

        This property caches on the instance; repeated calls return
        the same channel.
        """
        # Return the channel from cache.
        return self._grpc_channel

    @property
    def create_collection(self) -> Callable[
            [sa_collection.CreateCollectionRequest],
            Awaitable[sa_collection.Collection]]:
        r"""Return a callable for the create collection method over gRPC.

        Create a Collection.

        Returns:
            Callable[[~.CreateCollectionRequest],
                    Awaitable[~.Collection]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'create_collection' not in self._stubs:
            self._stubs['create_collection'] = self.grpc_channel.unary_unary(
                '/seqq.api.v1alpha.SeqqService/CreateCollection',
                request_serializer=sa_collection.CreateCollectionRequest.serialize,
                response_deserializer=sa_collection.Collection.deserialize,
            )
        return self._stubs['create_collection']

    @property
    def get_collection(self) -> Callable[
            [collection.GetCollectionRequest],
            Awaitable[collection.Collection]]:
        r"""Return a callable for the get collection method over gRPC.

        Get a Collection by its name.

        Returns:
            Callable[[~.GetCollectionRequest],
                    Awaitable[~.Collection]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'get_collection' not in self._stubs:
            self._stubs['get_collection'] = self.grpc_channel.unary_unary(
                '/seqq.api.v1alpha.SeqqService/GetCollection',
                request_serializer=collection.GetCollectionRequest.serialize,
                response_deserializer=collection.Collection.deserialize,
            )
        return self._stubs['get_collection']

    @property
    def list_collections(self) -> Callable[
            [collection.ListCollectionsRequest],
            Awaitable[collection.ListCollectionsResponse]]:
        r"""Return a callable for the list collections method over gRPC.

        List Collections.

        Returns:
            Callable[[~.ListCollectionsRequest],
                    Awaitable[~.ListCollectionsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'list_collections' not in self._stubs:
            self._stubs['list_collections'] = self.grpc_channel.unary_unary(
                '/seqq.api.v1alpha.SeqqService/ListCollections',
                request_serializer=collection.ListCollectionsRequest.serialize,
                response_deserializer=collection.ListCollectionsResponse.deserialize,
            )
        return self._stubs['list_collections']

    @property
    def delete_collection(self) -> Callable[
            [collection.DeleteCollectionRequest],
            Awaitable[empty_pb2.Empty]]:
        r"""Return a callable for the delete collection method over gRPC.

        Delete a Collection by name.

        This will only delete the Collection if it is empty. To delete a
        Collection and all its child resources, set ``force`` to true.

        Returns:
            Callable[[~.DeleteCollectionRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'delete_collection' not in self._stubs:
            self._stubs['delete_collection'] = self.grpc_channel.unary_unary(
                '/seqq.api.v1alpha.SeqqService/DeleteCollection',
                request_serializer=collection.DeleteCollectionRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs['delete_collection']

    @property
    def create_sequence(self) -> Callable[
            [sa_sequence.CreateSequenceRequest],
            Awaitable[sa_sequence.Sequence]]:
        r"""Return a callable for the create sequence method over gRPC.

        Create a Sequence in a Collection.

        Returns:
            Callable[[~.CreateSequenceRequest],
                    Awaitable[~.Sequence]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'create_sequence' not in self._stubs:
            self._stubs['create_sequence'] = self.grpc_channel.unary_unary(
                '/seqq.api.v1alpha.SeqqService/CreateSequence',
                request_serializer=sa_sequence.CreateSequenceRequest.serialize,
                response_deserializer=sa_sequence.Sequence.deserialize,
            )
        return self._stubs['create_sequence']

    @property
    def batch_create_sequences(self) -> Callable[
            [sequence.BatchCreateSequencesRequest],
            Awaitable[sequence.BatchCreateSequencesResponse]]:
        r"""Return a callable for the batch create sequences method over gRPC.

        Create a batch of Sequences in a Collection.

        Returns:
            Callable[[~.BatchCreateSequencesRequest],
                    Awaitable[~.BatchCreateSequencesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'batch_create_sequences' not in self._stubs:
            self._stubs['batch_create_sequences'] = self.grpc_channel.unary_unary(
                '/seqq.api.v1alpha.SeqqService/BatchCreateSequences',
                request_serializer=sequence.BatchCreateSequencesRequest.serialize,
                response_deserializer=sequence.BatchCreateSequencesResponse.deserialize,
            )
        return self._stubs['batch_create_sequences']

    @property
    def create_sequences_from_file(self) -> Callable[
            [sequence.CreateSequencesFromFileRequest],
            Awaitable[sequence.CreateSequencesFromFileResponse]]:
        r"""Return a callable for the create sequences from file method over gRPC.

        Create Sequences in a Collection by parsing a FASTA
        or GenBank file.

        Returns:
            Callable[[~.CreateSequencesFromFileRequest],
                    Awaitable[~.CreateSequencesFromFileResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'create_sequences_from_file' not in self._stubs:
            self._stubs['create_sequences_from_file'] = self.grpc_channel.unary_unary(
                '/seqq.api.v1alpha.SeqqService/CreateSequencesFromFile',
                request_serializer=sequence.CreateSequencesFromFileRequest.serialize,
                response_deserializer=sequence.CreateSequencesFromFileResponse.deserialize,
            )
        return self._stubs['create_sequences_from_file']

    @property
    def get_sequence(self) -> Callable[
            [sequence.GetSequenceRequest],
            Awaitable[sequence.Sequence]]:
        r"""Return a callable for the get sequence method over gRPC.

        Get a Sequence by name.

        Returns:
            Callable[[~.GetSequenceRequest],
                    Awaitable[~.Sequence]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'get_sequence' not in self._stubs:
            self._stubs['get_sequence'] = self.grpc_channel.unary_unary(
                '/seqq.api.v1alpha.SeqqService/GetSequence',
                request_serializer=sequence.GetSequenceRequest.serialize,
                response_deserializer=sequence.Sequence.deserialize,
            )
        return self._stubs['get_sequence']

    @property
    def list_sequences(self) -> Callable[
            [sequence.ListSequencesRequest],
            Awaitable[sequence.ListSequencesResponse]]:
        r"""Return a callable for the list sequences method over gRPC.

        List Sequences in a Collection.

        Returns:
            Callable[[~.ListSequencesRequest],
                    Awaitable[~.ListSequencesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'list_sequences' not in self._stubs:
            self._stubs['list_sequences'] = self.grpc_channel.unary_unary(
                '/seqq.api.v1alpha.SeqqService/ListSequences',
                request_serializer=sequence.ListSequencesRequest.serialize,
                response_deserializer=sequence.ListSequencesResponse.deserialize,
            )
        return self._stubs['list_sequences']

    @property
    def delete_sequence(self) -> Callable[
            [sequence.DeleteSequenceRequest],
            Awaitable[empty_pb2.Empty]]:
        r"""Return a callable for the delete sequence method over gRPC.

        Delete a Sequence by name.

        Returns:
            Callable[[~.DeleteSequenceRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'delete_sequence' not in self._stubs:
            self._stubs['delete_sequence'] = self.grpc_channel.unary_unary(
                '/seqq.api.v1alpha.SeqqService/DeleteSequence',
                request_serializer=sequence.DeleteSequenceRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs['delete_sequence']

    @property
    def start_search(self) -> Callable[
            [sa_search.StartSearchRequest],
            Awaitable[sa_search.Search]]:
        r"""Return a callable for the start search method over gRPC.

        Start a Search asynchronously.

        Returns:
            Callable[[~.StartSearchRequest],
                    Awaitable[~.Search]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'start_search' not in self._stubs:
            self._stubs['start_search'] = self.grpc_channel.unary_unary(
                '/seqq.api.v1alpha.SeqqService/StartSearch',
                request_serializer=sa_search.StartSearchRequest.serialize,
                response_deserializer=sa_search.Search.deserialize,
            )
        return self._stubs['start_search']

    @property
    def get_search(self) -> Callable[
            [search.GetSearchRequest],
            Awaitable[search.Search]]:
        r"""Return a callable for the get search method over gRPC.

        Get a Search by name.

        Returns:
            Callable[[~.GetSearchRequest],
                    Awaitable[~.Search]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'get_search' not in self._stubs:
            self._stubs['get_search'] = self.grpc_channel.unary_unary(
                '/seqq.api.v1alpha.SeqqService/GetSearch',
                request_serializer=search.GetSearchRequest.serialize,
                response_deserializer=search.Search.deserialize,
            )
        return self._stubs['get_search']

    @property
    def list_searches(self) -> Callable[
            [search.ListSearchesRequest],
            Awaitable[search.ListSearchesResponse]]:
        r"""Return a callable for the list searches method over gRPC.

        List Searches in a Collection.

        Returns:
            Callable[[~.ListSearchesRequest],
                    Awaitable[~.ListSearchesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'list_searches' not in self._stubs:
            self._stubs['list_searches'] = self.grpc_channel.unary_unary(
                '/seqq.api.v1alpha.SeqqService/ListSearches',
                request_serializer=search.ListSearchesRequest.serialize,
                response_deserializer=search.ListSearchesResponse.deserialize,
            )
        return self._stubs['list_searches']

    @property
    def delete_search(self) -> Callable[
            [search.DeleteSearchRequest],
            Awaitable[empty_pb2.Empty]]:
        r"""Return a callable for the delete search method over gRPC.

        Delete a Search by name.

        Returns:
            Callable[[~.DeleteSearchRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'delete_search' not in self._stubs:
            self._stubs['delete_search'] = self.grpc_channel.unary_unary(
                '/seqq.api.v1alpha.SeqqService/DeleteSearch',
                request_serializer=search.DeleteSearchRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs['delete_search']

    @property
    def create_integration(self) -> Callable[
            [sa_integration.CreateIntegrationRequest],
            Awaitable[sa_integration.Integration]]:
        r"""Return a callable for the create integration method over gRPC.

        Create an Integration.

        Returns:
            Callable[[~.CreateIntegrationRequest],
                    Awaitable[~.Integration]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'create_integration' not in self._stubs:
            self._stubs['create_integration'] = self.grpc_channel.unary_unary(
                '/seqq.api.v1alpha.SeqqService/CreateIntegration',
                request_serializer=sa_integration.CreateIntegrationRequest.serialize,
                response_deserializer=sa_integration.Integration.deserialize,
            )
        return self._stubs['create_integration']

    @property
    def get_integration(self) -> Callable[
            [integration.GetIntegrationRequest],
            Awaitable[integration.Integration]]:
        r"""Return a callable for the get integration method over gRPC.

        Get an Integration by name.

        Returns:
            Callable[[~.GetIntegrationRequest],
                    Awaitable[~.Integration]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'get_integration' not in self._stubs:
            self._stubs['get_integration'] = self.grpc_channel.unary_unary(
                '/seqq.api.v1alpha.SeqqService/GetIntegration',
                request_serializer=integration.GetIntegrationRequest.serialize,
                response_deserializer=integration.Integration.deserialize,
            )
        return self._stubs['get_integration']

    @property
    def update_integration(self) -> Callable[
            [sa_integration.UpdateIntegrationRequest],
            Awaitable[sa_integration.Integration]]:
        r"""Return a callable for the update integration method over gRPC.

        Update an Integration.

        Returns:
            Callable[[~.UpdateIntegrationRequest],
                    Awaitable[~.Integration]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'update_integration' not in self._stubs:
            self._stubs['update_integration'] = self.grpc_channel.unary_unary(
                '/seqq.api.v1alpha.SeqqService/UpdateIntegration',
                request_serializer=sa_integration.UpdateIntegrationRequest.serialize,
                response_deserializer=sa_integration.Integration.deserialize,
            )
        return self._stubs['update_integration']

    @property
    def list_integrations(self) -> Callable[
            [integration.ListIntegrationsRequest],
            Awaitable[integration.ListIntegrationsResponse]]:
        r"""Return a callable for the list integrations method over gRPC.

        List Integrations in a Collection.

        Returns:
            Callable[[~.ListIntegrationsRequest],
                    Awaitable[~.ListIntegrationsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'list_integrations' not in self._stubs:
            self._stubs['list_integrations'] = self.grpc_channel.unary_unary(
                '/seqq.api.v1alpha.SeqqService/ListIntegrations',
                request_serializer=integration.ListIntegrationsRequest.serialize,
                response_deserializer=integration.ListIntegrationsResponse.deserialize,
            )
        return self._stubs['list_integrations']

    @property
    def delete_integration(self) -> Callable[
            [integration.DeleteIntegrationRequest],
            Awaitable[empty_pb2.Empty]]:
        r"""Return a callable for the delete integration method over gRPC.

        Delete an Integration by name.

        Returns:
            Callable[[~.DeleteIntegrationRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'delete_integration' not in self._stubs:
            self._stubs['delete_integration'] = self.grpc_channel.unary_unary(
                '/seqq.api.v1alpha.SeqqService/DeleteIntegration',
                request_serializer=integration.DeleteIntegrationRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs['delete_integration']

    def close(self):
        return self.grpc_channel.close()


__all__ = (
    'SeqqServiceGrpcAsyncIOTransport',
)
