from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_flow_message_response_compound_document_data_relationships_flow_action import (
        GetFlowMessageResponseCompoundDocumentDataRelationshipsFlowAction,
    )
    from ..models.get_flow_message_response_compound_document_data_relationships_template import (
        GetFlowMessageResponseCompoundDocumentDataRelationshipsTemplate,
    )


T = TypeVar("T", bound="GetFlowMessageResponseCompoundDocumentDataRelationships")


@_attrs_define
class GetFlowMessageResponseCompoundDocumentDataRelationships:
    """
    Attributes:
        flow_action (Union[Unset, GetFlowMessageResponseCompoundDocumentDataRelationshipsFlowAction]):
        template (Union[Unset, GetFlowMessageResponseCompoundDocumentDataRelationshipsTemplate]):
    """

    flow_action: Union[Unset, "GetFlowMessageResponseCompoundDocumentDataRelationshipsFlowAction"] = UNSET
    template: Union[Unset, "GetFlowMessageResponseCompoundDocumentDataRelationshipsTemplate"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        flow_action: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.flow_action, Unset):
            flow_action = self.flow_action.to_dict()

        template: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.template, Unset):
            template = self.template.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if flow_action is not UNSET:
            field_dict["flow-action"] = flow_action
        if template is not UNSET:
            field_dict["template"] = template

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_flow_message_response_compound_document_data_relationships_flow_action import (
            GetFlowMessageResponseCompoundDocumentDataRelationshipsFlowAction,
        )
        from ..models.get_flow_message_response_compound_document_data_relationships_template import (
            GetFlowMessageResponseCompoundDocumentDataRelationshipsTemplate,
        )

        d = src_dict.copy()
        _flow_action = d.pop("flow-action", UNSET)
        flow_action: Union[Unset, GetFlowMessageResponseCompoundDocumentDataRelationshipsFlowAction]
        if isinstance(_flow_action, Unset):
            flow_action = UNSET
        else:
            flow_action = GetFlowMessageResponseCompoundDocumentDataRelationshipsFlowAction.from_dict(_flow_action)

        _template = d.pop("template", UNSET)
        template: Union[Unset, GetFlowMessageResponseCompoundDocumentDataRelationshipsTemplate]
        if isinstance(_template, Unset):
            template = UNSET
        else:
            template = GetFlowMessageResponseCompoundDocumentDataRelationshipsTemplate.from_dict(_template)

        get_flow_message_response_compound_document_data_relationships = cls(
            flow_action=flow_action,
            template=template,
        )

        get_flow_message_response_compound_document_data_relationships.additional_properties = d
        return get_flow_message_response_compound_document_data_relationships

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
