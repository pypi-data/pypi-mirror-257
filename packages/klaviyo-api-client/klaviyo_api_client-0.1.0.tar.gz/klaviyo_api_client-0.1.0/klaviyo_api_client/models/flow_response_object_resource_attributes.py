import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.flow_response_object_resource_attributes_trigger_type import (
    FlowResponseObjectResourceAttributesTriggerType,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="FlowResponseObjectResourceAttributes")


@_attrs_define
class FlowResponseObjectResourceAttributes:
    """
    Attributes:
        name (Union[Unset, str]):
        status (Union[Unset, str]):
        archived (Union[Unset, bool]):
        created (Union[Unset, datetime.datetime]):  Example: 2022-11-08T00:00:00.
        updated (Union[Unset, datetime.datetime]):  Example: 2022-11-08T00:00:00.
        trigger_type (Union[Unset, FlowResponseObjectResourceAttributesTriggerType]): Corresponds to the object which
            triggered the flow.
    """

    name: Union[Unset, str] = UNSET
    status: Union[Unset, str] = UNSET
    archived: Union[Unset, bool] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    updated: Union[Unset, datetime.datetime] = UNSET
    trigger_type: Union[Unset, FlowResponseObjectResourceAttributesTriggerType] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        status = self.status

        archived = self.archived

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        updated: Union[Unset, str] = UNSET
        if not isinstance(self.updated, Unset):
            updated = self.updated.isoformat()

        trigger_type: Union[Unset, str] = UNSET
        if not isinstance(self.trigger_type, Unset):
            trigger_type = self.trigger_type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if status is not UNSET:
            field_dict["status"] = status
        if archived is not UNSET:
            field_dict["archived"] = archived
        if created is not UNSET:
            field_dict["created"] = created
        if updated is not UNSET:
            field_dict["updated"] = updated
        if trigger_type is not UNSET:
            field_dict["trigger_type"] = trigger_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        status = d.pop("status", UNSET)

        archived = d.pop("archived", UNSET)

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset):
            created = UNSET
        else:
            created = isoparse(_created)

        _updated = d.pop("updated", UNSET)
        updated: Union[Unset, datetime.datetime]
        if isinstance(_updated, Unset):
            updated = UNSET
        else:
            updated = isoparse(_updated)

        _trigger_type = d.pop("trigger_type", UNSET)
        trigger_type: Union[Unset, FlowResponseObjectResourceAttributesTriggerType]
        if isinstance(_trigger_type, Unset):
            trigger_type = UNSET
        else:
            trigger_type = FlowResponseObjectResourceAttributesTriggerType(_trigger_type)

        flow_response_object_resource_attributes = cls(
            name=name,
            status=status,
            archived=archived,
            created=created,
            updated=updated,
            trigger_type=trigger_type,
        )

        flow_response_object_resource_attributes.additional_properties = d
        return flow_response_object_resource_attributes

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
