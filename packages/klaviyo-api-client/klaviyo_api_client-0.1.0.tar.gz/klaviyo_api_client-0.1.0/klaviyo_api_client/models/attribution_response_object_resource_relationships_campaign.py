from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.attribution_response_object_resource_relationships_campaign_data import (
        AttributionResponseObjectResourceRelationshipsCampaignData,
    )


T = TypeVar("T", bound="AttributionResponseObjectResourceRelationshipsCampaign")


@_attrs_define
class AttributionResponseObjectResourceRelationshipsCampaign:
    """
    Attributes:
        data (AttributionResponseObjectResourceRelationshipsCampaignData):
    """

    data: "AttributionResponseObjectResourceRelationshipsCampaignData"
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
        from ..models.attribution_response_object_resource_relationships_campaign_data import (
            AttributionResponseObjectResourceRelationshipsCampaignData,
        )

        d = src_dict.copy()
        data = AttributionResponseObjectResourceRelationshipsCampaignData.from_dict(d.pop("data"))

        attribution_response_object_resource_relationships_campaign = cls(
            data=data,
        )

        attribution_response_object_resource_relationships_campaign.additional_properties = d
        return attribution_response_object_resource_relationships_campaign

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
