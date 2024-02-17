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

from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package='seqq.api.v1alpha',
    manifest={
        'Code',
        'FileEncoding',
        'Sequence',
        'CreateSequenceRequest',
        'BatchCreateSequencesRequest',
        'BatchCreateSequencesResponse',
        'CreateSequencesFromFileRequest',
        'CreateSequencesFromFileResponse',
        'GetSequenceRequest',
        'ListSequencesRequest',
        'ListSequencesResponse',
        'DeleteSequenceRequest',
    },
)


class Code(proto.Enum):
    r"""Code is the type of sequence.

    Values:
        CODE_UNSPECIFIED (0):
            CODE_UNSPECIFIED is the default value.
        NUCLEIC (1):
            NUCLEIC is a nucleic acid sequence.
        PROTEIN (2):
            PROTEIN is an amino acid sequence.
    """
    CODE_UNSPECIFIED = 0
    NUCLEIC = 1
    PROTEIN = 2


class FileEncoding(proto.Enum):
    r"""FileEncoding is the type of sequence file to upload.

    Values:
        FILE_UNSPECIFIED (0):
            FILE_UNSPECIFIED is the default value.
        FASTA (1):
            FASTA is a FASTA file.
        GENBANK (2):
            GEBANK is a GenBank file.
    """
    FILE_UNSPECIFIED = 0
    FASTA = 1
    GENBANK = 2


class Sequence(proto.Message):
    r"""Sequence is a single entry containing nucleotides or amino
    acids and other optional metadata like a description, creation
    time, and taxonomy ID.

    Attributes:
        name (str):
            Name of the Sequence. Format:
            ``collections/{collection_id}/sequences/{sequence_id}``.
        collection (str):
            The ``name`` of the Collection the Sequence belongs to.
            Format: ``collections/{collection_id}``.
        sequence (str):
            A sequence of nucleotides or amino acids.
            Only characters in the IUPAC alphabets are
            allowed.
        code (seqq.api_v1alpha.types.Code):
            The code of the ``sequence``. This is guessed from
            ``sequence`` when unset.
        taxonomy_id (str):
            The taxonomy ID of the sequence in NCBI's
            Taxonomy database. This can be used to filter
            BLAST search results.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            The time that the Sequence was created. This
            is set once on creation by the server.
        etag (str):
            An opaque, server-assigned value that is a
            hash of all other fields in the Sequence
            resource. This is used during deletes to ensure
            stale Sequences are excluded from Search
            responses.
        description (str):
            A description of the Sequence. For Sequences
            from FASTA files, this is the entire description
            line without the leading ">". For Sequences from
            GenBank files, this is from the Description
            field.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    collection: str = proto.Field(
        proto.STRING,
        number=2,
    )
    sequence: str = proto.Field(
        proto.STRING,
        number=3,
    )
    code: 'Code' = proto.Field(
        proto.ENUM,
        number=4,
        enum='Code',
    )
    taxonomy_id: str = proto.Field(
        proto.STRING,
        number=5,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=6,
        message=timestamp_pb2.Timestamp,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=7,
    )
    description: str = proto.Field(
        proto.STRING,
        number=8,
    )


class CreateSequenceRequest(proto.Message):
    r"""CreateSequenceRequest is the request message for
    CreateSequence.

    Attributes:
        collection (str):
            The ``name`` of the Collection to create Sequences in.
            Format: ``collections/{collection_id}``.
        sequence_id (str):
            The ID of the Sequence to create.

            This is appended to the Collection name and ``/sequences/``
            to create the Sequence name.

            For example, if ``collection`` is
            ``collections/my-collection``, and ``sequence_id`` is
            ``my-prefix/my-sequence``, the Sequence name will be
            ``collections/my-collection/sequences/my-prefix/my-sequence``.

            The ``/`` delimiter is encouraged to group Sequences by
            prefix. This is useful in both the UI, where Sequences are
            grouped by folders by ``/``-delimited prefixes, and in
            Searches where a Search can be limited to a subset of
            Sequences by prefix.
        sequence (seqq.api_v1alpha.types.Sequence):
            The Sequence to create.
    """

    collection: str = proto.Field(
        proto.STRING,
        number=1,
    )
    sequence_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    sequence: 'Sequence' = proto.Field(
        proto.MESSAGE,
        number=3,
        message='Sequence',
    )


class BatchCreateSequencesRequest(proto.Message):
    r"""BatchCreateSequencesRequest specifies how to create a batch
    of sequences at once. Sequences in requests that already exist
    are ignored and not returned in the response.

    Attributes:
        collection (str):
            The ``name`` of the Collection to create Sequences in.
            Format: ``collections/{collection_id}``.
        requests (MutableSequence[seqq.api_v1alpha.types.CreateSequenceRequest]):
            The request message specifying the sequences
            to create. The maximum length is 100.
    """

    collection: str = proto.Field(
        proto.STRING,
        number=1,
    )
    requests: MutableSequence['CreateSequenceRequest'] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message='CreateSequenceRequest',
    )


class BatchCreateSequencesResponse(proto.Message):
    r"""BatchCreateSequencesResponse is the response message for
    BatchCreateSequences.

    Attributes:
        sequences (MutableSequence[seqq.api_v1alpha.types.Sequence]):
            Sequences are the sequences that were
            created.
    """

    sequences: MutableSequence['Sequence'] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message='Sequence',
    )


class CreateSequencesFromFileRequest(proto.Message):
    r"""CreateSequencesFromFileRequest accepts a file and creates
    sequences from it.

    Attributes:
        collection (str):
            The ``name`` of the Collection to create Sequences in.
            Format: ``collections/{collection_id}``.
        sequence_id_prefix (str):
            A prefix to prepend to all sequences in the
            file. Accessions are parsed from the sequence
            file.
        encoding (seqq.api_v1alpha.types.FileEncoding):
            The type of file to parse.
        contents (bytes):
            Content of the file to parse to sequences.
    """

    collection: str = proto.Field(
        proto.STRING,
        number=1,
    )
    sequence_id_prefix: str = proto.Field(
        proto.STRING,
        number=2,
    )
    encoding: 'FileEncoding' = proto.Field(
        proto.ENUM,
        number=3,
        enum='FileEncoding',
    )
    contents: bytes = proto.Field(
        proto.BYTES,
        number=4,
    )


class CreateSequencesFromFileResponse(proto.Message):
    r"""Contains the sequences that were created from the file.

    Attributes:
        sequences (MutableSequence[seqq.api_v1alpha.types.Sequence]):
            Sequences are the sequences that were
            created.
    """

    sequences: MutableSequence['Sequence'] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message='Sequence',
    )


class GetSequenceRequest(proto.Message):
    r"""GetSequenceRequest is the request message for GetSequence.

    Attributes:
        name (str):
            The ``name`` of the Sequence to retrieve. Format:
            ``collections/{collection_id}/sequences/{sequence_id}``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListSequencesRequest(proto.Message):
    r"""ListSequencesRequest is a request to list sequences.

    Attributes:
        collection (str):
            The ``name`` of the Collection to list Sequences from.
            Format: ``collections/{collection_id}``.
        page_size (int):
            The maximum number of Sequences to return.
            seqq may return fewer than this value. If unset,
            at most 50 sequences will be returned. The
            maximum value is 1000; values above 1000 will be
            coerced to 1000.
        page_token (str):
            A page token from a previous List Sequences
            call. Provide this to retrieve the subsequent
            page. When paginating, all other parameters
            provided to List Sequences must match the call
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


class ListSequencesResponse(proto.Message):
    r"""ListSequencesResponse is the response message for
    ListSequences.

    Attributes:
        sequences (MutableSequence[seqq.api_v1alpha.types.Sequence]):
            A list of Sequences.
        next_page_token (str):
            Next page token is the token to use to
            retrieve the next page of results.
    """

    @property
    def raw_page(self):
        return self

    sequences: MutableSequence['Sequence'] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message='Sequence',
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class DeleteSequenceRequest(proto.Message):
    r"""DeleteSequenceRequest is the request message for
    DeleteSequence.

    Attributes:
        name (str):
            The name of the Sequence to delete. Format:
            ``collections/{collection_id}/sequences/{sequence_id}``.
        force (bool):
            Whether to return a successful response even
            if the Sequence does not exist.
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
