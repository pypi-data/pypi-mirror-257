from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.campaign_message_assign_template_query_resource_object import (
        CampaignMessageAssignTemplateQueryResourceObject,
    )


T = TypeVar("T", bound="CampaignMessageAssignTemplateQuery")


@_attrs_define
class CampaignMessageAssignTemplateQuery:
    """
    Attributes:
        data (CampaignMessageAssignTemplateQueryResourceObject):
    """

    data: "CampaignMessageAssignTemplateQueryResourceObject"
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
        from ..models.campaign_message_assign_template_query_resource_object import (
            CampaignMessageAssignTemplateQueryResourceObject,
        )

        d = src_dict.copy()
        data = CampaignMessageAssignTemplateQueryResourceObject.from_dict(d.pop("data"))

        campaign_message_assign_template_query = cls(
            data=data,
        )

        campaign_message_assign_template_query.additional_properties = d
        return campaign_message_assign_template_query

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
