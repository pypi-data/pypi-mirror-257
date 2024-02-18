from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v1_alpha_search import V1AlphaSearch


T = TypeVar("T", bound="V1AlphaListSearchesResponse")


@_attrs_define
class V1AlphaListSearchesResponse:
    """ListSearchesResponse is the response message for ListSequences.

    Attributes:
        searches (Union[Unset, List['V1AlphaSearch']]): A list of Searches.
        next_page_token (Union[Unset, str]): Next page token is the token to use to retrieve the next page of results.
    """

    searches: Union[Unset, List["V1AlphaSearch"]] = UNSET
    next_page_token: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        searches: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.searches, Unset):
            searches = []
            for searches_item_data in self.searches:
                searches_item = searches_item_data.to_dict()
                searches.append(searches_item)

        next_page_token = self.next_page_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if searches is not UNSET:
            field_dict["searches"] = searches
        if next_page_token is not UNSET:
            field_dict["nextPageToken"] = next_page_token

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.v1_alpha_search import V1AlphaSearch

        d = src_dict.copy()
        searches = []
        _searches = d.pop("searches", UNSET)
        for searches_item_data in _searches or []:
            searches_item = V1AlphaSearch.from_dict(searches_item_data)

            searches.append(searches_item)

        next_page_token = d.pop("nextPageToken", UNSET)

        v1_alpha_list_searches_response = cls(
            searches=searches,
            next_page_token=next_page_token,
        )

        v1_alpha_list_searches_response.additional_properties = d
        return v1_alpha_list_searches_response

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
