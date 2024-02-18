from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v1_alpha_collection import V1AlphaCollection


T = TypeVar("T", bound="V1AlphaListCollectionsResponse")


@_attrs_define
class V1AlphaListCollectionsResponse:
    """ListCollectionsResponse is the response message for ListCollections.

    Attributes:
        collections (Union[Unset, List['V1AlphaCollection']]): Collections ordered by their name.
        next_page_token (Union[Unset, str]): A token to retrieve the next page of results. This is an opaque value that
            should not be parsed. If this is unset, there
            are no more collections to list.
    """

    collections: Union[Unset, List["V1AlphaCollection"]] = UNSET
    next_page_token: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        collections: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.collections, Unset):
            collections = []
            for collections_item_data in self.collections:
                collections_item = collections_item_data.to_dict()
                collections.append(collections_item)

        next_page_token = self.next_page_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if collections is not UNSET:
            field_dict["collections"] = collections
        if next_page_token is not UNSET:
            field_dict["nextPageToken"] = next_page_token

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.v1_alpha_collection import V1AlphaCollection

        d = src_dict.copy()
        collections = []
        _collections = d.pop("collections", UNSET)
        for collections_item_data in _collections or []:
            collections_item = V1AlphaCollection.from_dict(collections_item_data)

            collections.append(collections_item)

        next_page_token = d.pop("nextPageToken", UNSET)

        v1_alpha_list_collections_response = cls(
            collections=collections,
            next_page_token=next_page_token,
        )

        v1_alpha_list_collections_response.additional_properties = d
        return v1_alpha_list_collections_response

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
