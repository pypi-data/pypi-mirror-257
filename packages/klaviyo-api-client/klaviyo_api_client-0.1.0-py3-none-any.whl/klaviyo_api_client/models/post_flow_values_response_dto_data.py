from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.flow_values_report_enum import FlowValuesReportEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.object_links import ObjectLinks
    from ..models.post_flow_values_response_dto_data_attributes import PostFlowValuesResponseDTODataAttributes
    from ..models.post_flow_values_response_dto_data_relationships import PostFlowValuesResponseDTODataRelationships


T = TypeVar("T", bound="PostFlowValuesResponseDTOData")


@_attrs_define
class PostFlowValuesResponseDTOData:
    """
    Attributes:
        type (FlowValuesReportEnum):
        attributes (PostFlowValuesResponseDTODataAttributes):
        links (ObjectLinks):
        relationships (Union[Unset, PostFlowValuesResponseDTODataRelationships]):
    """

    type: FlowValuesReportEnum
    attributes: "PostFlowValuesResponseDTODataAttributes"
    links: "ObjectLinks"
    relationships: Union[Unset, "PostFlowValuesResponseDTODataRelationships"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

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
                "attributes": attributes,
                "links": links,
            }
        )
        if relationships is not UNSET:
            field_dict["relationships"] = relationships

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.object_links import ObjectLinks
        from ..models.post_flow_values_response_dto_data_attributes import PostFlowValuesResponseDTODataAttributes
        from ..models.post_flow_values_response_dto_data_relationships import PostFlowValuesResponseDTODataRelationships

        d = src_dict.copy()
        type = FlowValuesReportEnum(d.pop("type"))

        attributes = PostFlowValuesResponseDTODataAttributes.from_dict(d.pop("attributes"))

        links = ObjectLinks.from_dict(d.pop("links"))

        _relationships = d.pop("relationships", UNSET)
        relationships: Union[Unset, PostFlowValuesResponseDTODataRelationships]
        if isinstance(_relationships, Unset):
            relationships = UNSET
        else:
            relationships = PostFlowValuesResponseDTODataRelationships.from_dict(_relationships)

        post_flow_values_response_dto_data = cls(
            type=type,
            attributes=attributes,
            links=links,
            relationships=relationships,
        )

        post_flow_values_response_dto_data.additional_properties = d
        return post_flow_values_response_dto_data

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
