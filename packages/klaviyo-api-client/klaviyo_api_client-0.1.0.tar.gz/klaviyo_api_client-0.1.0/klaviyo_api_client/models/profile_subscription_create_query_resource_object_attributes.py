from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.subscription_channels import SubscriptionChannels


T = TypeVar("T", bound="ProfileSubscriptionCreateQueryResourceObjectAttributes")


@_attrs_define
class ProfileSubscriptionCreateQueryResourceObjectAttributes:
    """
    Attributes:
        email (Union[Unset, str]): The email address to subscribe or to set on the profile if `channels` is specified
            and the email channel is omitted. Example: matt-kemp@klaviyo-demo.com.
        phone_number (Union[Unset, str]): The phone number to subscribe or to set on the profile if `channels` is
            specified and the SMS channel is omitted. This must be in E.164 format. Example: +15005550006.
        subscriptions (Union[Unset, SubscriptionChannels]):
    """

    email: Union[Unset, str] = UNSET
    phone_number: Union[Unset, str] = UNSET
    subscriptions: Union[Unset, "SubscriptionChannels"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        email = self.email

        phone_number = self.phone_number

        subscriptions: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.subscriptions, Unset):
            subscriptions = self.subscriptions.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if email is not UNSET:
            field_dict["email"] = email
        if phone_number is not UNSET:
            field_dict["phone_number"] = phone_number
        if subscriptions is not UNSET:
            field_dict["subscriptions"] = subscriptions

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.subscription_channels import SubscriptionChannels

        d = src_dict.copy()
        email = d.pop("email", UNSET)

        phone_number = d.pop("phone_number", UNSET)

        _subscriptions = d.pop("subscriptions", UNSET)
        subscriptions: Union[Unset, SubscriptionChannels]
        if isinstance(_subscriptions, Unset):
            subscriptions = UNSET
        else:
            subscriptions = SubscriptionChannels.from_dict(_subscriptions)

        profile_subscription_create_query_resource_object_attributes = cls(
            email=email,
            phone_number=phone_number,
            subscriptions=subscriptions,
        )

        profile_subscription_create_query_resource_object_attributes.additional_properties = d
        return profile_subscription_create_query_resource_object_attributes

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
