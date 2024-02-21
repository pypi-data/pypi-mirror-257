from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_campaign_message_response_compound_document_data_relationships_template_data import (
        GetCampaignMessageResponseCompoundDocumentDataRelationshipsTemplateData,
    )
    from ..models.relationship_links import RelationshipLinks


T = TypeVar("T", bound="GetCampaignMessageResponseCompoundDocumentDataRelationshipsTemplate")


@_attrs_define
class GetCampaignMessageResponseCompoundDocumentDataRelationshipsTemplate:
    """
    Attributes:
        data (GetCampaignMessageResponseCompoundDocumentDataRelationshipsTemplateData):
        links (Union[Unset, RelationshipLinks]):
    """

    data: "GetCampaignMessageResponseCompoundDocumentDataRelationshipsTemplateData"
    links: Union[Unset, "RelationshipLinks"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = self.data.to_dict()

        links: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.links, Unset):
            links = self.links.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
            }
        )
        if links is not UNSET:
            field_dict["links"] = links

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_campaign_message_response_compound_document_data_relationships_template_data import (
            GetCampaignMessageResponseCompoundDocumentDataRelationshipsTemplateData,
        )
        from ..models.relationship_links import RelationshipLinks

        d = src_dict.copy()
        data = GetCampaignMessageResponseCompoundDocumentDataRelationshipsTemplateData.from_dict(d.pop("data"))

        _links = d.pop("links", UNSET)
        links: Union[Unset, RelationshipLinks]
        if isinstance(_links, Unset):
            links = UNSET
        else:
            links = RelationshipLinks.from_dict(_links)

        get_campaign_message_response_compound_document_data_relationships_template = cls(
            data=data,
            links=links,
        )

        get_campaign_message_response_compound_document_data_relationships_template.additional_properties = d
        return get_campaign_message_response_compound_document_data_relationships_template

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
