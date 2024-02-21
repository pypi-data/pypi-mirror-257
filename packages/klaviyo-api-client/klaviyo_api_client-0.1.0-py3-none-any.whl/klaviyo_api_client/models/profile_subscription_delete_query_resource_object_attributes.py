from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProfileSubscriptionDeleteQueryResourceObjectAttributes")


@_attrs_define
class ProfileSubscriptionDeleteQueryResourceObjectAttributes:
    """
    Attributes:
        email (Union[Unset, str]): The email address to unsubscribe. Example: matt-kemp@klaviyo-demo.com.
        phone_number (Union[Unset, str]): The phone number to unsubscribe. This must be in E.164 format. Example:
            +15005550006.
    """

    email: Union[Unset, str] = UNSET
    phone_number: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        email = self.email

        phone_number = self.phone_number

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if email is not UNSET:
            field_dict["email"] = email
        if phone_number is not UNSET:
            field_dict["phone_number"] = phone_number

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        email = d.pop("email", UNSET)

        phone_number = d.pop("phone_number", UNSET)

        profile_subscription_delete_query_resource_object_attributes = cls(
            email=email,
            phone_number=phone_number,
        )

        profile_subscription_delete_query_resource_object_attributes.additional_properties = d
        return profile_subscription_delete_query_resource_object_attributes

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
