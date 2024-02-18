from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v1_alpha_integration import V1AlphaIntegration


T = TypeVar("T", bound="V1AlphaListIntegrationsResponse")


@_attrs_define
class V1AlphaListIntegrationsResponse:
    """ListIntegrationsResponse holds a list of integrations.

    Attributes:
        integrations (Union[Unset, List['V1AlphaIntegration']]): A list of Integrations in the Collection.
        next_page_token (Union[Unset, str]): A token to retrieve the next page of Integrations.
    """

    integrations: Union[Unset, List["V1AlphaIntegration"]] = UNSET
    next_page_token: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        integrations: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.integrations, Unset):
            integrations = []
            for integrations_item_data in self.integrations:
                integrations_item = integrations_item_data.to_dict()
                integrations.append(integrations_item)

        next_page_token = self.next_page_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if integrations is not UNSET:
            field_dict["integrations"] = integrations
        if next_page_token is not UNSET:
            field_dict["nextPageToken"] = next_page_token

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.v1_alpha_integration import V1AlphaIntegration

        d = src_dict.copy()
        integrations = []
        _integrations = d.pop("integrations", UNSET)
        for integrations_item_data in _integrations or []:
            integrations_item = V1AlphaIntegration.from_dict(integrations_item_data)

            integrations.append(integrations_item)

        next_page_token = d.pop("nextPageToken", UNSET)

        v1_alpha_list_integrations_response = cls(
            integrations=integrations,
            next_page_token=next_page_token,
        )

        v1_alpha_list_integrations_response.additional_properties = d
        return v1_alpha_list_integrations_response

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
