from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.profile_import_job_create_query_resource_object_relationships_lists import (
        ProfileImportJobCreateQueryResourceObjectRelationshipsLists,
    )


T = TypeVar("T", bound="ProfileImportJobCreateQueryResourceObjectRelationships")


@_attrs_define
class ProfileImportJobCreateQueryResourceObjectRelationships:
    """
    Attributes:
        lists (Union[Unset, ProfileImportJobCreateQueryResourceObjectRelationshipsLists]):
    """

    lists: Union[Unset, "ProfileImportJobCreateQueryResourceObjectRelationshipsLists"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        lists: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.lists, Unset):
            lists = self.lists.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if lists is not UNSET:
            field_dict["lists"] = lists

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.profile_import_job_create_query_resource_object_relationships_lists import (
            ProfileImportJobCreateQueryResourceObjectRelationshipsLists,
        )

        d = src_dict.copy()
        _lists = d.pop("lists", UNSET)
        lists: Union[Unset, ProfileImportJobCreateQueryResourceObjectRelationshipsLists]
        if isinstance(_lists, Unset):
            lists = UNSET
        else:
            lists = ProfileImportJobCreateQueryResourceObjectRelationshipsLists.from_dict(_lists)

        profile_import_job_create_query_resource_object_relationships = cls(
            lists=lists,
        )

        profile_import_job_create_query_resource_object_relationships.additional_properties = d
        return profile_import_job_create_query_resource_object_relationships

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
