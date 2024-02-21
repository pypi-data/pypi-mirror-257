import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchTemplateResponseDataAttributes")


@_attrs_define
class PatchTemplateResponseDataAttributes:
    """
    Attributes:
        name (str): The name of the template
        editor_type (str): `editor_type` has a fixed set of values:
            * SYSTEM_DRAGGABLE: indicates a drag-and-drop editor template
            * SIMPLE: A rich text editor template
            * CODE: A custom HTML template
            * USER_DRAGGABLE: A hybrid template, using custom HTML in the drag-and-drop editor
        html (str): The rendered HTML of the template
        text (Union[Unset, str]): The template plain_text
        created (Union[Unset, datetime.datetime]): The date the template was created in ISO 8601 format (YYYY-MM-
            DDTHH:MM:SS.mmmmmm) Example: 2022-11-08T00:00:00.
        updated (Union[Unset, datetime.datetime]): The date the template was updated in ISO 8601 format (YYYY-MM-
            DDTHH:MM:SS.mmmmmm) Example: 2022-11-08T00:00:00.
    """

    name: str
    editor_type: str
    html: str
    text: Union[Unset, str] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    updated: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        editor_type = self.editor_type

        html = self.html

        text = self.text

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        updated: Union[Unset, str] = UNSET
        if not isinstance(self.updated, Unset):
            updated = self.updated.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "editor_type": editor_type,
                "html": html,
            }
        )
        if text is not UNSET:
            field_dict["text"] = text
        if created is not UNSET:
            field_dict["created"] = created
        if updated is not UNSET:
            field_dict["updated"] = updated

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        editor_type = d.pop("editor_type")

        html = d.pop("html")

        text = d.pop("text", UNSET)

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset):
            created = UNSET
        else:
            created = isoparse(_created)

        _updated = d.pop("updated", UNSET)
        updated: Union[Unset, datetime.datetime]
        if isinstance(_updated, Unset):
            updated = UNSET
        else:
            updated = isoparse(_updated)

        patch_template_response_data_attributes = cls(
            name=name,
            editor_type=editor_type,
            html=html,
            text=text,
            created=created,
            updated=updated,
        )

        patch_template_response_data_attributes.additional_properties = d
        return patch_template_response_data_attributes

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
