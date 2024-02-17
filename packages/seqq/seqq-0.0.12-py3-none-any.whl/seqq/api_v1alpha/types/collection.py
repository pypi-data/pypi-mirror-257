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


__protobuf__ = proto.module(
    package='seqq.api.v1alpha',
    manifest={
        'Collection',
        'CreateCollectionRequest',
        'GetCollectionRequest',
        'ListCollectionsRequest',
        'ListCollectionsResponse',
        'DeleteCollectionRequest',
    },
)


class Collection(proto.Message):
    r"""Collections contain Sequences, Searches, and Integration.

    Attributes:
        name (str):
            A globally unique name for the Collection. Format is
            ``collections/{collection_id}`` where ``collection_id`` is
            set during creation. This is not modifiable.
        display_name (str):
            Display name of the collection in the UI. This can differ
            from ``name``. If set, this is used in place of
            ``collection_id`` in the UI.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=2,
    )


class CreateCollectionRequest(proto.Message):
    r"""CreateCollectionRequest is used to create a collection.

    Attributes:
        collection_id (str):
            ID of the collection to create. Must be
            unique within the parent project. Must be
            between 3 and 64 characters long and can only
            contain alphanumeric characters and hyphens.
        collection (seqq.api_v1alpha.types.Collection):
            Collection to create. Provide ``collection`` when setting
            ``display_name``.
    """

    collection_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    collection: 'Collection' = proto.Field(
        proto.MESSAGE,
        number=2,
        message='Collection',
    )


class GetCollectionRequest(proto.Message):
    r"""GetCollectionRequest is the request message for
    GetCollection.

    Attributes:
        name (str):
            The name of the Collection to retrieve. Format:
            ``collections/{collection_id}``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListCollectionsRequest(proto.Message):
    r"""ListCollectionsRequest is a request to list collections.

    Attributes:
        page_size (int):
            The maximum number of Collections to return.
            If unset, at most 50 Collections will be
            returned. The maximum value is 1000; values
            above 1000 will be coerced to 1000.
        page_token (str):
            A page token from a previous List Collections
            call. Provide this to retrieve the subsequent
            page.
    """

    page_size: int = proto.Field(
        proto.INT32,
        number=1,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class ListCollectionsResponse(proto.Message):
    r"""ListCollectionsResponse is the response message for
    ListCollections.

    Attributes:
        collections (MutableSequence[seqq.api_v1alpha.types.Collection]):
            Collections ordered by their name.
        next_page_token (str):
            A token to retrieve the next page of results.
            This is an opaque value that should not be
            parsed. If this is unset, there are no more
            collections to list.
    """

    @property
    def raw_page(self):
        return self

    collections: MutableSequence['Collection'] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message='Collection',
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class DeleteCollectionRequest(proto.Message):
    r"""DeleteCollectionRequest is the request message for
    DeleteCollection.

    Attributes:
        name (str):
            The name of the collection to delete. Format:
            ``collections/{collection_id}``.
        force (bool):
            Force deletion of the collection even if it
            contains Sequences, Integrations, or Searches.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    force: bool = proto.Field(
        proto.BOOL,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
