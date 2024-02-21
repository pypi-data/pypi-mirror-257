from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.catalog_item_enum import CatalogItemEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.catalog_item_update_query_resource_object_attributes import (
        CatalogItemUpdateQueryResourceObjectAttributes,
    )
    from ..models.catalog_item_update_query_resource_object_relationships import (
        CatalogItemUpdateQueryResourceObjectRelationships,
    )


T = TypeVar("T", bound="CatalogItemUpdateQueryResourceObject")


@_attrs_define
class CatalogItemUpdateQueryResourceObject:
    """
    Attributes:
        type (CatalogItemEnum):
        id (str): The catalog item ID is a compound ID (string), with format:
            `{integration}:::{catalog}:::{external_id}`. Currently, the only supported integration type is `$custom`, and
            the only supported catalog is `$default`. Example: $custom:::$default:::SAMPLE-DATA-ITEM-1.
        attributes (CatalogItemUpdateQueryResourceObjectAttributes):
        relationships (Union[Unset, CatalogItemUpdateQueryResourceObjectRelationships]):
    """

    type: CatalogItemEnum
    id: str
    attributes: "CatalogItemUpdateQueryResourceObjectAttributes"
    relationships: Union[Unset, "CatalogItemUpdateQueryResourceObjectRelationships"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        id = self.id

        attributes = self.attributes.to_dict()

        relationships: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.relationships, Unset):
            relationships = self.relationships.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "id": id,
                "attributes": attributes,
            }
        )
        if relationships is not UNSET:
            field_dict["relationships"] = relationships

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.catalog_item_update_query_resource_object_attributes import (
            CatalogItemUpdateQueryResourceObjectAttributes,
        )
        from ..models.catalog_item_update_query_resource_object_relationships import (
            CatalogItemUpdateQueryResourceObjectRelationships,
        )

        d = src_dict.copy()
        type = CatalogItemEnum(d.pop("type"))

        id = d.pop("id")

        attributes = CatalogItemUpdateQueryResourceObjectAttributes.from_dict(d.pop("attributes"))

        _relationships = d.pop("relationships", UNSET)
        relationships: Union[Unset, CatalogItemUpdateQueryResourceObjectRelationships]
        if isinstance(_relationships, Unset):
            relationships = UNSET
        else:
            relationships = CatalogItemUpdateQueryResourceObjectRelationships.from_dict(_relationships)

        catalog_item_update_query_resource_object = cls(
            type=type,
            id=id,
            attributes=attributes,
            relationships=relationships,
        )

        catalog_item_update_query_resource_object.additional_properties = d
        return catalog_item_update_query_resource_object

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
