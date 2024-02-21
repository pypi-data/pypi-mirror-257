from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.post_tag_response_data_relationships_campaigns_data_item import (
        PostTagResponseDataRelationshipsCampaignsDataItem,
    )
    from ..models.relationship_links import RelationshipLinks


T = TypeVar("T", bound="PostTagResponseDataRelationshipsCampaigns")


@_attrs_define
class PostTagResponseDataRelationshipsCampaigns:
    """
    Attributes:
        data (List['PostTagResponseDataRelationshipsCampaignsDataItem']):
        links (Union[Unset, RelationshipLinks]):
    """

    data: List["PostTagResponseDataRelationshipsCampaignsDataItem"]
    links: Union[Unset, "RelationshipLinks"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)

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
        from ..models.post_tag_response_data_relationships_campaigns_data_item import (
            PostTagResponseDataRelationshipsCampaignsDataItem,
        )
        from ..models.relationship_links import RelationshipLinks

        d = src_dict.copy()
        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = PostTagResponseDataRelationshipsCampaignsDataItem.from_dict(data_item_data)

            data.append(data_item)

        _links = d.pop("links", UNSET)
        links: Union[Unset, RelationshipLinks]
        if isinstance(_links, Unset):
            links = UNSET
        else:
            links = RelationshipLinks.from_dict(_links)

        post_tag_response_data_relationships_campaigns = cls(
            data=data,
            links=links,
        )

        post_tag_response_data_relationships_campaigns.additional_properties = d
        return post_tag_response_data_relationships_campaigns

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
