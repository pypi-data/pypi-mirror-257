from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.subscription_delete_job_create_query_resource_object_relationships_list import (
        SubscriptionDeleteJobCreateQueryResourceObjectRelationshipsList,
    )


T = TypeVar("T", bound="SubscriptionDeleteJobCreateQueryResourceObjectRelationships")


@_attrs_define
class SubscriptionDeleteJobCreateQueryResourceObjectRelationships:
    """
    Attributes:
        list_ (Union[Unset, SubscriptionDeleteJobCreateQueryResourceObjectRelationshipsList]):
    """

    list_: Union[Unset, "SubscriptionDeleteJobCreateQueryResourceObjectRelationshipsList"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        list_: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.list_, Unset):
            list_ = self.list_.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if list_ is not UNSET:
            field_dict["list"] = list_

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.subscription_delete_job_create_query_resource_object_relationships_list import (
            SubscriptionDeleteJobCreateQueryResourceObjectRelationshipsList,
        )

        d = src_dict.copy()
        _list_ = d.pop("list", UNSET)
        list_: Union[Unset, SubscriptionDeleteJobCreateQueryResourceObjectRelationshipsList]
        if isinstance(_list_, Unset):
            list_ = UNSET
        else:
            list_ = SubscriptionDeleteJobCreateQueryResourceObjectRelationshipsList.from_dict(_list_)

        subscription_delete_job_create_query_resource_object_relationships = cls(
            list_=list_,
        )

        subscription_delete_job_create_query_resource_object_relationships.additional_properties = d
        return subscription_delete_job_create_query_resource_object_relationships

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
