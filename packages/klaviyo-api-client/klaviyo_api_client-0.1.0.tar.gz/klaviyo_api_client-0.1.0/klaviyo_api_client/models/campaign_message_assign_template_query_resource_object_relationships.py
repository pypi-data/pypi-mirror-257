from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.campaign_message_assign_template_query_resource_object_relationships_template import (
        CampaignMessageAssignTemplateQueryResourceObjectRelationshipsTemplate,
    )


T = TypeVar("T", bound="CampaignMessageAssignTemplateQueryResourceObjectRelationships")


@_attrs_define
class CampaignMessageAssignTemplateQueryResourceObjectRelationships:
    """
    Attributes:
        template (CampaignMessageAssignTemplateQueryResourceObjectRelationshipsTemplate):
    """

    template: "CampaignMessageAssignTemplateQueryResourceObjectRelationshipsTemplate"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        template = self.template.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "template": template,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.campaign_message_assign_template_query_resource_object_relationships_template import (
            CampaignMessageAssignTemplateQueryResourceObjectRelationshipsTemplate,
        )

        d = src_dict.copy()
        template = CampaignMessageAssignTemplateQueryResourceObjectRelationshipsTemplate.from_dict(d.pop("template"))

        campaign_message_assign_template_query_resource_object_relationships = cls(
            template=template,
        )

        campaign_message_assign_template_query_resource_object_relationships.additional_properties = d
        return campaign_message_assign_template_query_resource_object_relationships

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
