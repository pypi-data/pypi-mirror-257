from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.post_flow_values_response_dto_data_relationships_flow_messages import (
        PostFlowValuesResponseDTODataRelationshipsFlowMessages,
    )
    from ..models.post_flow_values_response_dto_data_relationships_flows import (
        PostFlowValuesResponseDTODataRelationshipsFlows,
    )


T = TypeVar("T", bound="PostFlowValuesResponseDTODataRelationships")


@_attrs_define
class PostFlowValuesResponseDTODataRelationships:
    """
    Attributes:
        flows (Union[Unset, PostFlowValuesResponseDTODataRelationshipsFlows]):
        flow_messages (Union[Unset, PostFlowValuesResponseDTODataRelationshipsFlowMessages]):
    """

    flows: Union[Unset, "PostFlowValuesResponseDTODataRelationshipsFlows"] = UNSET
    flow_messages: Union[Unset, "PostFlowValuesResponseDTODataRelationshipsFlowMessages"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        flows: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.flows, Unset):
            flows = self.flows.to_dict()

        flow_messages: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.flow_messages, Unset):
            flow_messages = self.flow_messages.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if flows is not UNSET:
            field_dict["flows"] = flows
        if flow_messages is not UNSET:
            field_dict["flow-messages"] = flow_messages

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.post_flow_values_response_dto_data_relationships_flow_messages import (
            PostFlowValuesResponseDTODataRelationshipsFlowMessages,
        )
        from ..models.post_flow_values_response_dto_data_relationships_flows import (
            PostFlowValuesResponseDTODataRelationshipsFlows,
        )

        d = src_dict.copy()
        _flows = d.pop("flows", UNSET)
        flows: Union[Unset, PostFlowValuesResponseDTODataRelationshipsFlows]
        if isinstance(_flows, Unset):
            flows = UNSET
        else:
            flows = PostFlowValuesResponseDTODataRelationshipsFlows.from_dict(_flows)

        _flow_messages = d.pop("flow-messages", UNSET)
        flow_messages: Union[Unset, PostFlowValuesResponseDTODataRelationshipsFlowMessages]
        if isinstance(_flow_messages, Unset):
            flow_messages = UNSET
        else:
            flow_messages = PostFlowValuesResponseDTODataRelationshipsFlowMessages.from_dict(_flow_messages)

        post_flow_values_response_dto_data_relationships = cls(
            flows=flows,
            flow_messages=flow_messages,
        )

        post_flow_values_response_dto_data_relationships.additional_properties = d
        return post_flow_values_response_dto_data_relationships

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
