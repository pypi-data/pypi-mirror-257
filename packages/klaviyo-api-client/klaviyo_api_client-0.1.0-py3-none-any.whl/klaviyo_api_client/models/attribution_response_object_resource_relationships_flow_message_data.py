from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.flow_message_enum import FlowMessageEnum

T = TypeVar("T", bound="AttributionResponseObjectResourceRelationshipsFlowMessageData")


@_attrs_define
class AttributionResponseObjectResourceRelationshipsFlowMessageData:
    """
    Attributes:
        type (FlowMessageEnum):
        id (str): Attributed Flow Message
    """

    type: FlowMessageEnum
    id: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "id": id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = FlowMessageEnum(d.pop("type"))

        id = d.pop("id")

        attribution_response_object_resource_relationships_flow_message_data = cls(
            type=type,
            id=id,
        )

        attribution_response_object_resource_relationships_flow_message_data.additional_properties = d
        return attribution_response_object_resource_relationships_flow_message_data

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
