from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ImageCreateQueryResourceObjectAttributes")


@_attrs_define
class ImageCreateQueryResourceObjectAttributes:
    """
    Attributes:
        import_from_url (str): An existing image url to import the image from. Alternatively, you may specify a base-64
            encoded data-uri (`data:image/...`). Supported image formats: jpeg,png,gif. Maximum image size: 5MB. Example:
            https://www.example.com/example.jpg.
        name (Union[Unset, str]): A name for the image.  Defaults to the filename if not provided.  If the name matches
            an existing image, a suffix will be added.
        hidden (Union[Unset, bool]): If true, this image is not shown in the asset library. Default: False.
    """

    import_from_url: str
    name: Union[Unset, str] = UNSET
    hidden: Union[Unset, bool] = False
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        import_from_url = self.import_from_url

        name = self.name

        hidden = self.hidden

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "import_from_url": import_from_url,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if hidden is not UNSET:
            field_dict["hidden"] = hidden

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        import_from_url = d.pop("import_from_url")

        name = d.pop("name", UNSET)

        hidden = d.pop("hidden", UNSET)

        image_create_query_resource_object_attributes = cls(
            import_from_url=import_from_url,
            name=name,
            hidden=hidden,
        )

        image_create_query_resource_object_attributes.additional_properties = d
        return image_create_query_resource_object_attributes

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
