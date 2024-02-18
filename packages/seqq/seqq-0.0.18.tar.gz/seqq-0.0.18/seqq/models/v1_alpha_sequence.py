import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.v1_alpha_code import V1AlphaCode
from ..types import UNSET, Unset

T = TypeVar("T", bound="V1AlphaSequence")


@_attrs_define
class V1AlphaSequence:
    """Sequence is a single entry containing nucleotides or amino acids and other optional metadata like a description,
    creation time, and taxonomy ID.

        Attributes:
            sequence (str): A sequence of nucleotides or amino acids. Only characters in the IUPAC alphabets are allowed.
            name (Union[Unset, str]): Name of the Sequence. Format: `collections/{collection_id}/sequences/{sequence_id}`.
            collection (Union[Unset, str]): The `name` of the Collection the Sequence belongs to. Format:
                `collections/{collection_id}`.
            code (Union[Unset, V1AlphaCode]): Code is the type of sequence.

                 - CODE_UNSPECIFIED: CODE_UNSPECIFIED is the default value.
                 - NUCLEIC: NUCLEIC is a nucleic acid sequence.
                 - PROTEIN: PROTEIN is an amino acid sequence.
            taxonomy_id (Union[Unset, str]): The taxonomy ID of the sequence in NCBI's Taxonomy database. This can be used
                to filter BLAST
                search results.
            create_time (Union[Unset, datetime.datetime]): The time that the Sequence was created. This is set once on
                creation by the server.
            etag (Union[Unset, str]): An opaque, server-assigned value that is a hash of all other fields in the Sequence
                resource.
                This is used during deletes to ensure stale Sequences are excluded from Search responses.
            description (Union[Unset, str]): A description of the Sequence. For Sequences from FASTA files, this is the
                entire
                description line without the leading ">". For Sequences from GenBank files, this
                is from the Description field.
    """

    sequence: str
    name: Union[Unset, str] = UNSET
    collection: Union[Unset, str] = UNSET
    code: Union[Unset, V1AlphaCode] = UNSET
    taxonomy_id: Union[Unset, str] = UNSET
    create_time: Union[Unset, datetime.datetime] = UNSET
    etag: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        sequence = self.sequence

        name = self.name

        collection = self.collection

        code: Union[Unset, str] = UNSET
        if not isinstance(self.code, Unset):
            code = self.code.value

        taxonomy_id = self.taxonomy_id

        create_time: Union[Unset, str] = UNSET
        if not isinstance(self.create_time, Unset):
            create_time = self.create_time.isoformat()

        etag = self.etag

        description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "sequence": sequence,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if collection is not UNSET:
            field_dict["collection"] = collection
        if code is not UNSET:
            field_dict["code"] = code
        if taxonomy_id is not UNSET:
            field_dict["taxonomyId"] = taxonomy_id
        if create_time is not UNSET:
            field_dict["createTime"] = create_time
        if etag is not UNSET:
            field_dict["etag"] = etag
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        sequence = d.pop("sequence")

        name = d.pop("name", UNSET)

        collection = d.pop("collection", UNSET)

        _code = d.pop("code", UNSET)
        code: Union[Unset, V1AlphaCode]
        if isinstance(_code, Unset):
            code = UNSET
        else:
            code = V1AlphaCode(_code)

        taxonomy_id = d.pop("taxonomyId", UNSET)

        _create_time = d.pop("createTime", UNSET)
        create_time: Union[Unset, datetime.datetime]
        if isinstance(_create_time, Unset):
            create_time = UNSET
        else:
            create_time = isoparse(_create_time)

        etag = d.pop("etag", UNSET)

        description = d.pop("description", UNSET)

        v1_alpha_sequence = cls(
            sequence=sequence,
            name=name,
            collection=collection,
            code=code,
            taxonomy_id=taxonomy_id,
            create_time=create_time,
            etag=etag,
            description=description,
        )

        v1_alpha_sequence.additional_properties = d
        return v1_alpha_sequence

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
