from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.post_tag_response_data_relationships_campaigns import PostTagResponseDataRelationshipsCampaigns
    from ..models.post_tag_response_data_relationships_flows import PostTagResponseDataRelationshipsFlows
    from ..models.post_tag_response_data_relationships_lists import PostTagResponseDataRelationshipsLists
    from ..models.post_tag_response_data_relationships_segments import PostTagResponseDataRelationshipsSegments
    from ..models.post_tag_response_data_relationships_tag_group import PostTagResponseDataRelationshipsTagGroup


T = TypeVar("T", bound="PostTagResponseDataRelationships")


@_attrs_define
class PostTagResponseDataRelationships:
    """
    Attributes:
        tag_group (Union[Unset, PostTagResponseDataRelationshipsTagGroup]):
        lists (Union[Unset, PostTagResponseDataRelationshipsLists]):
        segments (Union[Unset, PostTagResponseDataRelationshipsSegments]):
        campaigns (Union[Unset, PostTagResponseDataRelationshipsCampaigns]):
        flows (Union[Unset, PostTagResponseDataRelationshipsFlows]):
    """

    tag_group: Union[Unset, "PostTagResponseDataRelationshipsTagGroup"] = UNSET
    lists: Union[Unset, "PostTagResponseDataRelationshipsLists"] = UNSET
    segments: Union[Unset, "PostTagResponseDataRelationshipsSegments"] = UNSET
    campaigns: Union[Unset, "PostTagResponseDataRelationshipsCampaigns"] = UNSET
    flows: Union[Unset, "PostTagResponseDataRelationshipsFlows"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        tag_group: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.tag_group, Unset):
            tag_group = self.tag_group.to_dict()

        lists: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.lists, Unset):
            lists = self.lists.to_dict()

        segments: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.segments, Unset):
            segments = self.segments.to_dict()

        campaigns: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.campaigns, Unset):
            campaigns = self.campaigns.to_dict()

        flows: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.flows, Unset):
            flows = self.flows.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if tag_group is not UNSET:
            field_dict["tag-group"] = tag_group
        if lists is not UNSET:
            field_dict["lists"] = lists
        if segments is not UNSET:
            field_dict["segments"] = segments
        if campaigns is not UNSET:
            field_dict["campaigns"] = campaigns
        if flows is not UNSET:
            field_dict["flows"] = flows

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.post_tag_response_data_relationships_campaigns import PostTagResponseDataRelationshipsCampaigns
        from ..models.post_tag_response_data_relationships_flows import PostTagResponseDataRelationshipsFlows
        from ..models.post_tag_response_data_relationships_lists import PostTagResponseDataRelationshipsLists
        from ..models.post_tag_response_data_relationships_segments import PostTagResponseDataRelationshipsSegments
        from ..models.post_tag_response_data_relationships_tag_group import PostTagResponseDataRelationshipsTagGroup

        d = src_dict.copy()
        _tag_group = d.pop("tag-group", UNSET)
        tag_group: Union[Unset, PostTagResponseDataRelationshipsTagGroup]
        if isinstance(_tag_group, Unset):
            tag_group = UNSET
        else:
            tag_group = PostTagResponseDataRelationshipsTagGroup.from_dict(_tag_group)

        _lists = d.pop("lists", UNSET)
        lists: Union[Unset, PostTagResponseDataRelationshipsLists]
        if isinstance(_lists, Unset):
            lists = UNSET
        else:
            lists = PostTagResponseDataRelationshipsLists.from_dict(_lists)

        _segments = d.pop("segments", UNSET)
        segments: Union[Unset, PostTagResponseDataRelationshipsSegments]
        if isinstance(_segments, Unset):
            segments = UNSET
        else:
            segments = PostTagResponseDataRelationshipsSegments.from_dict(_segments)

        _campaigns = d.pop("campaigns", UNSET)
        campaigns: Union[Unset, PostTagResponseDataRelationshipsCampaigns]
        if isinstance(_campaigns, Unset):
            campaigns = UNSET
        else:
            campaigns = PostTagResponseDataRelationshipsCampaigns.from_dict(_campaigns)

        _flows = d.pop("flows", UNSET)
        flows: Union[Unset, PostTagResponseDataRelationshipsFlows]
        if isinstance(_flows, Unset):
            flows = UNSET
        else:
            flows = PostTagResponseDataRelationshipsFlows.from_dict(_flows)

        post_tag_response_data_relationships = cls(
            tag_group=tag_group,
            lists=lists,
            segments=segments,
            campaigns=campaigns,
            flows=flows,
        )

        post_tag_response_data_relationships.additional_properties = d
        return post_tag_response_data_relationships

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
