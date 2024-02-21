from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TemplateCreateQueryResourceObjectAttributes")


@_attrs_define
class TemplateCreateQueryResourceObjectAttributes:
    """
    Attributes:
        name (str): The name of the template Example: Monthly Newsletter Template.
        editor_type (str): Restricted to CODE
        html (Union[Unset, str]): The HTML contents of the template Example:
                        <html>
                            <body>
                                hello world
                            </body>
                        </html>
                    .
        text (Union[Unset, str]): The plaintext version of the template Example: hello world.
    """

    name: str
    editor_type: str
    html: Union[Unset, str] = UNSET
    text: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        editor_type = self.editor_type

        html = self.html

        text = self.text

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "editor_type": editor_type,
            }
        )
        if html is not UNSET:
            field_dict["html"] = html
        if text is not UNSET:
            field_dict["text"] = text

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        editor_type = d.pop("editor_type")

        html = d.pop("html", UNSET)

        text = d.pop("text", UNSET)

        template_create_query_resource_object_attributes = cls(
            name=name,
            editor_type=editor_type,
            html=html,
            text=text,
        )

        template_create_query_resource_object_attributes.additional_properties = d
        return template_create_query_resource_object_attributes

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
