from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v1_alpha_integration_google_drive import V1AlphaIntegrationGoogleDrive
    from ..models.v1_alpha_integration_ncbi import V1AlphaIntegrationNCBI


T = TypeVar("T", bound="TheIntegrationToUpdate")


@_attrs_define
class TheIntegrationToUpdate:
    """
    Attributes:
        collection (str): The name of the Collection that the Integration imports Sequences to. Format is
            `collections/{collection_id}`.
        sequence_id_prefix (Union[Unset, str]): A prefix that is prepended to all Sequence IDs added to the Collection.

            For example, if "proteins/flourescent" is imported to a Collection "my-collection", and a Sequence with an ID of
            "GFP" is imported, the Sequence name will be "collections/my-collection/sequences/proteins/flourescent/GFP".
        etag (Union[Unset, str]): An opaque, server-assigned value that is the hash of all fields in the Integration.
            Each change to an integration changes the Etag value.
        ncbi (Union[Unset, V1AlphaIntegrationNCBI]): NCBI integration.
        google_drive (Union[Unset, V1AlphaIntegrationGoogleDrive]): Google Drive integration.
    """

    collection: str
    sequence_id_prefix: Union[Unset, str] = UNSET
    etag: Union[Unset, str] = UNSET
    ncbi: Union[Unset, "V1AlphaIntegrationNCBI"] = UNSET
    google_drive: Union[Unset, "V1AlphaIntegrationGoogleDrive"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        collection = self.collection

        sequence_id_prefix = self.sequence_id_prefix

        etag = self.etag

        ncbi: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.ncbi, Unset):
            ncbi = self.ncbi.to_dict()

        google_drive: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.google_drive, Unset):
            google_drive = self.google_drive.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "collection": collection,
            }
        )
        if sequence_id_prefix is not UNSET:
            field_dict["sequenceIdPrefix"] = sequence_id_prefix
        if etag is not UNSET:
            field_dict["etag"] = etag
        if ncbi is not UNSET:
            field_dict["ncbi"] = ncbi
        if google_drive is not UNSET:
            field_dict["googleDrive"] = google_drive

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.v1_alpha_integration_google_drive import V1AlphaIntegrationGoogleDrive
        from ..models.v1_alpha_integration_ncbi import V1AlphaIntegrationNCBI

        d = src_dict.copy()
        collection = d.pop("collection")

        sequence_id_prefix = d.pop("sequenceIdPrefix", UNSET)

        etag = d.pop("etag", UNSET)

        _ncbi = d.pop("ncbi", UNSET)
        ncbi: Union[Unset, V1AlphaIntegrationNCBI]
        if isinstance(_ncbi, Unset):
            ncbi = UNSET
        else:
            ncbi = V1AlphaIntegrationNCBI.from_dict(_ncbi)

        _google_drive = d.pop("googleDrive", UNSET)
        google_drive: Union[Unset, V1AlphaIntegrationGoogleDrive]
        if isinstance(_google_drive, Unset):
            google_drive = UNSET
        else:
            google_drive = V1AlphaIntegrationGoogleDrive.from_dict(_google_drive)

        the_integration_to_update = cls(
            collection=collection,
            sequence_id_prefix=sequence_id_prefix,
            etag=etag,
            ncbi=ncbi,
            google_drive=google_drive,
        )

        the_integration_to_update.additional_properties = d
        return the_integration_to_update

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
