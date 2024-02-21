from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.subscription_create_job_create_query_resource_object_attributes_profiles import (
        SubscriptionCreateJobCreateQueryResourceObjectAttributesProfiles,
    )


T = TypeVar("T", bound="SubscriptionCreateJobCreateQueryResourceObjectAttributes")


@_attrs_define
class SubscriptionCreateJobCreateQueryResourceObjectAttributes:
    """
    Attributes:
        profiles (SubscriptionCreateJobCreateQueryResourceObjectAttributesProfiles): The profile(s) to subscribe
        custom_source (Union[Unset, str]): A custom method detail or source to store on the consent records. Example:
            Marketing Event.
    """

    profiles: "SubscriptionCreateJobCreateQueryResourceObjectAttributesProfiles"
    custom_source: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        profiles = self.profiles.to_dict()

        custom_source = self.custom_source

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "profiles": profiles,
            }
        )
        if custom_source is not UNSET:
            field_dict["custom_source"] = custom_source

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.subscription_create_job_create_query_resource_object_attributes_profiles import (
            SubscriptionCreateJobCreateQueryResourceObjectAttributesProfiles,
        )

        d = src_dict.copy()
        profiles = SubscriptionCreateJobCreateQueryResourceObjectAttributesProfiles.from_dict(d.pop("profiles"))

        custom_source = d.pop("custom_source", UNSET)

        subscription_create_job_create_query_resource_object_attributes = cls(
            profiles=profiles,
            custom_source=custom_source,
        )

        subscription_create_job_create_query_resource_object_attributes.additional_properties = d
        return subscription_create_job_create_query_resource_object_attributes

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
