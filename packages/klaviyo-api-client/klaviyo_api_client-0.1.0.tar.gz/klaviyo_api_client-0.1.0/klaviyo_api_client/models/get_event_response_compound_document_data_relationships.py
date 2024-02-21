from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_event_response_compound_document_data_relationships_attributions import (
        GetEventResponseCompoundDocumentDataRelationshipsAttributions,
    )
    from ..models.get_event_response_compound_document_data_relationships_metric import (
        GetEventResponseCompoundDocumentDataRelationshipsMetric,
    )
    from ..models.get_event_response_compound_document_data_relationships_profile import (
        GetEventResponseCompoundDocumentDataRelationshipsProfile,
    )


T = TypeVar("T", bound="GetEventResponseCompoundDocumentDataRelationships")


@_attrs_define
class GetEventResponseCompoundDocumentDataRelationships:
    """
    Attributes:
        profile (Union[Unset, GetEventResponseCompoundDocumentDataRelationshipsProfile]):
        metric (Union[Unset, GetEventResponseCompoundDocumentDataRelationshipsMetric]):
        attributions (Union[Unset, GetEventResponseCompoundDocumentDataRelationshipsAttributions]):
    """

    profile: Union[Unset, "GetEventResponseCompoundDocumentDataRelationshipsProfile"] = UNSET
    metric: Union[Unset, "GetEventResponseCompoundDocumentDataRelationshipsMetric"] = UNSET
    attributions: Union[Unset, "GetEventResponseCompoundDocumentDataRelationshipsAttributions"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        profile: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.profile, Unset):
            profile = self.profile.to_dict()

        metric: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.metric, Unset):
            metric = self.metric.to_dict()

        attributions: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.attributions, Unset):
            attributions = self.attributions.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if profile is not UNSET:
            field_dict["profile"] = profile
        if metric is not UNSET:
            field_dict["metric"] = metric
        if attributions is not UNSET:
            field_dict["attributions"] = attributions

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_event_response_compound_document_data_relationships_attributions import (
            GetEventResponseCompoundDocumentDataRelationshipsAttributions,
        )
        from ..models.get_event_response_compound_document_data_relationships_metric import (
            GetEventResponseCompoundDocumentDataRelationshipsMetric,
        )
        from ..models.get_event_response_compound_document_data_relationships_profile import (
            GetEventResponseCompoundDocumentDataRelationshipsProfile,
        )

        d = src_dict.copy()
        _profile = d.pop("profile", UNSET)
        profile: Union[Unset, GetEventResponseCompoundDocumentDataRelationshipsProfile]
        if isinstance(_profile, Unset):
            profile = UNSET
        else:
            profile = GetEventResponseCompoundDocumentDataRelationshipsProfile.from_dict(_profile)

        _metric = d.pop("metric", UNSET)
        metric: Union[Unset, GetEventResponseCompoundDocumentDataRelationshipsMetric]
        if isinstance(_metric, Unset):
            metric = UNSET
        else:
            metric = GetEventResponseCompoundDocumentDataRelationshipsMetric.from_dict(_metric)

        _attributions = d.pop("attributions", UNSET)
        attributions: Union[Unset, GetEventResponseCompoundDocumentDataRelationshipsAttributions]
        if isinstance(_attributions, Unset):
            attributions = UNSET
        else:
            attributions = GetEventResponseCompoundDocumentDataRelationshipsAttributions.from_dict(_attributions)

        get_event_response_compound_document_data_relationships = cls(
            profile=profile,
            metric=metric,
            attributions=attributions,
        )

        get_event_response_compound_document_data_relationships.additional_properties = d
        return get_event_response_compound_document_data_relationships

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
