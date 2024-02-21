from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.flow_message_response_object_resource import FlowMessageResponseObjectResource
    from ..models.flow_response_object_resource import FlowResponseObjectResource
    from ..models.get_flow_action_response_compound_document_data import GetFlowActionResponseCompoundDocumentData


T = TypeVar("T", bound="GetFlowActionResponseCompoundDocument")


@_attrs_define
class GetFlowActionResponseCompoundDocument:
    """
    Attributes:
        data (GetFlowActionResponseCompoundDocumentData):
        included (Union[Unset, List[Union['FlowMessageResponseObjectResource', 'FlowResponseObjectResource']]]):
    """

    data: "GetFlowActionResponseCompoundDocumentData"
    included: Union[Unset, List[Union["FlowMessageResponseObjectResource", "FlowResponseObjectResource"]]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.flow_response_object_resource import FlowResponseObjectResource

        data = self.data.to_dict()

        included: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.included, Unset):
            included = []
            for included_item_data in self.included:
                included_item: Dict[str, Any]
                if isinstance(included_item_data, FlowResponseObjectResource):
                    included_item = included_item_data.to_dict()
                else:
                    included_item = included_item_data.to_dict()

                included.append(included_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
            }
        )
        if included is not UNSET:
            field_dict["included"] = included

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.flow_message_response_object_resource import FlowMessageResponseObjectResource
        from ..models.flow_response_object_resource import FlowResponseObjectResource
        from ..models.get_flow_action_response_compound_document_data import GetFlowActionResponseCompoundDocumentData

        d = src_dict.copy()
        data = GetFlowActionResponseCompoundDocumentData.from_dict(d.pop("data"))

        included = []
        _included = d.pop("included", UNSET)
        for included_item_data in _included or []:

            def _parse_included_item(
                data: object,
            ) -> Union["FlowMessageResponseObjectResource", "FlowResponseObjectResource"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    included_item_type_0 = FlowResponseObjectResource.from_dict(data)

                    return included_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                included_item_type_1 = FlowMessageResponseObjectResource.from_dict(data)

                return included_item_type_1

            included_item = _parse_included_item(included_item_data)

            included.append(included_item)

        get_flow_action_response_compound_document = cls(
            data=data,
            included=included,
        )

        get_flow_action_response_compound_document.additional_properties = d
        return get_flow_action_response_compound_document

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
