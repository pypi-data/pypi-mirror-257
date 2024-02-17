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

from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
from seqq.api_v1alpha.types import sequence


__protobuf__ = proto.module(
    package='seqq.api.v1alpha',
    manifest={
        'Search',
        'Hit',
        'StartSearchRequest',
        'GetSearchRequest',
        'ListSearchesRequest',
        'ListSearchesResponse',
        'DeleteSearchRequest',
        'Blastn',
        'Blastp',
        'Blastx',
        'Tblastn',
        'Tblastx',
    },
)


class Search(proto.Message):
    r"""A Search of the Sequences in a Collection.

    On creation, Searches direct seqq to start a query against a
    Collection using a chosen ``program``. On reads, Searches contain
    the results of the query, including its current ``state`` and any
    ``hits``.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            The globally unique name of the Serach. Format is
            ``collections/{collection_id}/searches/{search_id}``.
        query (str):
            The sequence of nucleoties or amino acids to
            search the Collection for.
        code (seqq.api_v1alpha.types.Code):
            The code of the ``sequence``. This is guessed from
            ``sequence`` when unset.
        prefix (str):
            An optional "/" separated prefix to limit
            searches to.
        query_time (google.protobuf.timestamp_pb2.Timestamp):
            The time a search start is started.
        query_duration (google.protobuf.duration_pb2.Duration):
            The duration of a search from start to
            completion.
        hits (MutableSequence[seqq.api_v1alpha.types.Hit]):
            A list of hits from the Search. This is only set when
            ``state`` is ``SUCCEEDED``.
        state (seqq.api_v1alpha.types.Search.State):
            The current state of the Search.
        error (google.rpc.status_pb2.Status):
            The error that occurred during the search. This is only set
            when ``state`` is ``FAILED``.
        blastn (seqq.api_v1alpha.types.Blastn):
            Run a blastn search.

            This field is a member of `oneof`_ ``program``.
        blastp (seqq.api_v1alpha.types.Blastp):
            Run a blastp search.

            This field is a member of `oneof`_ ``program``.
        blastx (seqq.api_v1alpha.types.Blastp):
            Run a blastx search.

            This field is a member of `oneof`_ ``program``.
        tblastn (seqq.api_v1alpha.types.Tblastn):
            Run a tblastn search.

            This field is a member of `oneof`_ ``program``.
        tblastx (seqq.api_v1alpha.types.Tblastx):
            Run a tblastx search.

            This field is a member of `oneof`_ ``program``.
    """
    class State(proto.Enum):
        r"""The current state of the Search.

        Values:
            STATE_UNSPECIFIED (0):
                STATE_UNSPECIFIED is the default value.
            RUNNING (1):
                RUNNING is the search is running.
            SUCCEEDED (2):
                SUCCEEDED is the search succeeded.
            FAILED (3):
                FAILED is the search failed.
        """
        STATE_UNSPECIFIED = 0
        RUNNING = 1
        SUCCEEDED = 2
        FAILED = 3

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    query: str = proto.Field(
        proto.STRING,
        number=2,
    )
    code: sequence.Code = proto.Field(
        proto.ENUM,
        number=3,
        enum=sequence.Code,
    )
    prefix: str = proto.Field(
        proto.STRING,
        number=4,
    )
    query_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )
    query_duration: duration_pb2.Duration = proto.Field(
        proto.MESSAGE,
        number=6,
        message=duration_pb2.Duration,
    )
    hits: MutableSequence['Hit'] = proto.RepeatedField(
        proto.MESSAGE,
        number=7,
        message='Hit',
    )
    state: State = proto.Field(
        proto.ENUM,
        number=8,
        enum=State,
    )
    error: status_pb2.Status = proto.Field(
        proto.MESSAGE,
        number=9,
        message=status_pb2.Status,
    )
    blastn: 'Blastn' = proto.Field(
        proto.MESSAGE,
        number=10,
        oneof='program',
        message='Blastn',
    )
    blastp: 'Blastp' = proto.Field(
        proto.MESSAGE,
        number=11,
        oneof='program',
        message='Blastp',
    )
    blastx: 'Blastp' = proto.Field(
        proto.MESSAGE,
        number=12,
        oneof='program',
        message='Blastp',
    )
    tblastn: 'Tblastn' = proto.Field(
        proto.MESSAGE,
        number=13,
        oneof='program',
        message='Tblastn',
    )
    tblastx: 'Tblastx' = proto.Field(
        proto.MESSAGE,
        number=14,
        oneof='program',
        message='Tblastx',
    )


class Hit(proto.Message):
    r"""Hit is a single hit from a Search.

    Attributes:
        saccver (str):
            Subject accession version.
        pident (float):
            Percentage of identical matches.
        length (int):
            Alignment length.
        mismatch (int):
            Number of mismatches.
        gapopen (int):
            Number of gap openings.
        qstart (int):
            Start of alignment in search.
        qend (int):
            End of alignment in search.
        sstart (int):
            Start of alignment in subject.
        send (int):
            End of alignment in subject.
        evalue (float):
            Expect value.
        bitscore (float):
            Bit score.
    """

    saccver: str = proto.Field(
        proto.STRING,
        number=1,
    )
    pident: float = proto.Field(
        proto.DOUBLE,
        number=2,
    )
    length: int = proto.Field(
        proto.INT64,
        number=3,
    )
    mismatch: int = proto.Field(
        proto.INT64,
        number=4,
    )
    gapopen: int = proto.Field(
        proto.INT64,
        number=5,
    )
    qstart: int = proto.Field(
        proto.INT64,
        number=6,
    )
    qend: int = proto.Field(
        proto.INT64,
        number=7,
    )
    sstart: int = proto.Field(
        proto.INT64,
        number=8,
    )
    send: int = proto.Field(
        proto.INT64,
        number=9,
    )
    evalue: float = proto.Field(
        proto.DOUBLE,
        number=10,
    )
    bitscore: float = proto.Field(
        proto.DOUBLE,
        number=11,
    )


class StartSearchRequest(proto.Message):
    r"""StartSearchRequest is the request message for Search.

    Attributes:
        collection (str):
            The ``name`` of the Collection to search against. Only
            Sequences in this Collection are queried. Format:
            ``collections/{collection_id}``.
        search (seqq.api_v1alpha.types.Search):
            The search parameters to use.
    """

    collection: str = proto.Field(
        proto.STRING,
        number=1,
    )
    search: 'Search' = proto.Field(
        proto.MESSAGE,
        number=2,
        message='Search',
    )


class GetSearchRequest(proto.Message):
    r"""GetSearchRequest gets a currently ongoing search.

    Attributes:
        name (str):
            The name of the Search to retrieve. Format:
            ``collections/{collection_id}/searches/{search_id}``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListSearchesRequest(proto.Message):
    r"""ListSearchesRequest lists searches.

    Attributes:
        collection (str):
            The ``name`` of the Collection to list Searches from.
            Format: ``collections/{collection_id}``.
        page_size (int):
            The maximum number of Searches to return. If
            unset, at most 50 Searches will be returned. The
            maximum value is 1000; values above 1000 will be
            coerced to 1000.
        page_token (str):
            A page token from a previous List Searches
            call. Provide this to retrieve the subsequent
            page. When paginating, all other parameters
            provided to List Searches must match the call
            that provided the page token.
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


class ListSearchesResponse(proto.Message):
    r"""ListSearchesResponse is the response message for
    ListSequences.

    Attributes:
        searches (MutableSequence[seqq.api_v1alpha.types.Search]):
            A list of Searches.
        next_page_token (str):
            Next page token is the token to use to
            retrieve the next page of results.
    """

    @property
    def raw_page(self):
        return self

    searches: MutableSequence['Search'] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message='Search',
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class DeleteSearchRequest(proto.Message):
    r"""DeleteSearchRequest deletes a search.

    Attributes:
        name (str):
            The name of the Search to delete. Format:
            ``collections/{collection_id}/searches/{search_id}``.
        force (bool):
            Whether to return a successful response even
            if the Search does not exist.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    force: bool = proto.Field(
        proto.BOOL,
        number=2,
    )


class Blastn(proto.Message):
    r"""Blastn is a blastn search.
    """


class Blastp(proto.Message):
    r"""Blastp is a blastp search.
    """


class Blastx(proto.Message):
    r"""Blastx is a blastx search.
    """


class Tblastn(proto.Message):
    r"""Tblastn is a tblastn search.
    """


class Tblastx(proto.Message):
    r"""Tblastx is a tblastx search.
    """


__all__ = tuple(sorted(__protobuf__.manifest))
