from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="V1AlphaCollection")


@_attrs_define
class V1AlphaCollection:
    """Collections contain Sequences, Searches, and Integration.

    Attributes:
        name (Union[Unset, str]): A globally unique name for the Collection. Format is `collections/{collection_id}`
            where `collection_id`
            is set during creation. This is not modifiable.
        display_name (Union[Unset, str]): Display name of the collection in the UI. This can differ from `name`. If set,
            this is used in place of `collection_id` in the UI.
    """

    name: Union[Unset, str] = UNSET
    display_name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        display_name = self.display_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if display_name is not UNSET:
            field_dict["displayName"] = display_name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        display_name = d.pop("displayName", UNSET)

        v1_alpha_collection = cls(
            name=name,
            display_name=display_name,
        )

        v1_alpha_collection.additional_properties = d
        return v1_alpha_collection

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
