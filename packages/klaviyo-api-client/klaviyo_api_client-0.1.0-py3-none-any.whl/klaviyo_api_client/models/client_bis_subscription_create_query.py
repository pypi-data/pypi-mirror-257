from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.client_bis_subscription_create_query_resource_object import (
        ClientBISSubscriptionCreateQueryResourceObject,
    )


T = TypeVar("T", bound="ClientBISSubscriptionCreateQuery")


@_attrs_define
class ClientBISSubscriptionCreateQuery:
    """
    Attributes:
        data (ClientBISSubscriptionCreateQueryResourceObject):
    """

    data: "ClientBISSubscriptionCreateQueryResourceObject"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = self.data.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.client_bis_subscription_create_query_resource_object import (
            ClientBISSubscriptionCreateQueryResourceObject,
        )

        d = src_dict.copy()
        data = ClientBISSubscriptionCreateQueryResourceObject.from_dict(d.pop("data"))

        client_bis_subscription_create_query = cls(
            data=data,
        )

        client_bis_subscription_create_query.additional_properties = d
        return client_bis_subscription_create_query

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
