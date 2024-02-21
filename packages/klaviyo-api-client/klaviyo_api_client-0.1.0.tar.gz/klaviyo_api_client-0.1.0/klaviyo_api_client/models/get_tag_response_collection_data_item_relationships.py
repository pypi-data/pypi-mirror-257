from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_tag_response_collection_data_item_relationships_campaigns import (
        GetTagResponseCollectionDataItemRelationshipsCampaigns,
    )
    from ..models.get_tag_response_collection_data_item_relationships_flows import (
        GetTagResponseCollectionDataItemRelationshipsFlows,
    )
    from ..models.get_tag_response_collection_data_item_relationships_lists import (
        GetTagResponseCollectionDataItemRelationshipsLists,
    )
    from ..models.get_tag_response_collection_data_item_relationships_segments import (
        GetTagResponseCollectionDataItemRelationshipsSegments,
    )
    from ..models.get_tag_response_collection_data_item_relationships_tag_group import (
        GetTagResponseCollectionDataItemRelationshipsTagGroup,
    )


T = TypeVar("T", bound="GetTagResponseCollectionDataItemRelationships")


@_attrs_define
class GetTagResponseCollectionDataItemRelationships:
    """
    Attributes:
        tag_group (Union[Unset, GetTagResponseCollectionDataItemRelationshipsTagGroup]):
        lists (Union[Unset, GetTagResponseCollectionDataItemRelationshipsLists]):
        segments (Union[Unset, GetTagResponseCollectionDataItemRelationshipsSegments]):
        campaigns (Union[Unset, GetTagResponseCollectionDataItemRelationshipsCampaigns]):
        flows (Union[Unset, GetTagResponseCollectionDataItemRelationshipsFlows]):
    """

    tag_group: Union[Unset, "GetTagResponseCollectionDataItemRelationshipsTagGroup"] = UNSET
    lists: Union[Unset, "GetTagResponseCollectionDataItemRelationshipsLists"] = UNSET
    segments: Union[Unset, "GetTagResponseCollectionDataItemRelationshipsSegments"] = UNSET
    campaigns: Union[Unset, "GetTagResponseCollectionDataItemRelationshipsCampaigns"] = UNSET
    flows: Union[Unset, "GetTagResponseCollectionDataItemRelationshipsFlows"] = UNSET
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
        from ..models.get_tag_response_collection_data_item_relationships_campaigns import (
            GetTagResponseCollectionDataItemRelationshipsCampaigns,
        )
        from ..models.get_tag_response_collection_data_item_relationships_flows import (
            GetTagResponseCollectionDataItemRelationshipsFlows,
        )
        from ..models.get_tag_response_collection_data_item_relationships_lists import (
            GetTagResponseCollectionDataItemRelationshipsLists,
        )
        from ..models.get_tag_response_collection_data_item_relationships_segments import (
            GetTagResponseCollectionDataItemRelationshipsSegments,
        )
        from ..models.get_tag_response_collection_data_item_relationships_tag_group import (
            GetTagResponseCollectionDataItemRelationshipsTagGroup,
        )

        d = src_dict.copy()
        _tag_group = d.pop("tag-group", UNSET)
        tag_group: Union[Unset, GetTagResponseCollectionDataItemRelationshipsTagGroup]
        if isinstance(_tag_group, Unset):
            tag_group = UNSET
        else:
            tag_group = GetTagResponseCollectionDataItemRelationshipsTagGroup.from_dict(_tag_group)

        _lists = d.pop("lists", UNSET)
        lists: Union[Unset, GetTagResponseCollectionDataItemRelationshipsLists]
        if isinstance(_lists, Unset):
            lists = UNSET
        else:
            lists = GetTagResponseCollectionDataItemRelationshipsLists.from_dict(_lists)

        _segments = d.pop("segments", UNSET)
        segments: Union[Unset, GetTagResponseCollectionDataItemRelationshipsSegments]
        if isinstance(_segments, Unset):
            segments = UNSET
        else:
            segments = GetTagResponseCollectionDataItemRelationshipsSegments.from_dict(_segments)

        _campaigns = d.pop("campaigns", UNSET)
        campaigns: Union[Unset, GetTagResponseCollectionDataItemRelationshipsCampaigns]
        if isinstance(_campaigns, Unset):
            campaigns = UNSET
        else:
            campaigns = GetTagResponseCollectionDataItemRelationshipsCampaigns.from_dict(_campaigns)

        _flows = d.pop("flows", UNSET)
        flows: Union[Unset, GetTagResponseCollectionDataItemRelationshipsFlows]
        if isinstance(_flows, Unset):
            flows = UNSET
        else:
            flows = GetTagResponseCollectionDataItemRelationshipsFlows.from_dict(_flows)

        get_tag_response_collection_data_item_relationships = cls(
            tag_group=tag_group,
            lists=lists,
            segments=segments,
            campaigns=campaigns,
            flows=flows,
        )

        get_tag_response_collection_data_item_relationships.additional_properties = d
        return get_tag_response_collection_data_item_relationships

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
