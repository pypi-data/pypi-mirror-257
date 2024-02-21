from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_profile_import_job_response_compound_document_data_relationships_import_errors import (
        GetProfileImportJobResponseCompoundDocumentDataRelationshipsImportErrors,
    )
    from ..models.get_profile_import_job_response_compound_document_data_relationships_lists import (
        GetProfileImportJobResponseCompoundDocumentDataRelationshipsLists,
    )
    from ..models.get_profile_import_job_response_compound_document_data_relationships_profiles import (
        GetProfileImportJobResponseCompoundDocumentDataRelationshipsProfiles,
    )


T = TypeVar("T", bound="GetProfileImportJobResponseCompoundDocumentDataRelationships")


@_attrs_define
class GetProfileImportJobResponseCompoundDocumentDataRelationships:
    """
    Attributes:
        lists (Union[Unset, GetProfileImportJobResponseCompoundDocumentDataRelationshipsLists]):
        profiles (Union[Unset, GetProfileImportJobResponseCompoundDocumentDataRelationshipsProfiles]):
        import_errors (Union[Unset, GetProfileImportJobResponseCompoundDocumentDataRelationshipsImportErrors]):
    """

    lists: Union[Unset, "GetProfileImportJobResponseCompoundDocumentDataRelationshipsLists"] = UNSET
    profiles: Union[Unset, "GetProfileImportJobResponseCompoundDocumentDataRelationshipsProfiles"] = UNSET
    import_errors: Union[Unset, "GetProfileImportJobResponseCompoundDocumentDataRelationshipsImportErrors"] = UNSET
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
        from ..models.get_profile_import_job_response_compound_document_data_relationships_import_errors import (
            GetProfileImportJobResponseCompoundDocumentDataRelationshipsImportErrors,
        )
        from ..models.get_profile_import_job_response_compound_document_data_relationships_lists import (
            GetProfileImportJobResponseCompoundDocumentDataRelationshipsLists,
        )
        from ..models.get_profile_import_job_response_compound_document_data_relationships_profiles import (
            GetProfileImportJobResponseCompoundDocumentDataRelationshipsProfiles,
        )

        d = src_dict.copy()
        _lists = d.pop("lists", UNSET)
        lists: Union[Unset, GetProfileImportJobResponseCompoundDocumentDataRelationshipsLists]
        if isinstance(_lists, Unset):
            lists = UNSET
        else:
            lists = GetProfileImportJobResponseCompoundDocumentDataRelationshipsLists.from_dict(_lists)

        _profiles = d.pop("profiles", UNSET)
        profiles: Union[Unset, GetProfileImportJobResponseCompoundDocumentDataRelationshipsProfiles]
        if isinstance(_profiles, Unset):
            profiles = UNSET
        else:
            profiles = GetProfileImportJobResponseCompoundDocumentDataRelationshipsProfiles.from_dict(_profiles)

        _import_errors = d.pop("import-errors", UNSET)
        import_errors: Union[Unset, GetProfileImportJobResponseCompoundDocumentDataRelationshipsImportErrors]
        if isinstance(_import_errors, Unset):
            import_errors = UNSET
        else:
            import_errors = GetProfileImportJobResponseCompoundDocumentDataRelationshipsImportErrors.from_dict(
                _import_errors
            )

        get_profile_import_job_response_compound_document_data_relationships = cls(
            lists=lists,
            profiles=profiles,
            import_errors=import_errors,
        )

        get_profile_import_job_response_compound_document_data_relationships.additional_properties = d
        return get_profile_import_job_response_compound_document_data_relationships

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
