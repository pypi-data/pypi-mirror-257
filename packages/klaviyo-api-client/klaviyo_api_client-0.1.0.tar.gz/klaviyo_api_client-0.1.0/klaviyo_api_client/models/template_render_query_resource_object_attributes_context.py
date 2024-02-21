from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="TemplateRenderQueryResourceObjectAttributesContext")


@_attrs_define
class TemplateRenderQueryResourceObjectAttributesContext:
    """The context for the template render. This must be a JSON object which has values for any tags used in the template.
    See [this doc](https://help.klaviyo.com/hc/en-us/articles/4408802648731) for more details.

        Example:
            {'first_name': 'Jane', 'last_name': 'Smith'}

    """

    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        template_render_query_resource_object_attributes_context = cls()

        template_render_query_resource_object_attributes_context.additional_properties = d
        return template_render_query_resource_object_attributes_context

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
