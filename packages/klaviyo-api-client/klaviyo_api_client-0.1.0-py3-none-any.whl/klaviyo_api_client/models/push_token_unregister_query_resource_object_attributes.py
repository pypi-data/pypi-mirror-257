from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.push_token_unregister_query_resource_object_attributes_platform import (
    PushTokenUnregisterQueryResourceObjectAttributesPlatform,
)
from ..models.push_token_unregister_query_resource_object_attributes_vendor import (
    PushTokenUnregisterQueryResourceObjectAttributesVendor,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.push_token_unregister_query_resource_object_attributes_profile import (
        PushTokenUnregisterQueryResourceObjectAttributesProfile,
    )


T = TypeVar("T", bound="PushTokenUnregisterQueryResourceObjectAttributes")


@_attrs_define
class PushTokenUnregisterQueryResourceObjectAttributes:
    """
    Attributes:
        token (str): A push token from APNS or FCM. Example: 1234567890.
        platform (PushTokenUnregisterQueryResourceObjectAttributesPlatform): The platform on which the push token was
            created.
        profile (PushTokenUnregisterQueryResourceObjectAttributesProfile): The profile associated with the push token to
            create/update
        vendor (Union[Unset, PushTokenUnregisterQueryResourceObjectAttributesVendor]): The vendor of the push token.
            Example: apns.
    """

    token: str
    platform: PushTokenUnregisterQueryResourceObjectAttributesPlatform
    profile: "PushTokenUnregisterQueryResourceObjectAttributesProfile"
    vendor: Union[Unset, PushTokenUnregisterQueryResourceObjectAttributesVendor] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        token = self.token

        platform = self.platform.value

        profile = self.profile.to_dict()

        vendor: Union[Unset, str] = UNSET
        if not isinstance(self.vendor, Unset):
            vendor = self.vendor.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "token": token,
                "platform": platform,
                "profile": profile,
            }
        )
        if vendor is not UNSET:
            field_dict["vendor"] = vendor

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.push_token_unregister_query_resource_object_attributes_profile import (
            PushTokenUnregisterQueryResourceObjectAttributesProfile,
        )

        d = src_dict.copy()
        token = d.pop("token")

        platform = PushTokenUnregisterQueryResourceObjectAttributesPlatform(d.pop("platform"))

        profile = PushTokenUnregisterQueryResourceObjectAttributesProfile.from_dict(d.pop("profile"))

        _vendor = d.pop("vendor", UNSET)
        vendor: Union[Unset, PushTokenUnregisterQueryResourceObjectAttributesVendor]
        if isinstance(_vendor, Unset):
            vendor = UNSET
        else:
            vendor = PushTokenUnregisterQueryResourceObjectAttributesVendor(_vendor)

        push_token_unregister_query_resource_object_attributes = cls(
            token=token,
            platform=platform,
            profile=profile,
            vendor=vendor,
        )

        push_token_unregister_query_resource_object_attributes.additional_properties = d
        return push_token_unregister_query_resource_object_attributes

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
