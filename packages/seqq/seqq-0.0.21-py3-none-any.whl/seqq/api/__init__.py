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
from seqq.api import gapic_version as package_version

__version__ = package_version.__version__


from seqq.api_v1alpha.services.seqq_service.client import SeqqServiceClient
from seqq.api_v1alpha.services.seqq_service.async_client import SeqqServiceAsyncClient

from seqq.api_v1alpha.types.collection import Collection
from seqq.api_v1alpha.types.collection import CreateCollectionRequest
from seqq.api_v1alpha.types.collection import DeleteCollectionRequest
from seqq.api_v1alpha.types.collection import GetCollectionRequest
from seqq.api_v1alpha.types.collection import ListCollectionsRequest
from seqq.api_v1alpha.types.collection import ListCollectionsResponse
from seqq.api_v1alpha.types.integration import CreateIntegrationRequest
from seqq.api_v1alpha.types.integration import DeleteIntegrationRequest
from seqq.api_v1alpha.types.integration import GetIntegrationRequest
from seqq.api_v1alpha.types.integration import Integration
from seqq.api_v1alpha.types.integration import IntegrationGoogleDrive
from seqq.api_v1alpha.types.integration import IntegrationNCBI
from seqq.api_v1alpha.types.integration import ListIntegrationsRequest
from seqq.api_v1alpha.types.integration import ListIntegrationsResponse
from seqq.api_v1alpha.types.integration import UpdateIntegrationRequest
from seqq.api_v1alpha.types.search import Blastn
from seqq.api_v1alpha.types.search import Blastp
from seqq.api_v1alpha.types.search import Blastx
from seqq.api_v1alpha.types.search import DeleteSearchRequest
from seqq.api_v1alpha.types.search import GetSearchRequest
from seqq.api_v1alpha.types.search import Hit
from seqq.api_v1alpha.types.search import ListSearchesRequest
from seqq.api_v1alpha.types.search import ListSearchesResponse
from seqq.api_v1alpha.types.search import Search
from seqq.api_v1alpha.types.search import StartSearchRequest
from seqq.api_v1alpha.types.search import Tblastn
from seqq.api_v1alpha.types.search import Tblastx
from seqq.api_v1alpha.types.sequence import BatchCreateSequencesRequest
from seqq.api_v1alpha.types.sequence import BatchCreateSequencesResponse
from seqq.api_v1alpha.types.sequence import CreateSequenceRequest
from seqq.api_v1alpha.types.sequence import CreateSequencesFromFileRequest
from seqq.api_v1alpha.types.sequence import CreateSequencesFromFileResponse
from seqq.api_v1alpha.types.sequence import DeleteSequenceRequest
from seqq.api_v1alpha.types.sequence import GetSequenceRequest
from seqq.api_v1alpha.types.sequence import ListSequencesRequest
from seqq.api_v1alpha.types.sequence import ListSequencesResponse
from seqq.api_v1alpha.types.sequence import Sequence
from seqq.api_v1alpha.types.sequence import Code
from seqq.api_v1alpha.types.sequence import FileEncoding

__all__ = ('SeqqServiceClient',
    'SeqqServiceAsyncClient',
    'Collection',
    'CreateCollectionRequest',
    'DeleteCollectionRequest',
    'GetCollectionRequest',
    'ListCollectionsRequest',
    'ListCollectionsResponse',
    'CreateIntegrationRequest',
    'DeleteIntegrationRequest',
    'GetIntegrationRequest',
    'Integration',
    'IntegrationGoogleDrive',
    'IntegrationNCBI',
    'ListIntegrationsRequest',
    'ListIntegrationsResponse',
    'UpdateIntegrationRequest',
    'Blastn',
    'Blastp',
    'Blastx',
    'DeleteSearchRequest',
    'GetSearchRequest',
    'Hit',
    'ListSearchesRequest',
    'ListSearchesResponse',
    'Search',
    'StartSearchRequest',
    'Tblastn',
    'Tblastx',
    'BatchCreateSequencesRequest',
    'BatchCreateSequencesResponse',
    'CreateSequenceRequest',
    'CreateSequencesFromFileRequest',
    'CreateSequencesFromFileResponse',
    'DeleteSequenceRequest',
    'GetSequenceRequest',
    'ListSequencesRequest',
    'ListSequencesResponse',
    'Sequence',
    'Code',
    'FileEncoding',
)
