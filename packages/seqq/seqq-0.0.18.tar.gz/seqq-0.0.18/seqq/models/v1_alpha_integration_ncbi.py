from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v1_alpha_integration_ncbi_uploads import V1AlphaIntegrationNCBIUploads


T = TypeVar("T", bound="V1AlphaIntegrationNCBI")


@_attrs_define
class V1AlphaIntegrationNCBI:
    """NCBI integration.

    Attributes:
        manifest (str): The URL of an NCBI manifest to import Sequences from. These are from the BLAST FTP website.
            For example, "https://ftp.ncbi.nlm.nih.gov/blast/db/taxdb-metadata.json" imports Sequences from
            the NCBI Taxonomy database.
        uploads (Union[Unset, V1AlphaIntegrationNCBIUploads]): A map from file name to the count of sequences uploaded
            from that file.
            Files do not change in NCBI. This field is set by the server so integrations
            can skip sequence uploading if the sequences has already been uploaded. These
            are set when we fail to upload a single sequence within the file.
    """

    manifest: str
    uploads: Union[Unset, "V1AlphaIntegrationNCBIUploads"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        manifest = self.manifest

        uploads: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.uploads, Unset):
            uploads = self.uploads.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "manifest": manifest,
            }
        )
        if uploads is not UNSET:
            field_dict["uploads"] = uploads

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.v1_alpha_integration_ncbi_uploads import V1AlphaIntegrationNCBIUploads

        d = src_dict.copy()
        manifest = d.pop("manifest")

        _uploads = d.pop("uploads", UNSET)
        uploads: Union[Unset, V1AlphaIntegrationNCBIUploads]
        if isinstance(_uploads, Unset):
            uploads = UNSET
        else:
            uploads = V1AlphaIntegrationNCBIUploads.from_dict(_uploads)

        v1_alpha_integration_ncbi = cls(
            manifest=manifest,
            uploads=uploads,
        )

        v1_alpha_integration_ncbi.additional_properties = d
        return v1_alpha_integration_ncbi

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
