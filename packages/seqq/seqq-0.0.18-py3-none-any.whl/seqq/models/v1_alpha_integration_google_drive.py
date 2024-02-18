from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="V1AlphaIntegrationGoogleDrive")


@_attrs_define
class V1AlphaIntegrationGoogleDrive:
    """Google Drive integration.

    Attributes:
        service_account_credentials (Union[Unset, str]): Base64 encoded credentials for the service account authorized
            to list sequences in Google Drive.
    """

    service_account_credentials: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        service_account_credentials = self.service_account_credentials

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if service_account_credentials is not UNSET:
            field_dict["serviceAccountCredentials"] = service_account_credentials

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        service_account_credentials = d.pop("serviceAccountCredentials", UNSET)

        v1_alpha_integration_google_drive = cls(
            service_account_credentials=service_account_credentials,
        )

        v1_alpha_integration_google_drive.additional_properties = d
        return v1_alpha_integration_google_drive

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
