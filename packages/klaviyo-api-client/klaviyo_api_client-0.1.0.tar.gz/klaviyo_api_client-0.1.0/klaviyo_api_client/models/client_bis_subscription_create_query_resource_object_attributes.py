from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.client_bis_subscription_create_query_resource_object_attributes_channels_item import (
    ClientBISSubscriptionCreateQueryResourceObjectAttributesChannelsItem,
)

if TYPE_CHECKING:
    from ..models.client_bis_subscription_create_query_resource_object_attributes_profile import (
        ClientBISSubscriptionCreateQueryResourceObjectAttributesProfile,
    )


T = TypeVar("T", bound="ClientBISSubscriptionCreateQueryResourceObjectAttributes")


@_attrs_define
class ClientBISSubscriptionCreateQueryResourceObjectAttributes:
    """
    Attributes:
        channels (List[ClientBISSubscriptionCreateQueryResourceObjectAttributesChannelsItem]): The channel(s) through
            which the profile would like to receive the back in stock notification. This can be leveraged within a back in
            stock flow to notify the subscriber through their preferred channel(s). Example: ['EMAIL', 'SMS'].
        profile (ClientBISSubscriptionCreateQueryResourceObjectAttributesProfile):  Example: {'id':
            '01GDDKASAP8TKDDA2GRZDSVP4H', 'email': 'sarah.mason@klaviyo-demo.com', 'phone_number': '+15005550006',
            'external_id': '63f64a2b-c6bf-40c7-b81f-bed08162edbe'}.
    """

    channels: List[ClientBISSubscriptionCreateQueryResourceObjectAttributesChannelsItem]
    profile: "ClientBISSubscriptionCreateQueryResourceObjectAttributesProfile"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        channels = []
        for channels_item_data in self.channels:
            channels_item = channels_item_data.value
            channels.append(channels_item)

        profile = self.profile.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "channels": channels,
                "profile": profile,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.client_bis_subscription_create_query_resource_object_attributes_profile import (
            ClientBISSubscriptionCreateQueryResourceObjectAttributesProfile,
        )

        d = src_dict.copy()
        channels = []
        _channels = d.pop("channels")
        for channels_item_data in _channels:
            channels_item = ClientBISSubscriptionCreateQueryResourceObjectAttributesChannelsItem(channels_item_data)

            channels.append(channels_item)

        profile = ClientBISSubscriptionCreateQueryResourceObjectAttributesProfile.from_dict(d.pop("profile"))

        client_bis_subscription_create_query_resource_object_attributes = cls(
            channels=channels,
            profile=profile,
        )

        client_bis_subscription_create_query_resource_object_attributes.additional_properties = d
        return client_bis_subscription_create_query_resource_object_attributes

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
