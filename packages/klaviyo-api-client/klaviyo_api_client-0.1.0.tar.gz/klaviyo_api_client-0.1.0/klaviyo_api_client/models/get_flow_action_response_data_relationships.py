from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_flow_action_response_data_relationships_flow import GetFlowActionResponseDataRelationshipsFlow
    from ..models.get_flow_action_response_data_relationships_flow_messages import (
        GetFlowActionResponseDataRelationshipsFlowMessages,
    )


T = TypeVar("T", bound="GetFlowActionResponseDataRelationships")


@_attrs_define
class GetFlowActionResponseDataRelationships:
    """
    Attributes:
        flow (Union[Unset, GetFlowActionResponseDataRelationshipsFlow]):
        flow_messages (Union[Unset, GetFlowActionResponseDataRelationshipsFlowMessages]):
    """

    flow: Union[Unset, "GetFlowActionResponseDataRelationshipsFlow"] = UNSET
    flow_messages: Union[Unset, "GetFlowActionResponseDataRelationshipsFlowMessages"] = UNSET
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
        from ..models.get_flow_action_response_data_relationships_flow import GetFlowActionResponseDataRelationshipsFlow
        from ..models.get_flow_action_response_data_relationships_flow_messages import (
            GetFlowActionResponseDataRelationshipsFlowMessages,
        )

        d = src_dict.copy()
        _flow = d.pop("flow", UNSET)
        flow: Union[Unset, GetFlowActionResponseDataRelationshipsFlow]
        if isinstance(_flow, Unset):
            flow = UNSET
        else:
            flow = GetFlowActionResponseDataRelationshipsFlow.from_dict(_flow)

        _flow_messages = d.pop("flow-messages", UNSET)
        flow_messages: Union[Unset, GetFlowActionResponseDataRelationshipsFlowMessages]
        if isinstance(_flow_messages, Unset):
            flow_messages = UNSET
        else:
            flow_messages = GetFlowActionResponseDataRelationshipsFlowMessages.from_dict(_flow_messages)

        get_flow_action_response_data_relationships = cls(
            flow=flow,
            flow_messages=flow_messages,
        )

        get_flow_action_response_data_relationships.additional_properties = d
        return get_flow_action_response_data_relationships

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
