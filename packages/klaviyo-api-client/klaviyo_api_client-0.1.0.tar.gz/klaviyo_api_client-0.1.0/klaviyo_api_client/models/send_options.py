from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SendOptions")


@_attrs_define
class SendOptions:
    """
    Attributes:
        use_smart_sending (bool):
        is_transactional (bool):
    """

    use_smart_sending: bool
    is_transactional: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        use_smart_sending = self.use_smart_sending

        is_transactional = self.is_transactional

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "use_smart_sending": use_smart_sending,
                "is_transactional": is_transactional,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        use_smart_sending = d.pop("use_smart_sending")

        is_transactional = d.pop("is_transactional")

        send_options = cls(
            use_smart_sending=use_smart_sending,
            is_transactional=is_transactional,
        )

        send_options.additional_properties = d
        return send_options

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
