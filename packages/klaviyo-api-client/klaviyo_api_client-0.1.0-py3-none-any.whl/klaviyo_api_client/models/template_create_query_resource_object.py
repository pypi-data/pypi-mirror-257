from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.template_enum import TemplateEnum

if TYPE_CHECKING:
    from ..models.template_create_query_resource_object_attributes import TemplateCreateQueryResourceObjectAttributes


T = TypeVar("T", bound="TemplateCreateQueryResourceObject")


@_attrs_define
class TemplateCreateQueryResourceObject:
    """
    Attributes:
        type (TemplateEnum):
        attributes (TemplateCreateQueryResourceObjectAttributes):
    """

    type: TemplateEnum
    attributes: "TemplateCreateQueryResourceObjectAttributes"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        attributes = self.attributes.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "attributes": attributes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.template_create_query_resource_object_attributes import (
            TemplateCreateQueryResourceObjectAttributes,
        )

        d = src_dict.copy()
        type = TemplateEnum(d.pop("type"))

        attributes = TemplateCreateQueryResourceObjectAttributes.from_dict(d.pop("attributes"))

        template_create_query_resource_object = cls(
            type=type,
            attributes=attributes,
        )

        template_create_query_resource_object.additional_properties = d
        return template_create_query_resource_object

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
