from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.protobuf_any import ProtobufAny


T = TypeVar("T", bound="RpcStatus")


@_attrs_define
class RpcStatus:
    """The `Status` type defines a logical error model that is suitable for
    different programming environments, including REST APIs and RPC APIs. It is
    used by [gRPC](https://github.com/grpc). Each `Status` message contains
    three pieces of data: error code, error message, and error details.

    You can find out more about this error model and how to work with it in the
    [API Design Guide](https://cloud.google.com/apis/design/errors).

        Attributes:
            code (Union[Unset, int]): The status code, which should be an enum value of
                [google.rpc.Code][google.rpc.Code].
            message (Union[Unset, str]): A developer-facing error message, which should be in English. Any
                user-facing error message should be localized and sent in the
                [google.rpc.Status.details][google.rpc.Status.details] field, or localized
                by the client.
            details (Union[Unset, List['ProtobufAny']]): A list of messages that carry the error details.  There is a common
                set of
                message types for APIs to use.
    """

    code: Union[Unset, int] = UNSET
    message: Union[Unset, str] = UNSET
    details: Union[Unset, List["ProtobufAny"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        code = self.code

        message = self.message

        details: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.details, Unset):
            details = []
            for details_item_data in self.details:
                details_item = details_item_data.to_dict()
                details.append(details_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if code is not UNSET:
            field_dict["code"] = code
        if message is not UNSET:
            field_dict["message"] = message
        if details is not UNSET:
            field_dict["details"] = details

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.protobuf_any import ProtobufAny

        d = src_dict.copy()
        code = d.pop("code", UNSET)

        message = d.pop("message", UNSET)

        details = []
        _details = d.pop("details", UNSET)
        for details_item_data in _details or []:
            details_item = ProtobufAny.from_dict(details_item_data)

            details.append(details_item)

        rpc_status = cls(
            code=code,
            message=message,
            details=details,
        )

        rpc_status.additional_properties = d
        return rpc_status

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
