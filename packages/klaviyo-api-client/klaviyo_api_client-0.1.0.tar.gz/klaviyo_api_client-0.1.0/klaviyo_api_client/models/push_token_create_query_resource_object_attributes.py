from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.push_token_create_query_resource_object_attributes_background import (
    PushTokenCreateQueryResourceObjectAttributesBackground,
)
from ..models.push_token_create_query_resource_object_attributes_enablement_status import (
    PushTokenCreateQueryResourceObjectAttributesEnablementStatus,
)
from ..models.push_token_create_query_resource_object_attributes_platform import (
    PushTokenCreateQueryResourceObjectAttributesPlatform,
)
from ..models.push_token_create_query_resource_object_attributes_vendor import (
    PushTokenCreateQueryResourceObjectAttributesVendor,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.device_metadata import DeviceMetadata
    from ..models.push_token_create_query_resource_object_attributes_profile import (
        PushTokenCreateQueryResourceObjectAttributesProfile,
    )


T = TypeVar("T", bound="PushTokenCreateQueryResourceObjectAttributes")


@_attrs_define
class PushTokenCreateQueryResourceObjectAttributes:
    """
    Attributes:
        token (str): A push token from APNS or FCM. Example: 1234567890.
        platform (PushTokenCreateQueryResourceObjectAttributesPlatform): The platform on which the push token was
            created.
        vendor (PushTokenCreateQueryResourceObjectAttributesVendor): The vendor of the push token. Example: APNs.
        profile (PushTokenCreateQueryResourceObjectAttributesProfile): The profile associated with the push token to
            create/update
        enablement_status (Union[Unset, PushTokenCreateQueryResourceObjectAttributesEnablementStatus]): This is the
            enablement status for the individual push token. Default:
            PushTokenCreateQueryResourceObjectAttributesEnablementStatus.AUTHORIZED. Example: AUTHORIZED.
        background (Union[Unset, PushTokenCreateQueryResourceObjectAttributesBackground]): The background state of the
            push token. Default: PushTokenCreateQueryResourceObjectAttributesBackground.AVAILABLE. Example: AVAILABLE.
        device_metadata (Union[Unset, DeviceMetadata]):
    """

    token: str
    platform: PushTokenCreateQueryResourceObjectAttributesPlatform
    vendor: PushTokenCreateQueryResourceObjectAttributesVendor
    profile: "PushTokenCreateQueryResourceObjectAttributesProfile"
    enablement_status: Union[
        Unset, PushTokenCreateQueryResourceObjectAttributesEnablementStatus
    ] = PushTokenCreateQueryResourceObjectAttributesEnablementStatus.AUTHORIZED
    background: Union[
        Unset, PushTokenCreateQueryResourceObjectAttributesBackground
    ] = PushTokenCreateQueryResourceObjectAttributesBackground.AVAILABLE
    device_metadata: Union[Unset, "DeviceMetadata"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        token = self.token

        platform = self.platform.value

        vendor = self.vendor.value

        profile = self.profile.to_dict()

        enablement_status: Union[Unset, str] = UNSET
        if not isinstance(self.enablement_status, Unset):
            enablement_status = self.enablement_status.value

        background: Union[Unset, str] = UNSET
        if not isinstance(self.background, Unset):
            background = self.background.value

        device_metadata: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.device_metadata, Unset):
            device_metadata = self.device_metadata.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "token": token,
                "platform": platform,
                "vendor": vendor,
                "profile": profile,
            }
        )
        if enablement_status is not UNSET:
            field_dict["enablement_status"] = enablement_status
        if background is not UNSET:
            field_dict["background"] = background
        if device_metadata is not UNSET:
            field_dict["device_metadata"] = device_metadata

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.device_metadata import DeviceMetadata
        from ..models.push_token_create_query_resource_object_attributes_profile import (
            PushTokenCreateQueryResourceObjectAttributesProfile,
        )

        d = src_dict.copy()
        token = d.pop("token")

        platform = PushTokenCreateQueryResourceObjectAttributesPlatform(d.pop("platform"))

        vendor = PushTokenCreateQueryResourceObjectAttributesVendor(d.pop("vendor"))

        profile = PushTokenCreateQueryResourceObjectAttributesProfile.from_dict(d.pop("profile"))

        _enablement_status = d.pop("enablement_status", UNSET)
        enablement_status: Union[Unset, PushTokenCreateQueryResourceObjectAttributesEnablementStatus]
        if isinstance(_enablement_status, Unset):
            enablement_status = UNSET
        else:
            enablement_status = PushTokenCreateQueryResourceObjectAttributesEnablementStatus(_enablement_status)

        _background = d.pop("background", UNSET)
        background: Union[Unset, PushTokenCreateQueryResourceObjectAttributesBackground]
        if isinstance(_background, Unset):
            background = UNSET
        else:
            background = PushTokenCreateQueryResourceObjectAttributesBackground(_background)

        _device_metadata = d.pop("device_metadata", UNSET)
        device_metadata: Union[Unset, DeviceMetadata]
        if isinstance(_device_metadata, Unset):
            device_metadata = UNSET
        else:
            device_metadata = DeviceMetadata.from_dict(_device_metadata)

        push_token_create_query_resource_object_attributes = cls(
            token=token,
            platform=platform,
            vendor=vendor,
            profile=profile,
            enablement_status=enablement_status,
            background=background,
            device_metadata=device_metadata,
        )

        push_token_create_query_resource_object_attributes.additional_properties = d
        return push_token_create_query_resource_object_attributes

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
