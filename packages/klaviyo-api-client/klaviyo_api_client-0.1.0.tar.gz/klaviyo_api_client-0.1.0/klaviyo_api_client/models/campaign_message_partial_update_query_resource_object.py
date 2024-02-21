from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.campaign_message_enum import CampaignMessageEnum

if TYPE_CHECKING:
    from ..models.campaign_message_partial_update_query_resource_object_attributes import (
        CampaignMessagePartialUpdateQueryResourceObjectAttributes,
    )


T = TypeVar("T", bound="CampaignMessagePartialUpdateQueryResourceObject")


@_attrs_define
class CampaignMessagePartialUpdateQueryResourceObject:
    """
    Attributes:
        type (CampaignMessageEnum):
        id (str): The message ID to be retrieved
        attributes (CampaignMessagePartialUpdateQueryResourceObjectAttributes):
    """

    type: CampaignMessageEnum
    id: str
    attributes: "CampaignMessagePartialUpdateQueryResourceObjectAttributes"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        id = self.id

        attributes = self.attributes.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "id": id,
                "attributes": attributes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.campaign_message_partial_update_query_resource_object_attributes import (
            CampaignMessagePartialUpdateQueryResourceObjectAttributes,
        )

        d = src_dict.copy()
        type = CampaignMessageEnum(d.pop("type"))

        id = d.pop("id")

        attributes = CampaignMessagePartialUpdateQueryResourceObjectAttributes.from_dict(d.pop("attributes"))

        campaign_message_partial_update_query_resource_object = cls(
            type=type,
            id=id,
            attributes=attributes,
        )

        campaign_message_partial_update_query_resource_object.additional_properties = d
        return campaign_message_partial_update_query_resource_object

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
