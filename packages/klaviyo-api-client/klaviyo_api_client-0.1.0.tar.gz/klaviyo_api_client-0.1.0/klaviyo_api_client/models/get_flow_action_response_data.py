from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.flow_action_enum import FlowActionEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.flow_action_response_object_resource_attributes import FlowActionResponseObjectResourceAttributes
    from ..models.get_flow_action_response_data_relationships import GetFlowActionResponseDataRelationships
    from ..models.object_links import ObjectLinks


T = TypeVar("T", bound="GetFlowActionResponseData")


@_attrs_define
class GetFlowActionResponseData:
    """
    Attributes:
        type (FlowActionEnum):
        id (str):
        attributes (FlowActionResponseObjectResourceAttributes):
        links (ObjectLinks):
        relationships (Union[Unset, GetFlowActionResponseDataRelationships]):
    """

    type: FlowActionEnum
    id: str
    attributes: "FlowActionResponseObjectResourceAttributes"
    links: "ObjectLinks"
    relationships: Union[Unset, "GetFlowActionResponseDataRelationships"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        id = self.id

        attributes = self.attributes.to_dict()

        links = self.links.to_dict()

        relationships: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.relationships, Unset):
            relationships = self.relationships.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "id": id,
                "attributes": attributes,
                "links": links,
            }
        )
        if relationships is not UNSET:
            field_dict["relationships"] = relationships

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.flow_action_response_object_resource_attributes import FlowActionResponseObjectResourceAttributes
        from ..models.get_flow_action_response_data_relationships import GetFlowActionResponseDataRelationships
        from ..models.object_links import ObjectLinks

        d = src_dict.copy()
        type = FlowActionEnum(d.pop("type"))

        id = d.pop("id")

        attributes = FlowActionResponseObjectResourceAttributes.from_dict(d.pop("attributes"))

        links = ObjectLinks.from_dict(d.pop("links"))

        _relationships = d.pop("relationships", UNSET)
        relationships: Union[Unset, GetFlowActionResponseDataRelationships]
        if isinstance(_relationships, Unset):
            relationships = UNSET
        else:
            relationships = GetFlowActionResponseDataRelationships.from_dict(_relationships)

        get_flow_action_response_data = cls(
            type=type,
            id=id,
            attributes=attributes,
            links=links,
            relationships=relationships,
        )

        get_flow_action_response_data.additional_properties = d
        return get_flow_action_response_data

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
