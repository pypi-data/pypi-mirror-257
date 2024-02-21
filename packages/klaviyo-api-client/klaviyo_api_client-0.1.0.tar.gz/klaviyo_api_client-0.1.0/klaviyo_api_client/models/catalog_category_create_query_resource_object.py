from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.catalog_category_enum import CatalogCategoryEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.catalog_category_create_query_resource_object_attributes import (
        CatalogCategoryCreateQueryResourceObjectAttributes,
    )
    from ..models.catalog_category_create_query_resource_object_relationships import (
        CatalogCategoryCreateQueryResourceObjectRelationships,
    )


T = TypeVar("T", bound="CatalogCategoryCreateQueryResourceObject")


@_attrs_define
class CatalogCategoryCreateQueryResourceObject:
    """
    Attributes:
        type (CatalogCategoryEnum):
        attributes (CatalogCategoryCreateQueryResourceObjectAttributes):
        relationships (Union[Unset, CatalogCategoryCreateQueryResourceObjectRelationships]):
    """

    type: CatalogCategoryEnum
    attributes: "CatalogCategoryCreateQueryResourceObjectAttributes"
    relationships: Union[Unset, "CatalogCategoryCreateQueryResourceObjectRelationships"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        attributes = self.attributes.to_dict()

        relationships: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.relationships, Unset):
            relationships = self.relationships.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "attributes": attributes,
            }
        )
        if relationships is not UNSET:
            field_dict["relationships"] = relationships

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.catalog_category_create_query_resource_object_attributes import (
            CatalogCategoryCreateQueryResourceObjectAttributes,
        )
        from ..models.catalog_category_create_query_resource_object_relationships import (
            CatalogCategoryCreateQueryResourceObjectRelationships,
        )

        d = src_dict.copy()
        type = CatalogCategoryEnum(d.pop("type"))

        attributes = CatalogCategoryCreateQueryResourceObjectAttributes.from_dict(d.pop("attributes"))

        _relationships = d.pop("relationships", UNSET)
        relationships: Union[Unset, CatalogCategoryCreateQueryResourceObjectRelationships]
        if isinstance(_relationships, Unset):
            relationships = UNSET
        else:
            relationships = CatalogCategoryCreateQueryResourceObjectRelationships.from_dict(_relationships)

        catalog_category_create_query_resource_object = cls(
            type=type,
            attributes=attributes,
            relationships=relationships,
        )

        catalog_category_create_query_resource_object.additional_properties = d
        return catalog_category_create_query_resource_object

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
