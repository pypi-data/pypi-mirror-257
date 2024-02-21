from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.push_token_unregister_enum import PushTokenUnregisterEnum

if TYPE_CHECKING:
    from ..models.push_token_unregister_query_resource_object_attributes import (
        PushTokenUnregisterQueryResourceObjectAttributes,
    )


T = TypeVar("T", bound="PushTokenUnregisterQueryResourceObject")


@_attrs_define
class PushTokenUnregisterQueryResourceObject:
    """
    Attributes:
        type (PushTokenUnregisterEnum):
        attributes (PushTokenUnregisterQueryResourceObjectAttributes):
    """

    type: PushTokenUnregisterEnum
    attributes: "PushTokenUnregisterQueryResourceObjectAttributes"
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
        from ..models.push_token_unregister_query_resource_object_attributes import (
            PushTokenUnregisterQueryResourceObjectAttributes,
        )

        d = src_dict.copy()
        type = PushTokenUnregisterEnum(d.pop("type"))

        attributes = PushTokenUnregisterQueryResourceObjectAttributes.from_dict(d.pop("attributes"))

        push_token_unregister_query_resource_object = cls(
            type=type,
            attributes=attributes,
        )

        push_token_unregister_query_resource_object.additional_properties = d
        return push_token_unregister_query_resource_object

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
