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
from __future__ import annotations

from typing import MutableMapping, MutableSequence

import proto  # type: ignore

from google.protobuf import field_mask_pb2  # type: ignore


__protobuf__ = proto.module(
    package='seqq.api.v1alpha',
    manifest={
        'Integration',
        'IntegrationNCBI',
        'IntegrationGoogleDrive',
        'CreateIntegrationRequest',
        'UpdateIntegrationRequest',
        'GetIntegrationRequest',
        'ListIntegrationsRequest',
        'ListIntegrationsResponse',
        'DeleteIntegrationRequest',
    },
)


class Integration(proto.Message):
    r"""Integrations instruct seqq to import Sequences from external
    sources.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        collection (str):
            The name of the Collection that the Integration imports
            Sequences to. Format is ``collections/{collection_id}``.
        name (str):
            A globally unique name of the Integration. Format is
            ``collections/{collection_id}/integrations/{integration_id}``.
        sequence_id_prefix (str):
            A prefix that is prepended to all Sequence
            IDs added to the Collection.
            For example, if "proteins/flourescent" is
            imported to a Collection "my-collection", and a
            Sequence with an ID of "GFP" is imported, the
            Sequence name will be
            "collections/my-collection/sequences/proteins/flourescent/GFP".
        etag (str):
            An opaque, server-assigned value that is the
            hash of all fields in the Integration. Each
            change to an integration changes the Etag value.
        ncbi (seqq.api_v1alpha.types.IntegrationNCBI):
            NCBI integration.

            This field is a member of `oneof`_ ``import``.
        google_drive (seqq.api_v1alpha.types.IntegrationGoogleDrive):
            Google Drive integration.

            This field is a member of `oneof`_ ``import``.
    """

    collection: str = proto.Field(
        proto.STRING,
        number=1,
    )
    name: str = proto.Field(
        proto.STRING,
        number=2,
    )
    sequence_id_prefix: str = proto.Field(
        proto.STRING,
        number=3,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=4,
    )
    ncbi: 'IntegrationNCBI' = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof='import',
        message='IntegrationNCBI',
    )
    google_drive: 'IntegrationGoogleDrive' = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof='import',
        message='IntegrationGoogleDrive',
    )


class IntegrationNCBI(proto.Message):
    r"""NCBI integration.

    Attributes:
        manifest (str):
            The URL of an NCBI manifest to import
            Sequences from. These are from the BLAST FTP
            website. For example,
            "https://ftp.ncbi.nlm.nih.gov/blast/db/taxdb-metadata.json"
            imports Sequences from the NCBI Taxonomy
            database.
        uploads (MutableMapping[str, int]):
            A map from file name to the count of
            sequences uploaded from that file. Files do not
            change in NCBI. This field is set by the server
            so integrations can skip sequence uploading if
            the sequences has already been uploaded. These
            are set when we fail to upload a single sequence
            within the file.
    """

    manifest: str = proto.Field(
        proto.STRING,
        number=1,
    )
    uploads: MutableMapping[str, int] = proto.MapField(
        proto.STRING,
        proto.INT64,
        number=2,
    )


class IntegrationGoogleDrive(proto.Message):
    r"""Google Drive integration.

    Attributes:
        service_account_credentials (bytes):
            Base64 encoded credentials for the service
            account authorized to list sequences in Google
            Drive.
    """

    service_account_credentials: bytes = proto.Field(
        proto.BYTES,
        number=1,
    )


class CreateIntegrationRequest(proto.Message):
    r"""CreateIntegrationRequest is a request to create a new
    integration.

    Attributes:
        collection (str):
            The name of the integration to create.
        integration_id (str):
            ID of the integration to create.
        integration (seqq.api_v1alpha.types.Integration):
            The integration to create.
    """

    collection: str = proto.Field(
        proto.STRING,
        number=1,
    )
    integration_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    integration: 'Integration' = proto.Field(
        proto.MESSAGE,
        number=3,
        message='Integration',
    )


class UpdateIntegrationRequest(proto.Message):
    r"""UpdateIntegrationRequest is a request to update an
    integration.

    Attributes:
        integration (seqq.api_v1alpha.types.Integration):
            The integration to update.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            The list of fields to update.
    """

    integration: 'Integration' = proto.Field(
        proto.MESSAGE,
        number=1,
        message='Integration',
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class GetIntegrationRequest(proto.Message):
    r"""GetIntegrationRequest is the request message for getting an
    integration.

    Attributes:
        name (str):
            The name of the integration to retrieve.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListIntegrationsRequest(proto.Message):
    r"""ListIntegrationsRequest is a request to list integrations.

    Attributes:
        collection (str):
            The collection collection of the integrations
            to retrieve.
        page_size (int):
            The maximum number of Integrations to return.
            If unset, at most 50 Integrations will be
            returned. The maximum value is 1000; values
            above 1000 will be coerced to 1000.
        page_token (str):
            A page token, received from a previous List
            Integrations call. Provide this to retrieve the
            subsequent page. When paginating, all other
            parameters provided to ListIntegrations must
            match the call that provided the page token.
    """

    collection: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )


class ListIntegrationsResponse(proto.Message):
    r"""ListIntegrationsResponse holds a list of integrations.

    Attributes:
        integrations (MutableSequence[seqq.api_v1alpha.types.Integration]):
            A list of Integrations in the Collection.
        next_page_token (str):
            A token to retrieve the next page of
            Integrations.
    """

    @property
    def raw_page(self):
        return self

    integrations: MutableSequence['Integration'] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message='Integration',
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class DeleteIntegrationRequest(proto.Message):
    r"""DeleteIntegrationRequest is the request message for
    DeleteIntegration.

    Attributes:
        name (str):
            The name of the Integration to delete. Format is
            ``collections/{collection_id}/integrations/{integration_id}``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
