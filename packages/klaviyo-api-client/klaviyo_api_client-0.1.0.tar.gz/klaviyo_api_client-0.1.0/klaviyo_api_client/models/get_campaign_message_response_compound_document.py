from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.campaign_response_object_resource import CampaignResponseObjectResource
    from ..models.get_campaign_message_response_compound_document_data import (
        GetCampaignMessageResponseCompoundDocumentData,
    )
    from ..models.template_response_object_resource import TemplateResponseObjectResource


T = TypeVar("T", bound="GetCampaignMessageResponseCompoundDocument")


@_attrs_define
class GetCampaignMessageResponseCompoundDocument:
    """
    Attributes:
        data (GetCampaignMessageResponseCompoundDocumentData):
        included (Union[Unset, List[Union['CampaignResponseObjectResource', 'TemplateResponseObjectResource']]]):
    """

    data: "GetCampaignMessageResponseCompoundDocumentData"
    included: Union[Unset, List[Union["CampaignResponseObjectResource", "TemplateResponseObjectResource"]]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.campaign_response_object_resource import CampaignResponseObjectResource

        data = self.data.to_dict()

        included: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.included, Unset):
            included = []
            for included_item_data in self.included:
                included_item: Dict[str, Any]
                if isinstance(included_item_data, CampaignResponseObjectResource):
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
        from ..models.campaign_response_object_resource import CampaignResponseObjectResource
        from ..models.get_campaign_message_response_compound_document_data import (
            GetCampaignMessageResponseCompoundDocumentData,
        )
        from ..models.template_response_object_resource import TemplateResponseObjectResource

        d = src_dict.copy()
        data = GetCampaignMessageResponseCompoundDocumentData.from_dict(d.pop("data"))

        included = []
        _included = d.pop("included", UNSET)
        for included_item_data in _included or []:

            def _parse_included_item(
                data: object,
            ) -> Union["CampaignResponseObjectResource", "TemplateResponseObjectResource"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    included_item_type_0 = CampaignResponseObjectResource.from_dict(data)

                    return included_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                included_item_type_1 = TemplateResponseObjectResource.from_dict(data)

                return included_item_type_1

            included_item = _parse_included_item(included_item_data)

            included.append(included_item)

        get_campaign_message_response_compound_document = cls(
            data=data,
            included=included,
        )

        get_campaign_message_response_compound_document.additional_properties = d
        return get_campaign_message_response_compound_document

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
