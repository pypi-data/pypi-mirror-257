from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.email_channel import EmailChannel
    from ..models.sms_channel import SMSChannel


T = TypeVar("T", bound="Subscriptions")


@_attrs_define
class Subscriptions:
    """
    Attributes:
        email (Union[Unset, EmailChannel]):
        sms (Union[Unset, SMSChannel]):
    """

    email: Union[Unset, "EmailChannel"] = UNSET
    sms: Union[Unset, "SMSChannel"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        email: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.email, Unset):
            email = self.email.to_dict()

        sms: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.sms, Unset):
            sms = self.sms.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if email is not UNSET:
            field_dict["email"] = email
        if sms is not UNSET:
            field_dict["sms"] = sms

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.email_channel import EmailChannel
        from ..models.sms_channel import SMSChannel

        d = src_dict.copy()
        _email = d.pop("email", UNSET)
        email: Union[Unset, EmailChannel]
        if isinstance(_email, Unset):
            email = UNSET
        else:
            email = EmailChannel.from_dict(_email)

        _sms = d.pop("sms", UNSET)
        sms: Union[Unset, SMSChannel]
        if isinstance(_sms, Unset):
            sms = UNSET
        else:
            sms = SMSChannel.from_dict(_sms)

        subscriptions = cls(
            email=email,
            sms=sms,
        )

        subscriptions.additional_properties = d
        return subscriptions

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
