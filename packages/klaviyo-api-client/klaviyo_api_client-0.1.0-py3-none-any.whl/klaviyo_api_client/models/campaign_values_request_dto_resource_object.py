from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.campaign_values_report_enum import CampaignValuesReportEnum

if TYPE_CHECKING:
    from ..models.campaign_values_request_dto_resource_object_attributes import (
        CampaignValuesRequestDTOResourceObjectAttributes,
    )


T = TypeVar("T", bound="CampaignValuesRequestDTOResourceObject")


@_attrs_define
class CampaignValuesRequestDTOResourceObject:
    """
    Attributes:
        type (CampaignValuesReportEnum):
        attributes (CampaignValuesRequestDTOResourceObjectAttributes):
    """

    type: CampaignValuesReportEnum
    attributes: "CampaignValuesRequestDTOResourceObjectAttributes"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        attributes = self.attributes.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "attributes": attributes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.campaign_values_request_dto_resource_object_attributes import (
            CampaignValuesRequestDTOResourceObjectAttributes,
        )

        d = src_dict.copy()
        type = CampaignValuesReportEnum(d.pop("type"))

        attributes = CampaignValuesRequestDTOResourceObjectAttributes.from_dict(d.pop("attributes"))

        campaign_values_request_dto_resource_object = cls(
            type=type,
            attributes=attributes,
        )

        campaign_values_request_dto_resource_object.additional_properties = d
        return campaign_values_request_dto_resource_object

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
