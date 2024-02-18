from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="V1AlphaIntegrationNCBIUploads")


@_attrs_define
class V1AlphaIntegrationNCBIUploads:
    """A map from file name to the count of sequences uploaded from that file.
    Files do not change in NCBI. This field is set by the server so integrations
    can skip sequence uploading if the sequences has already been uploaded. These
    are set when we fail to upload a single sequence within the file.

    """

    additional_properties: Dict[str, str] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        v1_alpha_integration_ncbi_uploads = cls()

        v1_alpha_integration_ncbi_uploads.additional_properties = d
        return v1_alpha_integration_ncbi_uploads

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> str:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: str) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
