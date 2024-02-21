from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.email_subscription_parameters import EmailSubscriptionParameters
    from ..models.sms_subscription_parameters import SMSSubscriptionParameters


T = TypeVar("T", bound="SubscriptionChannels")


@_attrs_define
class SubscriptionChannels:
    """
    Attributes:
        email (Union[Unset, EmailSubscriptionParameters]):
        sms (Union[Unset, SMSSubscriptionParameters]):
    """

    email: Union[Unset, "EmailSubscriptionParameters"] = UNSET
    sms: Union[Unset, "SMSSubscriptionParameters"] = UNSET
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
        from ..models.email_subscription_parameters import EmailSubscriptionParameters
        from ..models.sms_subscription_parameters import SMSSubscriptionParameters

        d = src_dict.copy()
        _email = d.pop("email", UNSET)
        email: Union[Unset, EmailSubscriptionParameters]
        if isinstance(_email, Unset):
            email = UNSET
        else:
            email = EmailSubscriptionParameters.from_dict(_email)

        _sms = d.pop("sms", UNSET)
        sms: Union[Unset, SMSSubscriptionParameters]
        if isinstance(_sms, Unset):
            sms = UNSET
        else:
            sms = SMSSubscriptionParameters.from_dict(_sms)

        subscription_channels = cls(
            email=email,
            sms=sms,
        )

        subscription_channels.additional_properties = d
        return subscription_channels

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
