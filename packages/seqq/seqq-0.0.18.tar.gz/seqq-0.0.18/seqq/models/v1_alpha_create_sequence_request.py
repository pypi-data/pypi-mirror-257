from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.v1_alpha_sequence import V1AlphaSequence


T = TypeVar("T", bound="V1AlphaCreateSequenceRequest")


@_attrs_define
class V1AlphaCreateSequenceRequest:
    """CreateSequenceRequest is the request message for CreateSequence.

    Attributes:
        collection (str): The `name` of the Collection to create Sequences in. Format: `collections/{collection_id}`.
        sequence_id (str): The ID of the Sequence to create.

            This is appended to the Collection name and `/sequences/` to create the Sequence name.

            For example, if `collection` is `collections/my-collection`, and `sequence_id` is `my-prefix/my-sequence`,
            the Sequence name will be `collections/my-collection/sequences/my-prefix/my-sequence`.

            The `/` delimiter is encouraged to group Sequences by prefix. This is useful in both the UI, where
            Sequences are grouped by folders by `/`-delimited prefixes, and in Searches where a Search can be
            limited to a subset of Sequences by prefix.
        sequence (V1AlphaSequence): Sequence is a single entry containing nucleotides or amino acids and other optional
            metadata like a description, creation time, and taxonomy ID.
    """

    collection: str
    sequence_id: str
    sequence: "V1AlphaSequence"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        collection = self.collection

        sequence_id = self.sequence_id

        sequence = self.sequence.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "collection": collection,
                "sequenceId": sequence_id,
                "sequence": sequence,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.v1_alpha_sequence import V1AlphaSequence

        d = src_dict.copy()
        collection = d.pop("collection")

        sequence_id = d.pop("sequenceId")

        sequence = V1AlphaSequence.from_dict(d.pop("sequence"))

        v1_alpha_create_sequence_request = cls(
            collection=collection,
            sequence_id=sequence_id,
            sequence=sequence,
        )

        v1_alpha_create_sequence_request.additional_properties = d
        return v1_alpha_create_sequence_request

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
