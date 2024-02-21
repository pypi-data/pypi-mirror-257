from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.attribution_response_object_resource_relationships_campaign_message_data import (
        AttributionResponseObjectResourceRelationshipsCampaignMessageData,
    )


T = TypeVar("T", bound="AttributionResponseObjectResourceRelationshipsCampaignMessage")


@_attrs_define
class AttributionResponseObjectResourceRelationshipsCampaignMessage:
    """
    Attributes:
        data (AttributionResponseObjectResourceRelationshipsCampaignMessageData):
    """

    data: "AttributionResponseObjectResourceRelationshipsCampaignMessageData"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = self.data.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.attribution_response_object_resource_relationships_campaign_message_data import (
            AttributionResponseObjectResourceRelationshipsCampaignMessageData,
        )

        d = src_dict.copy()
        data = AttributionResponseObjectResourceRelationshipsCampaignMessageData.from_dict(d.pop("data"))

        attribution_response_object_resource_relationships_campaign_message = cls(
            data=data,
        )

        attribution_response_object_resource_relationships_campaign_message.additional_properties = d
        return attribution_response_object_resource_relationships_campaign_message

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
