from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.campaign_enum import CampaignEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.campaign_response_object_resource_attributes import CampaignResponseObjectResourceAttributes
    from ..models.get_campaign_response_data_relationships import GetCampaignResponseDataRelationships
    from ..models.object_links import ObjectLinks


T = TypeVar("T", bound="GetCampaignResponseData")


@_attrs_define
class GetCampaignResponseData:
    """
    Attributes:
        type (CampaignEnum):
        id (str): The campaign ID
        attributes (CampaignResponseObjectResourceAttributes):
        links (ObjectLinks):
        relationships (Union[Unset, GetCampaignResponseDataRelationships]):
    """

    type: CampaignEnum
    id: str
    attributes: "CampaignResponseObjectResourceAttributes"
    links: "ObjectLinks"
    relationships: Union[Unset, "GetCampaignResponseDataRelationships"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        id = self.id

        attributes = self.attributes.to_dict()

        links = self.links.to_dict()

        relationships: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.relationships, Unset):
            relationships = self.relationships.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "id": id,
                "attributes": attributes,
                "links": links,
            }
        )
        if relationships is not UNSET:
            field_dict["relationships"] = relationships

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.campaign_response_object_resource_attributes import CampaignResponseObjectResourceAttributes
        from ..models.get_campaign_response_data_relationships import GetCampaignResponseDataRelationships
        from ..models.object_links import ObjectLinks

        d = src_dict.copy()
        type = CampaignEnum(d.pop("type"))

        id = d.pop("id")

        attributes = CampaignResponseObjectResourceAttributes.from_dict(d.pop("attributes"))

        links = ObjectLinks.from_dict(d.pop("links"))

        _relationships = d.pop("relationships", UNSET)
        relationships: Union[Unset, GetCampaignResponseDataRelationships]
        if isinstance(_relationships, Unset):
            relationships = UNSET
        else:
            relationships = GetCampaignResponseDataRelationships.from_dict(_relationships)

        get_campaign_response_data = cls(
            type=type,
            id=id,
            attributes=attributes,
            links=links,
            relationships=relationships,
        )

        get_campaign_response_data.additional_properties = d
        return get_campaign_response_data

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
