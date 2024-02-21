from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_tag_response_compound_document_data_relationships_campaigns import (
        GetTagResponseCompoundDocumentDataRelationshipsCampaigns,
    )
    from ..models.get_tag_response_compound_document_data_relationships_flows import (
        GetTagResponseCompoundDocumentDataRelationshipsFlows,
    )
    from ..models.get_tag_response_compound_document_data_relationships_lists import (
        GetTagResponseCompoundDocumentDataRelationshipsLists,
    )
    from ..models.get_tag_response_compound_document_data_relationships_segments import (
        GetTagResponseCompoundDocumentDataRelationshipsSegments,
    )
    from ..models.get_tag_response_compound_document_data_relationships_tag_group import (
        GetTagResponseCompoundDocumentDataRelationshipsTagGroup,
    )


T = TypeVar("T", bound="GetTagResponseCompoundDocumentDataRelationships")


@_attrs_define
class GetTagResponseCompoundDocumentDataRelationships:
    """
    Attributes:
        tag_group (Union[Unset, GetTagResponseCompoundDocumentDataRelationshipsTagGroup]):
        lists (Union[Unset, GetTagResponseCompoundDocumentDataRelationshipsLists]):
        segments (Union[Unset, GetTagResponseCompoundDocumentDataRelationshipsSegments]):
        campaigns (Union[Unset, GetTagResponseCompoundDocumentDataRelationshipsCampaigns]):
        flows (Union[Unset, GetTagResponseCompoundDocumentDataRelationshipsFlows]):
    """

    tag_group: Union[Unset, "GetTagResponseCompoundDocumentDataRelationshipsTagGroup"] = UNSET
    lists: Union[Unset, "GetTagResponseCompoundDocumentDataRelationshipsLists"] = UNSET
    segments: Union[Unset, "GetTagResponseCompoundDocumentDataRelationshipsSegments"] = UNSET
    campaigns: Union[Unset, "GetTagResponseCompoundDocumentDataRelationshipsCampaigns"] = UNSET
    flows: Union[Unset, "GetTagResponseCompoundDocumentDataRelationshipsFlows"] = UNSET
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
        from ..models.get_tag_response_compound_document_data_relationships_campaigns import (
            GetTagResponseCompoundDocumentDataRelationshipsCampaigns,
        )
        from ..models.get_tag_response_compound_document_data_relationships_flows import (
            GetTagResponseCompoundDocumentDataRelationshipsFlows,
        )
        from ..models.get_tag_response_compound_document_data_relationships_lists import (
            GetTagResponseCompoundDocumentDataRelationshipsLists,
        )
        from ..models.get_tag_response_compound_document_data_relationships_segments import (
            GetTagResponseCompoundDocumentDataRelationshipsSegments,
        )
        from ..models.get_tag_response_compound_document_data_relationships_tag_group import (
            GetTagResponseCompoundDocumentDataRelationshipsTagGroup,
        )

        d = src_dict.copy()
        _tag_group = d.pop("tag-group", UNSET)
        tag_group: Union[Unset, GetTagResponseCompoundDocumentDataRelationshipsTagGroup]
        if isinstance(_tag_group, Unset):
            tag_group = UNSET
        else:
            tag_group = GetTagResponseCompoundDocumentDataRelationshipsTagGroup.from_dict(_tag_group)

        _lists = d.pop("lists", UNSET)
        lists: Union[Unset, GetTagResponseCompoundDocumentDataRelationshipsLists]
        if isinstance(_lists, Unset):
            lists = UNSET
        else:
            lists = GetTagResponseCompoundDocumentDataRelationshipsLists.from_dict(_lists)

        _segments = d.pop("segments", UNSET)
        segments: Union[Unset, GetTagResponseCompoundDocumentDataRelationshipsSegments]
        if isinstance(_segments, Unset):
            segments = UNSET
        else:
            segments = GetTagResponseCompoundDocumentDataRelationshipsSegments.from_dict(_segments)

        _campaigns = d.pop("campaigns", UNSET)
        campaigns: Union[Unset, GetTagResponseCompoundDocumentDataRelationshipsCampaigns]
        if isinstance(_campaigns, Unset):
            campaigns = UNSET
        else:
            campaigns = GetTagResponseCompoundDocumentDataRelationshipsCampaigns.from_dict(_campaigns)

        _flows = d.pop("flows", UNSET)
        flows: Union[Unset, GetTagResponseCompoundDocumentDataRelationshipsFlows]
        if isinstance(_flows, Unset):
            flows = UNSET
        else:
            flows = GetTagResponseCompoundDocumentDataRelationshipsFlows.from_dict(_flows)

        get_tag_response_compound_document_data_relationships = cls(
            tag_group=tag_group,
            lists=lists,
            segments=segments,
            campaigns=campaigns,
            flows=flows,
        )

        get_tag_response_compound_document_data_relationships.additional_properties = d
        return get_tag_response_compound_document_data_relationships

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
