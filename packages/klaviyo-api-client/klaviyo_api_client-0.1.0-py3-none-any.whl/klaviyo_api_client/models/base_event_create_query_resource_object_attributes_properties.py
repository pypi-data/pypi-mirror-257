from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="BaseEventCreateQueryResourceObjectAttributesProperties")


@_attrs_define
class BaseEventCreateQueryResourceObjectAttributesProperties:
    """Properties of this event. Any top level property (that are not objects) can be
    used to create segments. The $extra property is a special property. This records any
    non-segmentable values that can be referenced later. For example, HTML templates are
    useful on a segment but are not used to create a segment. There are limits
    placed onto the size of the data present. This must not exceed 5 MB. This must not
    exceed 300 event properties. A single string cannot be larger than 100 KB. Each array
    must not exceed 4000 elements. The properties cannot contain more than 10 nested levels.

        Example:
            {'Brand': 'Kids Book', 'Categories': ['Fiction', 'Children'], 'ProductID': 1111, 'ProductName': 'Winnie the
                Pooh', '$extra': {'URL': 'http://www.example.com/path/to/product', 'ImageURL':
                'http://www.example.com/path/to/product/image.png'}}

    """

    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        base_event_create_query_resource_object_attributes_properties = cls()

        base_event_create_query_resource_object_attributes_properties.additional_properties = d
        return base_event_create_query_resource_object_attributes_properties

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
