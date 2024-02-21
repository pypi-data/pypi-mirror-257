from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.profile_enum import ProfileEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.profile_subscription_create_query_resource_object_attributes import (
        ProfileSubscriptionCreateQueryResourceObjectAttributes,
    )


T = TypeVar("T", bound="ProfileSubscriptionCreateQueryResourceObject")


@_attrs_define
class ProfileSubscriptionCreateQueryResourceObject:
    """
    Attributes:
        type (ProfileEnum):
        attributes (ProfileSubscriptionCreateQueryResourceObjectAttributes):
        id (Union[Unset, str]): The ID of the profile to subscribe. If provided, this will be used to perform the
            lookup. Example: 01GDDKASAP8TKDDA2GRZDSVP4H.
    """

    type: ProfileEnum
    attributes: "ProfileSubscriptionCreateQueryResourceObjectAttributes"
    id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        attributes = self.attributes.to_dict()

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "attributes": attributes,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.profile_subscription_create_query_resource_object_attributes import (
            ProfileSubscriptionCreateQueryResourceObjectAttributes,
        )

        d = src_dict.copy()
        type = ProfileEnum(d.pop("type"))

        attributes = ProfileSubscriptionCreateQueryResourceObjectAttributes.from_dict(d.pop("attributes"))

        id = d.pop("id", UNSET)

        profile_subscription_create_query_resource_object = cls(
            type=type,
            attributes=attributes,
            id=id,
        )

        profile_subscription_create_query_resource_object.additional_properties = d
        return profile_subscription_create_query_resource_object

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
