from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.server_bis_subscription_create_query_resource_object_attributes_channels_item import (
    ServerBISSubscriptionCreateQueryResourceObjectAttributesChannelsItem,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.server_bis_subscription_create_query_resource_object_attributes_profile import (
        ServerBISSubscriptionCreateQueryResourceObjectAttributesProfile,
    )


T = TypeVar("T", bound="ServerBISSubscriptionCreateQueryResourceObjectAttributes")


@_attrs_define
class ServerBISSubscriptionCreateQueryResourceObjectAttributes:
    """
    Attributes:
        channels (List[ServerBISSubscriptionCreateQueryResourceObjectAttributesChannelsItem]): The channel(s) through
            which the profile would like to receive the back in stock notification. This can be leveraged within a back in
            stock flow to notify the subscriber through their preferred channel(s). Example: ['EMAIL', 'SMS'].
        profile (Union[Unset, ServerBISSubscriptionCreateQueryResourceObjectAttributesProfile]):  Example: {'id':
            '01GDDKASAP8TKDDA2GRZDSVP4H', 'email': 'sarah.mason@klaviyo-demo.com', 'phone_number': '+15005550006',
            'external_id': '63f64a2b-c6bf-40c7-b81f-bed08162edbe'}.
    """

    channels: List[ServerBISSubscriptionCreateQueryResourceObjectAttributesChannelsItem]
    profile: Union[Unset, "ServerBISSubscriptionCreateQueryResourceObjectAttributesProfile"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        channels = []
        for channels_item_data in self.channels:
            channels_item = channels_item_data.value
            channels.append(channels_item)

        profile: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.profile, Unset):
            profile = self.profile.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "channels": channels,
            }
        )
        if profile is not UNSET:
            field_dict["profile"] = profile

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.server_bis_subscription_create_query_resource_object_attributes_profile import (
            ServerBISSubscriptionCreateQueryResourceObjectAttributesProfile,
        )

        d = src_dict.copy()
        channels = []
        _channels = d.pop("channels")
        for channels_item_data in _channels:
            channels_item = ServerBISSubscriptionCreateQueryResourceObjectAttributesChannelsItem(channels_item_data)

            channels.append(channels_item)

        _profile = d.pop("profile", UNSET)
        profile: Union[Unset, ServerBISSubscriptionCreateQueryResourceObjectAttributesProfile]
        if isinstance(_profile, Unset):
            profile = UNSET
        else:
            profile = ServerBISSubscriptionCreateQueryResourceObjectAttributesProfile.from_dict(_profile)

        server_bis_subscription_create_query_resource_object_attributes = cls(
            channels=channels,
            profile=profile,
        )

        server_bis_subscription_create_query_resource_object_attributes.additional_properties = d
        return server_bis_subscription_create_query_resource_object_attributes

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
