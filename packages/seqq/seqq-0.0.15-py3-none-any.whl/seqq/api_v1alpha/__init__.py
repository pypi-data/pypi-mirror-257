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
from seqq.api_v1alpha import gapic_version as package_version

__version__ = package_version.__version__


from .services.seqq_service import SeqqServiceClient
from .services.seqq_service import SeqqServiceAsyncClient

from .types.collection import Collection
from .types.collection import CreateCollectionRequest
from .types.collection import DeleteCollectionRequest
from .types.collection import GetCollectionRequest
from .types.collection import ListCollectionsRequest
from .types.collection import ListCollectionsResponse
from .types.integration import CreateIntegrationRequest
from .types.integration import DeleteIntegrationRequest
from .types.integration import GetIntegrationRequest
from .types.integration import Integration
from .types.integration import IntegrationGoogleDrive
from .types.integration import IntegrationNCBI
from .types.integration import ListIntegrationsRequest
from .types.integration import ListIntegrationsResponse
from .types.integration import UpdateIntegrationRequest
from .types.search import Blastn
from .types.search import Blastp
from .types.search import Blastx
from .types.search import DeleteSearchRequest
from .types.search import GetSearchRequest
from .types.search import Hit
from .types.search import ListSearchesRequest
from .types.search import ListSearchesResponse
from .types.search import Search
from .types.search import StartSearchRequest
from .types.search import Tblastn
from .types.search import Tblastx
from .types.sequence import BatchCreateSequencesRequest
from .types.sequence import BatchCreateSequencesResponse
from .types.sequence import CreateSequenceRequest
from .types.sequence import CreateSequencesFromFileRequest
from .types.sequence import CreateSequencesFromFileResponse
from .types.sequence import DeleteSequenceRequest
from .types.sequence import GetSequenceRequest
from .types.sequence import ListSequencesRequest
from .types.sequence import ListSequencesResponse
from .types.sequence import Sequence
from .types.sequence import Code
from .types.sequence import FileEncoding

__all__ = (
    'SeqqServiceAsyncClient',
'BatchCreateSequencesRequest',
'BatchCreateSequencesResponse',
'Blastn',
'Blastp',
'Blastx',
'Code',
'Collection',
'CreateCollectionRequest',
'CreateIntegrationRequest',
'CreateSequenceRequest',
'CreateSequencesFromFileRequest',
'CreateSequencesFromFileResponse',
'DeleteCollectionRequest',
'DeleteIntegrationRequest',
'DeleteSearchRequest',
'DeleteSequenceRequest',
'FileEncoding',
'GetCollectionRequest',
'GetIntegrationRequest',
'GetSearchRequest',
'GetSequenceRequest',
'Hit',
'Integration',
'IntegrationGoogleDrive',
'IntegrationNCBI',
'ListCollectionsRequest',
'ListCollectionsResponse',
'ListIntegrationsRequest',
'ListIntegrationsResponse',
'ListSearchesRequest',
'ListSearchesResponse',
'ListSequencesRequest',
'ListSequencesResponse',
'Search',
'SeqqServiceClient',
'Sequence',
'StartSearchRequest',
'Tblastn',
'Tblastx',
'UpdateIntegrationRequest',
)
