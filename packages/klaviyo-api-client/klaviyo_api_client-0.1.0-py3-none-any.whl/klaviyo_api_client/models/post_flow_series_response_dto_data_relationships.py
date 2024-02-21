from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.post_flow_series_response_dto_data_relationships_flow_messages import (
        PostFlowSeriesResponseDTODataRelationshipsFlowMessages,
    )
    from ..models.post_flow_series_response_dto_data_relationships_flows import (
        PostFlowSeriesResponseDTODataRelationshipsFlows,
    )


T = TypeVar("T", bound="PostFlowSeriesResponseDTODataRelationships")


@_attrs_define
class PostFlowSeriesResponseDTODataRelationships:
    """
    Attributes:
        flows (Union[Unset, PostFlowSeriesResponseDTODataRelationshipsFlows]):
        flow_messages (Union[Unset, PostFlowSeriesResponseDTODataRelationshipsFlowMessages]):
    """

    flows: Union[Unset, "PostFlowSeriesResponseDTODataRelationshipsFlows"] = UNSET
    flow_messages: Union[Unset, "PostFlowSeriesResponseDTODataRelationshipsFlowMessages"] = UNSET
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
        from ..models.post_flow_series_response_dto_data_relationships_flow_messages import (
            PostFlowSeriesResponseDTODataRelationshipsFlowMessages,
        )
        from ..models.post_flow_series_response_dto_data_relationships_flows import (
            PostFlowSeriesResponseDTODataRelationshipsFlows,
        )

        d = src_dict.copy()
        _flows = d.pop("flows", UNSET)
        flows: Union[Unset, PostFlowSeriesResponseDTODataRelationshipsFlows]
        if isinstance(_flows, Unset):
            flows = UNSET
        else:
            flows = PostFlowSeriesResponseDTODataRelationshipsFlows.from_dict(_flows)

        _flow_messages = d.pop("flow-messages", UNSET)
        flow_messages: Union[Unset, PostFlowSeriesResponseDTODataRelationshipsFlowMessages]
        if isinstance(_flow_messages, Unset):
            flow_messages = UNSET
        else:
            flow_messages = PostFlowSeriesResponseDTODataRelationshipsFlowMessages.from_dict(_flow_messages)

        post_flow_series_response_dto_data_relationships = cls(
            flows=flows,
            flow_messages=flow_messages,
        )

        post_flow_series_response_dto_data_relationships.additional_properties = d
        return post_flow_series_response_dto_data_relationships

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
