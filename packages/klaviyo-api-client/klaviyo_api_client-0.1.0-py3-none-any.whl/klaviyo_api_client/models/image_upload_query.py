from io import BytesIO
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, File, Unset

T = TypeVar("T", bound="ImageUploadQuery")


@_attrs_define
class ImageUploadQuery:
    """
    Attributes:
        file (File): The image file to upload. Supported image formats: jpeg,png,gif. Maximum image size: 5MB.
        name (Union[Unset, str]): A name for the image.  Defaults to the filename if not provided.  If the name matches
            an existing image, a suffix will be added.
        hidden (Union[Unset, bool]): If true, this image is not shown in the asset library. Default: False.
    """

    file: File
    name: Union[Unset, str] = UNSET
    hidden: Union[Unset, bool] = False
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        file = self.file.to_tuple()

        name = self.name

        hidden = self.hidden

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "file": file,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if hidden is not UNSET:
            field_dict["hidden"] = hidden

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        file = self.file.to_tuple()

        name = self.name if isinstance(self.name, Unset) else (None, str(self.name).encode(), "text/plain")

        hidden = self.hidden if isinstance(self.hidden, Unset) else (None, str(self.hidden).encode(), "text/plain")

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {key: (None, str(value).encode(), "text/plain") for key, value in self.additional_properties.items()}
        )
        field_dict.update(
            {
                "file": file,
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
        file = File(payload=BytesIO(d.pop("file")))

        name = d.pop("name", UNSET)

        hidden = d.pop("hidden", UNSET)

        image_upload_query = cls(
            file=file,
            name=name,
            hidden=hidden,
        )

        image_upload_query.additional_properties = d
        return image_upload_query

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
