from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.patch_flow_response_data_relationships_flow_actions import (
        PatchFlowResponseDataRelationshipsFlowActions,
    )
    from ..models.patch_flow_response_data_relationships_tags import PatchFlowResponseDataRelationshipsTags


T = TypeVar("T", bound="PatchFlowResponseDataRelationships")


@_attrs_define
class PatchFlowResponseDataRelationships:
    """
    Attributes:
        flow_actions (Union[Unset, PatchFlowResponseDataRelationshipsFlowActions]):
        tags (Union[Unset, PatchFlowResponseDataRelationshipsTags]):
    """

    flow_actions: Union[Unset, "PatchFlowResponseDataRelationshipsFlowActions"] = UNSET
    tags: Union[Unset, "PatchFlowResponseDataRelationshipsTags"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        flow_actions: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.flow_actions, Unset):
            flow_actions = self.flow_actions.to_dict()

        tags: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if flow_actions is not UNSET:
            field_dict["flow-actions"] = flow_actions
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.patch_flow_response_data_relationships_flow_actions import (
            PatchFlowResponseDataRelationshipsFlowActions,
        )
        from ..models.patch_flow_response_data_relationships_tags import PatchFlowResponseDataRelationshipsTags

        d = src_dict.copy()
        _flow_actions = d.pop("flow-actions", UNSET)
        flow_actions: Union[Unset, PatchFlowResponseDataRelationshipsFlowActions]
        if isinstance(_flow_actions, Unset):
            flow_actions = UNSET
        else:
            flow_actions = PatchFlowResponseDataRelationshipsFlowActions.from_dict(_flow_actions)

        _tags = d.pop("tags", UNSET)
        tags: Union[Unset, PatchFlowResponseDataRelationshipsTags]
        if isinstance(_tags, Unset):
            tags = UNSET
        else:
            tags = PatchFlowResponseDataRelationshipsTags.from_dict(_tags)

        patch_flow_response_data_relationships = cls(
            flow_actions=flow_actions,
            tags=tags,
        )

        patch_flow_response_data_relationships.additional_properties = d
        return patch_flow_response_data_relationships

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
