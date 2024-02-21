from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_flow_action_response_collection_data_item_relationships_flow import (
        GetFlowActionResponseCollectionDataItemRelationshipsFlow,
    )
    from ..models.get_flow_action_response_collection_data_item_relationships_flow_messages import (
        GetFlowActionResponseCollectionDataItemRelationshipsFlowMessages,
    )


T = TypeVar("T", bound="GetFlowActionResponseCollectionDataItemRelationships")


@_attrs_define
class GetFlowActionResponseCollectionDataItemRelationships:
    """
    Attributes:
        flow (Union[Unset, GetFlowActionResponseCollectionDataItemRelationshipsFlow]):
        flow_messages (Union[Unset, GetFlowActionResponseCollectionDataItemRelationshipsFlowMessages]):
    """

    flow: Union[Unset, "GetFlowActionResponseCollectionDataItemRelationshipsFlow"] = UNSET
    flow_messages: Union[Unset, "GetFlowActionResponseCollectionDataItemRelationshipsFlowMessages"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        flow: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.flow, Unset):
            flow = self.flow.to_dict()

        flow_messages: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.flow_messages, Unset):
            flow_messages = self.flow_messages.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if flow is not UNSET:
            field_dict["flow"] = flow
        if flow_messages is not UNSET:
            field_dict["flow-messages"] = flow_messages

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_flow_action_response_collection_data_item_relationships_flow import (
            GetFlowActionResponseCollectionDataItemRelationshipsFlow,
        )
        from ..models.get_flow_action_response_collection_data_item_relationships_flow_messages import (
            GetFlowActionResponseCollectionDataItemRelationshipsFlowMessages,
        )

        d = src_dict.copy()
        _flow = d.pop("flow", UNSET)
        flow: Union[Unset, GetFlowActionResponseCollectionDataItemRelationshipsFlow]
        if isinstance(_flow, Unset):
            flow = UNSET
        else:
            flow = GetFlowActionResponseCollectionDataItemRelationshipsFlow.from_dict(_flow)

        _flow_messages = d.pop("flow-messages", UNSET)
        flow_messages: Union[Unset, GetFlowActionResponseCollectionDataItemRelationshipsFlowMessages]
        if isinstance(_flow_messages, Unset):
            flow_messages = UNSET
        else:
            flow_messages = GetFlowActionResponseCollectionDataItemRelationshipsFlowMessages.from_dict(_flow_messages)

        get_flow_action_response_collection_data_item_relationships = cls(
            flow=flow,
            flow_messages=flow_messages,
        )

        get_flow_action_response_collection_data_item_relationships.additional_properties = d
        return get_flow_action_response_collection_data_item_relationships

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
