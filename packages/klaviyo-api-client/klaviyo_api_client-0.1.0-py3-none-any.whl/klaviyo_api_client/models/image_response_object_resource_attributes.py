import datetime
from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="ImageResponseObjectResourceAttributes")


@_attrs_define
class ImageResponseObjectResourceAttributes:
    """
    Attributes:
        name (str):
        image_url (str):
        format_ (str):
        size (int):
        hidden (bool):
        updated_at (datetime.datetime):  Example: 2022-11-08T00:00:00.
    """

    name: str
    image_url: str
    format_: str
    size: int
    hidden: bool
    updated_at: datetime.datetime
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        image_url = self.image_url

        format_ = self.format_

        size = self.size

        hidden = self.hidden

        updated_at = self.updated_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "image_url": image_url,
                "format": format_,
                "size": size,
                "hidden": hidden,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        image_url = d.pop("image_url")

        format_ = d.pop("format")

        size = d.pop("size")

        hidden = d.pop("hidden")

        updated_at = isoparse(d.pop("updated_at"))

        image_response_object_resource_attributes = cls(
            name=name,
            image_url=image_url,
            format_=format_,
            size=size,
            hidden=hidden,
            updated_at=updated_at,
        )

        image_response_object_resource_attributes.additional_properties = d
        return image_response_object_resource_attributes

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
