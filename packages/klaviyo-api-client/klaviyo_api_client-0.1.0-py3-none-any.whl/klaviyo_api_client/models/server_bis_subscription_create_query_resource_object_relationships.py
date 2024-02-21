from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.server_bis_subscription_create_query_resource_object_relationships_variant import (
        ServerBISSubscriptionCreateQueryResourceObjectRelationshipsVariant,
    )


T = TypeVar("T", bound="ServerBISSubscriptionCreateQueryResourceObjectRelationships")


@_attrs_define
class ServerBISSubscriptionCreateQueryResourceObjectRelationships:
    """
    Attributes:
        variant (ServerBISSubscriptionCreateQueryResourceObjectRelationshipsVariant):
    """

    variant: "ServerBISSubscriptionCreateQueryResourceObjectRelationshipsVariant"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        variant = self.variant.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "variant": variant,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.server_bis_subscription_create_query_resource_object_relationships_variant import (
            ServerBISSubscriptionCreateQueryResourceObjectRelationshipsVariant,
        )

        d = src_dict.copy()
        variant = ServerBISSubscriptionCreateQueryResourceObjectRelationshipsVariant.from_dict(d.pop("variant"))

        server_bis_subscription_create_query_resource_object_relationships = cls(
            variant=variant,
        )

        server_bis_subscription_create_query_resource_object_relationships.additional_properties = d
        return server_bis_subscription_create_query_resource_object_relationships

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
