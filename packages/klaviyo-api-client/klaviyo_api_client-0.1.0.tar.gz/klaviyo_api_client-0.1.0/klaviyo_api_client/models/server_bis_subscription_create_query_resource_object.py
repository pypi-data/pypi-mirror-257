from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.back_in_stock_subscription_enum import BackInStockSubscriptionEnum

if TYPE_CHECKING:
    from ..models.server_bis_subscription_create_query_resource_object_attributes import (
        ServerBISSubscriptionCreateQueryResourceObjectAttributes,
    )
    from ..models.server_bis_subscription_create_query_resource_object_relationships import (
        ServerBISSubscriptionCreateQueryResourceObjectRelationships,
    )


T = TypeVar("T", bound="ServerBISSubscriptionCreateQueryResourceObject")


@_attrs_define
class ServerBISSubscriptionCreateQueryResourceObject:
    """
    Attributes:
        type (BackInStockSubscriptionEnum):
        attributes (ServerBISSubscriptionCreateQueryResourceObjectAttributes):
        relationships (ServerBISSubscriptionCreateQueryResourceObjectRelationships):
    """

    type: BackInStockSubscriptionEnum
    attributes: "ServerBISSubscriptionCreateQueryResourceObjectAttributes"
    relationships: "ServerBISSubscriptionCreateQueryResourceObjectRelationships"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        attributes = self.attributes.to_dict()

        relationships = self.relationships.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "attributes": attributes,
                "relationships": relationships,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.server_bis_subscription_create_query_resource_object_attributes import (
            ServerBISSubscriptionCreateQueryResourceObjectAttributes,
        )
        from ..models.server_bis_subscription_create_query_resource_object_relationships import (
            ServerBISSubscriptionCreateQueryResourceObjectRelationships,
        )

        d = src_dict.copy()
        type = BackInStockSubscriptionEnum(d.pop("type"))

        attributes = ServerBISSubscriptionCreateQueryResourceObjectAttributes.from_dict(d.pop("attributes"))

        relationships = ServerBISSubscriptionCreateQueryResourceObjectRelationships.from_dict(d.pop("relationships"))

        server_bis_subscription_create_query_resource_object = cls(
            type=type,
            attributes=attributes,
            relationships=relationships,
        )

        server_bis_subscription_create_query_resource_object.additional_properties = d
        return server_bis_subscription_create_query_resource_object

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
