from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_flow_message_response_collection_data_item_relationships_flow_action import (
        GetFlowMessageResponseCollectionDataItemRelationshipsFlowAction,
    )
    from ..models.get_flow_message_response_collection_data_item_relationships_template import (
        GetFlowMessageResponseCollectionDataItemRelationshipsTemplate,
    )


T = TypeVar("T", bound="GetFlowMessageResponseCollectionDataItemRelationships")


@_attrs_define
class GetFlowMessageResponseCollectionDataItemRelationships:
    """
    Attributes:
        flow_action (Union[Unset, GetFlowMessageResponseCollectionDataItemRelationshipsFlowAction]):
        template (Union[Unset, GetFlowMessageResponseCollectionDataItemRelationshipsTemplate]):
    """

    flow_action: Union[Unset, "GetFlowMessageResponseCollectionDataItemRelationshipsFlowAction"] = UNSET
    template: Union[Unset, "GetFlowMessageResponseCollectionDataItemRelationshipsTemplate"] = UNSET
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
        from ..models.get_flow_message_response_collection_data_item_relationships_flow_action import (
            GetFlowMessageResponseCollectionDataItemRelationshipsFlowAction,
        )
        from ..models.get_flow_message_response_collection_data_item_relationships_template import (
            GetFlowMessageResponseCollectionDataItemRelationshipsTemplate,
        )

        d = src_dict.copy()
        _flow_action = d.pop("flow-action", UNSET)
        flow_action: Union[Unset, GetFlowMessageResponseCollectionDataItemRelationshipsFlowAction]
        if isinstance(_flow_action, Unset):
            flow_action = UNSET
        else:
            flow_action = GetFlowMessageResponseCollectionDataItemRelationshipsFlowAction.from_dict(_flow_action)

        _template = d.pop("template", UNSET)
        template: Union[Unset, GetFlowMessageResponseCollectionDataItemRelationshipsTemplate]
        if isinstance(_template, Unset):
            template = UNSET
        else:
            template = GetFlowMessageResponseCollectionDataItemRelationshipsTemplate.from_dict(_template)

        get_flow_message_response_collection_data_item_relationships = cls(
            flow_action=flow_action,
            template=template,
        )

        get_flow_message_response_collection_data_item_relationships.additional_properties = d
        return get_flow_message_response_collection_data_item_relationships

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
