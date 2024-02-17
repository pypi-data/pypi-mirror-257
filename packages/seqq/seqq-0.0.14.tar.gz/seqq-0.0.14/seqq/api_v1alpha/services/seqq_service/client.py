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
import os
import re
from typing import Dict, Mapping, MutableMapping, MutableSequence, Optional, Sequence, Tuple, Type, Union, cast
import warnings

from seqq.api_v1alpha import gapic_version as package_version

from google.api_core import client_options as client_options_lib
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials             # type: ignore
from google.auth.transport import mtls                            # type: ignore
from google.auth.transport.grpc import SslCredentials             # type: ignore
from google.auth.exceptions import MutualTLSChannelError          # type: ignore
from google.oauth2 import service_account                         # type: ignore

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore

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
from .transports.grpc import SeqqServiceGrpcTransport
from .transports.grpc_asyncio import SeqqServiceGrpcAsyncIOTransport


class SeqqServiceClientMeta(type):
    """Metaclass for the SeqqService client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """
    _transport_registry = OrderedDict()  # type: Dict[str, Type[SeqqServiceTransport]]
    _transport_registry["grpc"] = SeqqServiceGrpcTransport
    _transport_registry["grpc_asyncio"] = SeqqServiceGrpcAsyncIOTransport

    def get_transport_class(cls,
            label: Optional[str] = None,
        ) -> Type[SeqqServiceTransport]:
        """Returns an appropriate transport class.

        Args:
            label: The name of the desired transport. If none is
                provided, then the first transport in the registry is used.

        Returns:
            The transport class to use.
        """
        # If a specific transport is requested, return that one.
        if label:
            return cls._transport_registry[label]

        # No transport is requested; return the default (that is, the first one
        # in the dictionary).
        return next(iter(cls._transport_registry.values()))


class SeqqServiceClient(metaclass=SeqqServiceClientMeta):
    """Handles user interactions with the service."""

    @staticmethod
    def _get_default_mtls_endpoint(api_endpoint):
        """Converts api endpoint to mTLS endpoint.

        Convert "*.sandbox.googleapis.com" and "*.googleapis.com" to
        "*.mtls.sandbox.googleapis.com" and "*.mtls.googleapis.com" respectively.
        Args:
            api_endpoint (Optional[str]): the api endpoint to convert.
        Returns:
            str: converted mTLS api endpoint.
        """
        if not api_endpoint:
            return api_endpoint

        mtls_endpoint_re = re.compile(
            r"(?P<name>[^.]+)(?P<mtls>\.mtls)?(?P<sandbox>\.sandbox)?(?P<googledomain>\.googleapis\.com)?"
        )

        m = mtls_endpoint_re.match(api_endpoint)
        name, mtls, sandbox, googledomain = m.groups()
        if mtls or not googledomain:
            return api_endpoint

        if sandbox:
            return api_endpoint.replace(
                "sandbox.googleapis.com", "mtls.sandbox.googleapis.com"
            )

        return api_endpoint.replace(".googleapis.com", ".mtls.googleapis.com")

    # Note: DEFAULT_ENDPOINT is deprecated. Use _DEFAULT_ENDPOINT_TEMPLATE instead.
    DEFAULT_ENDPOINT = "api.seqq.io"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

    _DEFAULT_ENDPOINT_TEMPLATE = "api.seqq.io"
    _DEFAULT_UNIVERSE = "googleapis.com"

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            SeqqServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_info(info)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

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
            SeqqServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(
            filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> SeqqServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            SeqqServiceTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def collection_path(collection: str,) -> str:
        """Returns a fully-qualified collection string."""
        return "collections/{collection}".format(collection=collection, )

    @staticmethod
    def parse_collection_path(path: str) -> Dict[str,str]:
        """Parses a collection path into its component segments."""
        m = re.match(r"^collections/(?P<collection>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def integration_path(collection: str,integration: str,) -> str:
        """Returns a fully-qualified integration string."""
        return "collections/{collection}/integrations/{integration}".format(collection=collection, integration=integration, )

    @staticmethod
    def parse_integration_path(path: str) -> Dict[str,str]:
        """Parses a integration path into its component segments."""
        m = re.match(r"^collections/(?P<collection>.+?)/integrations/(?P<integration>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def search_path(collection: str,search: str,) -> str:
        """Returns a fully-qualified search string."""
        return "collections/{collection}/searches/{search}".format(collection=collection, search=search, )

    @staticmethod
    def parse_search_path(path: str) -> Dict[str,str]:
        """Parses a search path into its component segments."""
        m = re.match(r"^collections/(?P<collection>.+?)/searches/(?P<search>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def sequence_path(collection: str,sequence: str,) -> str:
        """Returns a fully-qualified sequence string."""
        return "collections/{collection}/sequences/{sequence}".format(collection=collection, sequence=sequence, )

    @staticmethod
    def parse_sequence_path(path: str) -> Dict[str,str]:
        """Parses a sequence path into its component segments."""
        m = re.match(r"^collections/(?P<collection>.+?)/sequences/(?P<sequence>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_billing_account_path(billing_account: str, ) -> str:
        """Returns a fully-qualified billing_account string."""
        return "billingAccounts/{billing_account}".format(billing_account=billing_account, )

    @staticmethod
    def parse_common_billing_account_path(path: str) -> Dict[str,str]:
        """Parse a billing_account path into its component segments."""
        m = re.match(r"^billingAccounts/(?P<billing_account>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_folder_path(folder: str, ) -> str:
        """Returns a fully-qualified folder string."""
        return "folders/{folder}".format(folder=folder, )

    @staticmethod
    def parse_common_folder_path(path: str) -> Dict[str,str]:
        """Parse a folder path into its component segments."""
        m = re.match(r"^folders/(?P<folder>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_organization_path(organization: str, ) -> str:
        """Returns a fully-qualified organization string."""
        return "organizations/{organization}".format(organization=organization, )

    @staticmethod
    def parse_common_organization_path(path: str) -> Dict[str,str]:
        """Parse a organization path into its component segments."""
        m = re.match(r"^organizations/(?P<organization>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_project_path(project: str, ) -> str:
        """Returns a fully-qualified project string."""
        return "projects/{project}".format(project=project, )

    @staticmethod
    def parse_common_project_path(path: str) -> Dict[str,str]:
        """Parse a project path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_location_path(project: str, location: str, ) -> str:
        """Returns a fully-qualified location string."""
        return "projects/{project}/locations/{location}".format(project=project, location=location, )

    @staticmethod
    def parse_common_location_path(path: str) -> Dict[str,str]:
        """Parse a location path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)$", path)
        return m.groupdict() if m else {}

    @classmethod
    def get_mtls_endpoint_and_cert_source(cls, client_options: Optional[client_options_lib.ClientOptions] = None):
        """Deprecated. Return the API endpoint and client cert source for mutual TLS.

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

        warnings.warn("get_mtls_endpoint_and_cert_source is deprecated. Use the api_endpoint property instead.",
            DeprecationWarning)
        if client_options is None:
            client_options = client_options_lib.ClientOptions()
        use_client_cert = os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false")
        use_mtls_endpoint = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto")
        if use_client_cert not in ("true", "false"):
            raise ValueError("Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`")
        if use_mtls_endpoint not in ("auto", "never", "always"):
            raise MutualTLSChannelError("Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`")

        # Figure out the client cert source to use.
        client_cert_source = None
        if use_client_cert == "true":
            if client_options.client_cert_source:
                client_cert_source = client_options.client_cert_source
            elif mtls.has_default_client_cert_source():
                client_cert_source = mtls.default_client_cert_source()

        # Figure out which api endpoint to use.
        if client_options.api_endpoint is not None:
            api_endpoint = client_options.api_endpoint
        elif use_mtls_endpoint == "always" or (use_mtls_endpoint == "auto" and client_cert_source):
            api_endpoint = cls.DEFAULT_MTLS_ENDPOINT
        else:
            api_endpoint = cls.DEFAULT_ENDPOINT

        return api_endpoint, client_cert_source

    @staticmethod
    def _read_environment_variables():
        """Returns the environment variables used by the client.

        Returns:
            Tuple[bool, str, str]: returns the GOOGLE_API_USE_CLIENT_CERTIFICATE,
            GOOGLE_API_USE_MTLS_ENDPOINT, and GOOGLE_CLOUD_UNIVERSE_DOMAIN environment variables.

        Raises:
            ValueError: If GOOGLE_API_USE_CLIENT_CERTIFICATE is not
                any of ["true", "false"].
            google.auth.exceptions.MutualTLSChannelError: If GOOGLE_API_USE_MTLS_ENDPOINT
                is not any of ["auto", "never", "always"].
        """
        use_client_cert = os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false").lower()
        use_mtls_endpoint = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto").lower()
        universe_domain_env = os.getenv("GOOGLE_CLOUD_UNIVERSE_DOMAIN")
        if use_client_cert not in ("true", "false"):
            raise ValueError("Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`")
        if use_mtls_endpoint not in ("auto", "never", "always"):
            raise MutualTLSChannelError("Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`")
        return use_client_cert == "true", use_mtls_endpoint, universe_domain_env

    @staticmethod
    def _get_client_cert_source(provided_cert_source, use_cert_flag):
        """Return the client cert source to be used by the client.

        Args:
            provided_cert_source (bytes): The client certificate source provided.
            use_cert_flag (bool): A flag indicating whether to use the client certificate.

        Returns:
            bytes or None: The client cert source to be used by the client.
        """
        client_cert_source = None
        if use_cert_flag:
            if provided_cert_source:
                client_cert_source = provided_cert_source
            elif mtls.has_default_client_cert_source():
                client_cert_source = mtls.default_client_cert_source()
        return client_cert_source

    @staticmethod
    def _get_api_endpoint(api_override, client_cert_source, universe_domain, use_mtls_endpoint):
        """Return the API endpoint used by the client.

        Args:
            api_override (str): The API endpoint override. If specified, this is always
                the return value of this function and the other arguments are not used.
            client_cert_source (bytes): The client certificate source used by the client.
            universe_domain (str): The universe domain used by the client.
            use_mtls_endpoint (str): How to use the mTLS endpoint, which depends also on the other parameters.
                Possible values are "always", "auto", or "never".

        Returns:
            str: The API endpoint to be used by the client.
        """
        if api_override is not None:
            api_endpoint = api_override
        elif use_mtls_endpoint == "always" or (use_mtls_endpoint == "auto" and client_cert_source):
            _default_universe = SeqqServiceClient._DEFAULT_UNIVERSE
            if universe_domain != _default_universe:
                raise MutualTLSChannelError(f"mTLS is not supported in any universe other than {_default_universe}.")
            api_endpoint = SeqqServiceClient.DEFAULT_MTLS_ENDPOINT
        else:
            api_endpoint = SeqqServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(UNIVERSE_DOMAIN=universe_domain)
        return api_endpoint

    @staticmethod
    def _get_universe_domain(client_universe_domain: Optional[str], universe_domain_env: Optional[str]) -> str:
        """Return the universe domain used by the client.

        Args:
            client_universe_domain (Optional[str]): The universe domain configured via the client options.
            universe_domain_env (Optional[str]): The universe domain configured via the "GOOGLE_CLOUD_UNIVERSE_DOMAIN" environment variable.

        Returns:
            str: The universe domain to be used by the client.

        Raises:
            ValueError: If the universe domain is an empty string.
        """
        universe_domain = SeqqServiceClient._DEFAULT_UNIVERSE
        if client_universe_domain is not None:
            universe_domain = client_universe_domain
        elif universe_domain_env is not None:
            universe_domain = universe_domain_env
        if len(universe_domain.strip()) == 0:
            raise ValueError("Universe Domain cannot be an empty string.")
        return universe_domain

    @staticmethod
    def _compare_universes(client_universe: str,
                           credentials: ga_credentials.Credentials) -> bool:
        """Returns True iff the universe domains used by the client and credentials match.

        Args:
            client_universe (str): The universe domain configured via the client options.
            credentials (ga_credentials.Credentials): The credentials being used in the client.

        Returns:
            bool: True iff client_universe matches the universe in credentials.

        Raises:
            ValueError: when client_universe does not match the universe in credentials.
        """

        default_universe = SeqqServiceClient._DEFAULT_UNIVERSE
        credentials_universe = getattr(credentials, "universe_domain", default_universe)

        if client_universe != credentials_universe:
            raise ValueError("The configured universe domain "
                f"({client_universe}) does not match the universe domain "
                f"found in the credentials ({credentials_universe}). "
                "If you haven't configured the universe domain explicitly, "
                f"`{default_universe}` is the default.")
        return True

    def _validate_universe_domain(self):
        """Validates client's and credentials' universe domains are consistent.

        Returns:
            bool: True iff the configured universe domain is valid.

        Raises:
            ValueError: If the configured universe domain is not valid.
        """
        self._is_universe_domain_valid = (self._is_universe_domain_valid or
            SeqqServiceClient._compare_universes(self.universe_domain, self.transport._credentials))
        return self._is_universe_domain_valid

    @property
    def api_endpoint(self):
        """Return the API endpoint used by the client instance.

        Returns:
            str: The API endpoint used by the client instance.
        """
        return self._api_endpoint

    @property
    def universe_domain(self) -> str:
        """Return the universe domain used by the client instance.

        Returns:
            str: The universe domain used by the client instance.
        """
        return self._universe_domain

    def __init__(self, *,
            credentials: Optional[ga_credentials.Credentials] = None,
            transport: Optional[Union[str, SeqqServiceTransport]] = None,
            client_options: Optional[Union[client_options_lib.ClientOptions, dict]] = None,
            client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
            ) -> None:
        """Instantiates the seqq service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, SeqqServiceTransport]): The
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
                default "googleapis.com" universe. Note that the ``api_endpoint``
                property still takes precedence; and ``universe_domain`` is
                currently not supported for mTLS.

            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        self._client_options = client_options
        if isinstance(self._client_options, dict):
            self._client_options = client_options_lib.from_dict(self._client_options)
        if self._client_options is None:
            self._client_options = client_options_lib.ClientOptions()
        self._client_options = cast(client_options_lib.ClientOptions, self._client_options)

        universe_domain_opt = getattr(self._client_options, 'universe_domain', None)

        self._use_client_cert, self._use_mtls_endpoint, self._universe_domain_env = SeqqServiceClient._read_environment_variables()
        self._client_cert_source = SeqqServiceClient._get_client_cert_source(self._client_options.client_cert_source, self._use_client_cert)
        self._universe_domain = SeqqServiceClient._get_universe_domain(universe_domain_opt, self._universe_domain_env)
        self._api_endpoint = None # updated below, depending on `transport`

        # Initialize the universe domain validation.
        self._is_universe_domain_valid = False

        api_key_value = getattr(self._client_options, "api_key", None)
        if api_key_value and credentials:
            raise ValueError("client_options.api_key and credentials are mutually exclusive")

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        transport_provided = isinstance(transport, SeqqServiceTransport)
        if transport_provided:
            # transport is a SeqqServiceTransport instance.
            if credentials or self._client_options.credentials_file or api_key_value:
                raise ValueError("When providing a transport instance, "
                                 "provide its credentials directly.")
            if self._client_options.scopes:
                raise ValueError(
                    "When providing a transport instance, provide its scopes "
                    "directly."
                )
            self._transport = cast(SeqqServiceTransport, transport)
            self._api_endpoint = self._transport.host

        self._api_endpoint = (self._api_endpoint or
            SeqqServiceClient._get_api_endpoint(
                self._client_options.api_endpoint,
                self._client_cert_source,
                self._universe_domain,
                self._use_mtls_endpoint))

        if not transport_provided:
            import google.auth._default  # type: ignore

            if api_key_value and hasattr(google.auth._default, "get_api_key_credentials"):
                credentials = google.auth._default.get_api_key_credentials(api_key_value)

            Transport = type(self).get_transport_class(cast(str, transport))
            self._transport = Transport(
                credentials=credentials,
                credentials_file=self._client_options.credentials_file,
                host=self._api_endpoint,
                scopes=self._client_options.scopes,
                client_cert_source_for_mtls=self._client_cert_source,
                quota_project_id=self._client_options.quota_project_id,
                client_info=client_info,
                always_use_jwt_access=True,
                api_audience=self._client_options.api_audience,
            )

    def create_collection(self,
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

            def sample_create_collection():
                # Create a client
                client = api_v1alpha.SeqqServiceClient()

                # Initialize request argument(s)
                request = api_v1alpha.CreateCollectionRequest(
                    collection_id="collection_id_value",
                )

                # Make the request
                response = client.create_collection(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[seqq.api_v1alpha.types.CreateCollectionRequest, dict]):
                The request object. CreateCollectionRequest is used to
                create a collection.
            collection (seqq.api_v1alpha.types.Collection):
                Collection to create. Provide ``collection`` when
                setting ``display_name``.

                This corresponds to the ``collection`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            collection_id (str):
                ID of the collection to create. Must
                be unique within the parent project.
                Must be between 3 and 64 characters long
                and can only contain alphanumeric
                characters and hyphens.

                This corresponds to the ``collection_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
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
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # Minor optimization to avoid making a copy if the user passes
        # in a sa_collection.CreateCollectionRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, sa_collection.CreateCollectionRequest):
            request = sa_collection.CreateCollectionRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if collection is not None:
                request.collection = collection
            if collection_id is not None:
                request.collection_id = collection_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_collection]

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_collection(self,
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

            def sample_get_collection():
                # Create a client
                client = api_v1alpha.SeqqServiceClient()

                # Initialize request argument(s)
                request = api_v1alpha.GetCollectionRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_collection(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[seqq.api_v1alpha.types.GetCollectionRequest, dict]):
                The request object. GetCollectionRequest is the request
                message for GetCollection.
            name (str):
                The name of the Collection to retrieve. Format:
                ``collections/{collection_id}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
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
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # Minor optimization to avoid making a copy if the user passes
        # in a collection.GetCollectionRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, collection.GetCollectionRequest):
            request = collection.GetCollectionRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_collection]

         # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("name", request.name),
            )),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_collections(self,
            request: Optional[Union[collection.ListCollectionsRequest, dict]] = None,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> pagers.ListCollectionsPager:
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

            def sample_list_collections():
                # Create a client
                client = api_v1alpha.SeqqServiceClient()

                # Initialize request argument(s)
                request = api_v1alpha.ListCollectionsRequest(
                )

                # Make the request
                page_result = client.list_collections(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[seqq.api_v1alpha.types.ListCollectionsRequest, dict]):
                The request object. ListCollectionsRequest is a request
                to list collections.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            seqq.api_v1alpha.services.seqq_service.pagers.ListCollectionsPager:
                ListCollectionsResponse is the
                response message for ListCollections.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a collection.ListCollectionsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, collection.ListCollectionsRequest):
            request = collection.ListCollectionsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_collections]

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListCollectionsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_collection(self,
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

            def sample_delete_collection():
                # Create a client
                client = api_v1alpha.SeqqServiceClient()

                # Initialize request argument(s)
                request = api_v1alpha.DeleteCollectionRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_collection(request=request)

        Args:
            request (Union[seqq.api_v1alpha.types.DeleteCollectionRequest, dict]):
                The request object. DeleteCollectionRequest is the
                request message for DeleteCollection.
            name (str):
                The name of the collection to delete. Format:
                ``collections/{collection_id}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
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
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # Minor optimization to avoid making a copy if the user passes
        # in a collection.DeleteCollectionRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, collection.DeleteCollectionRequest):
            request = collection.DeleteCollectionRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_collection]

         # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("name", request.name),
            )),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def create_sequence(self,
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

            def sample_create_sequence():
                # Create a client
                client = api_v1alpha.SeqqServiceClient()

                # Initialize request argument(s)
                sequence = api_v1alpha.Sequence()
                sequence.sequence = "sequence_value"

                request = api_v1alpha.CreateSequenceRequest(
                    collection="collection_value",
                    sequence_id="sequence_id_value",
                    sequence=sequence,
                )

                # Make the request
                response = client.create_sequence(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[seqq.api_v1alpha.types.CreateSequenceRequest, dict]):
                The request object. CreateSequenceRequest is the request
                message for CreateSequence.
            collection (str):
                The ``name`` of the Collection to create Sequences in.
                Format: ``collections/{collection_id}``.

                This corresponds to the ``collection`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            sequence (seqq.api_v1alpha.types.Sequence):
                The Sequence to create.
                This corresponds to the ``sequence`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            sequence_id (str):
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
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
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
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # Minor optimization to avoid making a copy if the user passes
        # in a sa_sequence.CreateSequenceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, sa_sequence.CreateSequenceRequest):
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
        rpc = self._transport._wrapped_methods[self._transport.create_sequence]

         # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("collection", request.collection),
            )),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def batch_create_sequences(self,
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

            def sample_batch_create_sequences():
                # Create a client
                client = api_v1alpha.SeqqServiceClient()

                # Initialize request argument(s)
                requests = api_v1alpha.CreateSequenceRequest()
                requests.collection = "collection_value"
                requests.sequence_id = "sequence_id_value"
                requests.sequence.sequence = "sequence_value"

                request = api_v1alpha.BatchCreateSequencesRequest(
                    requests=requests,
                )

                # Make the request
                response = client.batch_create_sequences(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[seqq.api_v1alpha.types.BatchCreateSequencesRequest, dict]):
                The request object. BatchCreateSequencesRequest specifies
                how to create a batch of sequences at
                once. Sequences in requests that already
                exist are ignored and not returned in
                the response.
            collection (str):
                The ``name`` of the Collection to create Sequences in.
                Format: ``collections/{collection_id}``.

                This corresponds to the ``collection`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            requests (MutableSequence[seqq.api_v1alpha.types.CreateSequenceRequest]):
                The request message specifying the
                sequences to create. The maximum length
                is 100.

                This corresponds to the ``requests`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
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
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # Minor optimization to avoid making a copy if the user passes
        # in a sequence.BatchCreateSequencesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, sequence.BatchCreateSequencesRequest):
            request = sequence.BatchCreateSequencesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if collection is not None:
                request.collection = collection
            if requests is not None:
                request.requests = requests

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.batch_create_sequences]

         # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("collection", request.collection),
            )),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_sequences_from_file(self,
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

            def sample_create_sequences_from_file():
                # Create a client
                client = api_v1alpha.SeqqServiceClient()

                # Initialize request argument(s)
                request = api_v1alpha.CreateSequencesFromFileRequest(
                    collection="collection_value",
                    encoding="GENBANK",
                    contents=b'contents_blob',
                )

                # Make the request
                response = client.create_sequences_from_file(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[seqq.api_v1alpha.types.CreateSequencesFromFileRequest, dict]):
                The request object. CreateSequencesFromFileRequest
                accepts a file and creates sequences
                from it.
            collection (str):
                The ``name`` of the Collection to create Sequences in.
                Format: ``collections/{collection_id}``.

                This corresponds to the ``collection`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            contents (bytes):
                Content of the file to parse to
                sequences.

                This corresponds to the ``contents`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
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
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # Minor optimization to avoid making a copy if the user passes
        # in a sequence.CreateSequencesFromFileRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, sequence.CreateSequencesFromFileRequest):
            request = sequence.CreateSequencesFromFileRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if collection is not None:
                request.collection = collection
            if contents is not None:
                request.contents = contents

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_sequences_from_file]

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_sequence(self,
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

            def sample_get_sequence():
                # Create a client
                client = api_v1alpha.SeqqServiceClient()

                # Initialize request argument(s)
                request = api_v1alpha.GetSequenceRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_sequence(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[seqq.api_v1alpha.types.GetSequenceRequest, dict]):
                The request object. GetSequenceRequest is the request
                message for GetSequence.
            name (str):
                The ``name`` of the Sequence to retrieve. Format:
                ``collections/{collection_id}/sequences/{sequence_id}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
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
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # Minor optimization to avoid making a copy if the user passes
        # in a sequence.GetSequenceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, sequence.GetSequenceRequest):
            request = sequence.GetSequenceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_sequence]

         # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("name", request.name),
            )),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_sequences(self,
            request: Optional[Union[sequence.ListSequencesRequest, dict]] = None,
            *,
            collection: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> pagers.ListSequencesPager:
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

            def sample_list_sequences():
                # Create a client
                client = api_v1alpha.SeqqServiceClient()

                # Initialize request argument(s)
                request = api_v1alpha.ListSequencesRequest(
                    collection="collection_value",
                )

                # Make the request
                page_result = client.list_sequences(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[seqq.api_v1alpha.types.ListSequencesRequest, dict]):
                The request object. ListSequencesRequest is a request to
                list sequences.
            collection (str):
                The ``name`` of the Collection to list Sequences from.
                Format: ``collections/{collection_id}``.

                This corresponds to the ``collection`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            seqq.api_v1alpha.services.seqq_service.pagers.ListSequencesPager:
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
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # Minor optimization to avoid making a copy if the user passes
        # in a sequence.ListSequencesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, sequence.ListSequencesRequest):
            request = sequence.ListSequencesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if collection is not None:
                request.collection = collection

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_sequences]

         # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("collection", request.collection),
            )),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListSequencesPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_sequence(self,
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

            def sample_delete_sequence():
                # Create a client
                client = api_v1alpha.SeqqServiceClient()

                # Initialize request argument(s)
                request = api_v1alpha.DeleteSequenceRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_sequence(request=request)

        Args:
            request (Union[seqq.api_v1alpha.types.DeleteSequenceRequest, dict]):
                The request object. DeleteSequenceRequest is the request
                message for DeleteSequence.
            name (str):
                The name of the Sequence to delete. Format:
                ``collections/{collection_id}/sequences/{sequence_id}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
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
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # Minor optimization to avoid making a copy if the user passes
        # in a sequence.DeleteSequenceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, sequence.DeleteSequenceRequest):
            request = sequence.DeleteSequenceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_sequence]

         # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("name", request.name),
            )),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def start_search(self,
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

            def sample_start_search():
                # Create a client
                client = api_v1alpha.SeqqServiceClient()

                # Initialize request argument(s)
                search = api_v1alpha.Search()
                search.query = "query_value"

                request = api_v1alpha.StartSearchRequest(
                    collection="collection_value",
                    search=search,
                )

                # Make the request
                response = client.start_search(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[seqq.api_v1alpha.types.StartSearchRequest, dict]):
                The request object. StartSearchRequest is the request
                message for Search.
            collection (str):
                The ``name`` of the Collection to search against. Only
                Sequences in this Collection are queried. Format:
                ``collections/{collection_id}``.

                This corresponds to the ``collection`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            search (seqq.api_v1alpha.types.Search):
                The search parameters to use.
                This corresponds to the ``search`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
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
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # Minor optimization to avoid making a copy if the user passes
        # in a sa_search.StartSearchRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, sa_search.StartSearchRequest):
            request = sa_search.StartSearchRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if collection is not None:
                request.collection = collection
            if search is not None:
                request.search = search

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.start_search]

         # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("collection", request.collection),
            )),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_search(self,
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

            def sample_get_search():
                # Create a client
                client = api_v1alpha.SeqqServiceClient()

                # Initialize request argument(s)
                request = api_v1alpha.GetSearchRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_search(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[seqq.api_v1alpha.types.GetSearchRequest, dict]):
                The request object. GetSearchRequest gets a currently
                ongoing search.
            name (str):
                The name of the Search to retrieve. Format:
                ``collections/{collection_id}/searches/{search_id}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
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
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # Minor optimization to avoid making a copy if the user passes
        # in a search.GetSearchRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, search.GetSearchRequest):
            request = search.GetSearchRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_search]

         # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("name", request.name),
            )),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_searches(self,
            request: Optional[Union[search.ListSearchesRequest, dict]] = None,
            *,
            collection: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> pagers.ListSearchesPager:
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

            def sample_list_searches():
                # Create a client
                client = api_v1alpha.SeqqServiceClient()

                # Initialize request argument(s)
                request = api_v1alpha.ListSearchesRequest(
                    collection="collection_value",
                )

                # Make the request
                page_result = client.list_searches(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[seqq.api_v1alpha.types.ListSearchesRequest, dict]):
                The request object. ListSearchesRequest lists searches.
            collection (str):
                The ``name`` of the Collection to list Searches from.
                Format: ``collections/{collection_id}``.

                This corresponds to the ``collection`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            seqq.api_v1alpha.services.seqq_service.pagers.ListSearchesPager:
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
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # Minor optimization to avoid making a copy if the user passes
        # in a search.ListSearchesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, search.ListSearchesRequest):
            request = search.ListSearchesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if collection is not None:
                request.collection = collection

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_searches]

         # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("collection", request.collection),
            )),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListSearchesPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_search(self,
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

            def sample_delete_search():
                # Create a client
                client = api_v1alpha.SeqqServiceClient()

                # Initialize request argument(s)
                request = api_v1alpha.DeleteSearchRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_search(request=request)

        Args:
            request (Union[seqq.api_v1alpha.types.DeleteSearchRequest, dict]):
                The request object. DeleteSearchRequest deletes a search.
            name (str):
                The name of the Search to delete. Format:
                ``collections/{collection_id}/searches/{search_id}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
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
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # Minor optimization to avoid making a copy if the user passes
        # in a search.DeleteSearchRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, search.DeleteSearchRequest):
            request = search.DeleteSearchRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_search]

         # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("name", request.name),
            )),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def create_integration(self,
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

            def sample_create_integration():
                # Create a client
                client = api_v1alpha.SeqqServiceClient()

                # Initialize request argument(s)
                integration = api_v1alpha.Integration()
                integration.ncbi.manifest = "manifest_value"
                integration.collection = "collection_value"

                request = api_v1alpha.CreateIntegrationRequest(
                    collection="collection_value",
                    integration=integration,
                )

                # Make the request
                response = client.create_integration(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[seqq.api_v1alpha.types.CreateIntegrationRequest, dict]):
                The request object. CreateIntegrationRequest is a request
                to create a new integration.
            collection (str):
                The name of the integration to
                create.

                This corresponds to the ``collection`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            integration (seqq.api_v1alpha.types.Integration):
                The integration to create.
                This corresponds to the ``integration`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            integration_id (str):
                ID of the integration to create.
                This corresponds to the ``integration_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
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
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # Minor optimization to avoid making a copy if the user passes
        # in a sa_integration.CreateIntegrationRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, sa_integration.CreateIntegrationRequest):
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
        rpc = self._transport._wrapped_methods[self._transport.create_integration]

         # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("collection", request.collection),
            )),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_integration(self,
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

            def sample_get_integration():
                # Create a client
                client = api_v1alpha.SeqqServiceClient()

                # Initialize request argument(s)
                request = api_v1alpha.GetIntegrationRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_integration(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[seqq.api_v1alpha.types.GetIntegrationRequest, dict]):
                The request object. GetIntegrationRequest is the request
                message for getting an integration.
            name (str):
                The name of the integration to
                retrieve.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
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
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # Minor optimization to avoid making a copy if the user passes
        # in a integration.GetIntegrationRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, integration.GetIntegrationRequest):
            request = integration.GetIntegrationRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_integration]

         # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("name", request.name),
            )),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_integration(self,
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

            def sample_update_integration():
                # Create a client
                client = api_v1alpha.SeqqServiceClient()

                # Initialize request argument(s)
                integration = api_v1alpha.Integration()
                integration.ncbi.manifest = "manifest_value"
                integration.collection = "collection_value"

                request = api_v1alpha.UpdateIntegrationRequest(
                    integration=integration,
                )

                # Make the request
                response = client.update_integration(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[seqq.api_v1alpha.types.UpdateIntegrationRequest, dict]):
                The request object. UpdateIntegrationRequest is a request
                to update an integration.
            integration (seqq.api_v1alpha.types.Integration):
                The integration to update.
                This corresponds to the ``integration`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                The list of fields to update.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
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
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # Minor optimization to avoid making a copy if the user passes
        # in a sa_integration.UpdateIntegrationRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, sa_integration.UpdateIntegrationRequest):
            request = sa_integration.UpdateIntegrationRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if integration is not None:
                request.integration = integration
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_integration]

         # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("integration.name", request.integration.name),
            )),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_integrations(self,
            request: Optional[Union[integration.ListIntegrationsRequest, dict]] = None,
            *,
            collection: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> pagers.ListIntegrationsPager:
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

            def sample_list_integrations():
                # Create a client
                client = api_v1alpha.SeqqServiceClient()

                # Initialize request argument(s)
                request = api_v1alpha.ListIntegrationsRequest(
                    collection="collection_value",
                )

                # Make the request
                page_result = client.list_integrations(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[seqq.api_v1alpha.types.ListIntegrationsRequest, dict]):
                The request object. ListIntegrationsRequest is a request
                to list integrations.
            collection (str):
                The collection collection of the
                integrations to retrieve.

                This corresponds to the ``collection`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            seqq.api_v1alpha.services.seqq_service.pagers.ListIntegrationsPager:
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
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # Minor optimization to avoid making a copy if the user passes
        # in a integration.ListIntegrationsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, integration.ListIntegrationsRequest):
            request = integration.ListIntegrationsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if collection is not None:
                request.collection = collection

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_integrations]

         # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("collection", request.collection),
            )),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListIntegrationsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_integration(self,
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

            def sample_delete_integration():
                # Create a client
                client = api_v1alpha.SeqqServiceClient()

                # Initialize request argument(s)
                request = api_v1alpha.DeleteIntegrationRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_integration(request=request)

        Args:
            request (Union[seqq.api_v1alpha.types.DeleteIntegrationRequest, dict]):
                The request object. DeleteIntegrationRequest is the
                request message for DeleteIntegration.
            name (str):
                The name of the Integration to delete. Format is
                ``collections/{collection_id}/integrations/{integration_id}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
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
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # Minor optimization to avoid making a copy if the user passes
        # in a integration.DeleteIntegrationRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, integration.DeleteIntegrationRequest):
            request = integration.DeleteIntegrationRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_integration]

         # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("name", request.name),
            )),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def __enter__(self) -> "SeqqServiceClient":
        return self

    def __exit__(self, type, value, traceback):
        """Releases underlying transport's resources.

        .. warning::
            ONLY use as a context manager if the transport is NOT shared
            with other clients! Exiting the with block will CLOSE the transport
            and may cause errors in other clients!
        """
        self.transport.close()







DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(gapic_version=package_version.__version__)


__all__ = (
    "SeqqServiceClient",
)
