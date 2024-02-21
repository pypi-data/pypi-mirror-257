from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EmailSendOptionsSubObject")


@_attrs_define
class EmailSendOptionsSubObject:
    """
    Attributes:
        use_smart_sending (Union[Unset, bool]): Use smart sending. Defaults to True
    """

    use_smart_sending: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        use_smart_sending = self.use_smart_sending

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if use_smart_sending is not UNSET:
            field_dict["use_smart_sending"] = use_smart_sending

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        use_smart_sending = d.pop("use_smart_sending", UNSET)

        email_send_options_sub_object = cls(
            use_smart_sending=use_smart_sending,
        )

        email_send_options_sub_object.additional_properties = d
        return email_send_options_sub_object

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
