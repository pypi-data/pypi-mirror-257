from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.post_profile_import_job_response_data_relationships_import_errors import (
        PostProfileImportJobResponseDataRelationshipsImportErrors,
    )
    from ..models.post_profile_import_job_response_data_relationships_lists import (
        PostProfileImportJobResponseDataRelationshipsLists,
    )
    from ..models.post_profile_import_job_response_data_relationships_profiles import (
        PostProfileImportJobResponseDataRelationshipsProfiles,
    )


T = TypeVar("T", bound="PostProfileImportJobResponseDataRelationships")


@_attrs_define
class PostProfileImportJobResponseDataRelationships:
    """
    Attributes:
        lists (Union[Unset, PostProfileImportJobResponseDataRelationshipsLists]):
        profiles (Union[Unset, PostProfileImportJobResponseDataRelationshipsProfiles]):
        import_errors (Union[Unset, PostProfileImportJobResponseDataRelationshipsImportErrors]):
    """

    lists: Union[Unset, "PostProfileImportJobResponseDataRelationshipsLists"] = UNSET
    profiles: Union[Unset, "PostProfileImportJobResponseDataRelationshipsProfiles"] = UNSET
    import_errors: Union[Unset, "PostProfileImportJobResponseDataRelationshipsImportErrors"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        lists: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.lists, Unset):
            lists = self.lists.to_dict()

        profiles: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.profiles, Unset):
            profiles = self.profiles.to_dict()

        import_errors: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.import_errors, Unset):
            import_errors = self.import_errors.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if lists is not UNSET:
            field_dict["lists"] = lists
        if profiles is not UNSET:
            field_dict["profiles"] = profiles
        if import_errors is not UNSET:
            field_dict["import-errors"] = import_errors

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.post_profile_import_job_response_data_relationships_import_errors import (
            PostProfileImportJobResponseDataRelationshipsImportErrors,
        )
        from ..models.post_profile_import_job_response_data_relationships_lists import (
            PostProfileImportJobResponseDataRelationshipsLists,
        )
        from ..models.post_profile_import_job_response_data_relationships_profiles import (
            PostProfileImportJobResponseDataRelationshipsProfiles,
        )

        d = src_dict.copy()
        _lists = d.pop("lists", UNSET)
        lists: Union[Unset, PostProfileImportJobResponseDataRelationshipsLists]
        if isinstance(_lists, Unset):
            lists = UNSET
        else:
            lists = PostProfileImportJobResponseDataRelationshipsLists.from_dict(_lists)

        _profiles = d.pop("profiles", UNSET)
        profiles: Union[Unset, PostProfileImportJobResponseDataRelationshipsProfiles]
        if isinstance(_profiles, Unset):
            profiles = UNSET
        else:
            profiles = PostProfileImportJobResponseDataRelationshipsProfiles.from_dict(_profiles)

        _import_errors = d.pop("import-errors", UNSET)
        import_errors: Union[Unset, PostProfileImportJobResponseDataRelationshipsImportErrors]
        if isinstance(_import_errors, Unset):
            import_errors = UNSET
        else:
            import_errors = PostProfileImportJobResponseDataRelationshipsImportErrors.from_dict(_import_errors)

        post_profile_import_job_response_data_relationships = cls(
            lists=lists,
            profiles=profiles,
            import_errors=import_errors,
        )

        post_profile_import_job_response_data_relationships.additional_properties = d
        return post_profile_import_job_response_data_relationships

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
