from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sms_marketing import SMSMarketing


T = TypeVar("T", bound="SMSChannel")


@_attrs_define
class SMSChannel:
    """
    Attributes:
        marketing (Union[Unset, SMSMarketing]):
    """

    marketing: Union[Unset, "SMSMarketing"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        marketing: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.marketing, Unset):
            marketing = self.marketing.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if marketing is not UNSET:
            field_dict["marketing"] = marketing

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.sms_marketing import SMSMarketing

        d = src_dict.copy()
        _marketing = d.pop("marketing", UNSET)
        marketing: Union[Unset, SMSMarketing]
        if isinstance(_marketing, Unset):
            marketing = UNSET
        else:
            marketing = SMSMarketing.from_dict(_marketing)

        sms_channel = cls(
            marketing=marketing,
        )

        sms_channel.additional_properties = d
        return sms_channel

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
