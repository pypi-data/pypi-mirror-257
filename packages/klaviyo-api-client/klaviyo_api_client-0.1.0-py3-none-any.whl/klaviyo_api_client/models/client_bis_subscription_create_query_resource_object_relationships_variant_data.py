from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.catalog_variant_enum import CatalogVariantEnum

T = TypeVar("T", bound="ClientBISSubscriptionCreateQueryResourceObjectRelationshipsVariantData")


@_attrs_define
class ClientBISSubscriptionCreateQueryResourceObjectRelationshipsVariantData:
    """
    Attributes:
        type (CatalogVariantEnum):
        id (str): The catalog variant ID for which the profile is subscribing to back in stock notifications. This ID is
            made up of the integration type, catalog ID, and and the external ID of the variant like so:
            `integrationType:::catalogId:::externalId`. If the integration you are using is not set up for multi-catalog
            storage, the 'catalogId' will be `$default`. For Shopify `$shopify:::$default:::33001893429341` Example:
            $custom:::$default:::SAMPLE-DATA-ITEM-1-VARIANT-MEDIUM.
    """

    type: CatalogVariantEnum
    id: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "id": id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = CatalogVariantEnum(d.pop("type"))

        id = d.pop("id")

        client_bis_subscription_create_query_resource_object_relationships_variant_data = cls(
            type=type,
            id=id,
        )

        client_bis_subscription_create_query_resource_object_relationships_variant_data.additional_properties = d
        return client_bis_subscription_create_query_resource_object_relationships_variant_data

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
