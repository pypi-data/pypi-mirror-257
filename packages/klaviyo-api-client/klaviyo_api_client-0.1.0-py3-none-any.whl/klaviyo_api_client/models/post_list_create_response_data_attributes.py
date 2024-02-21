import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.post_list_create_response_data_attributes_opt_in_process import (
    PostListCreateResponseDataAttributesOptInProcess,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="PostListCreateResponseDataAttributes")


@_attrs_define
class PostListCreateResponseDataAttributes:
    """
    Attributes:
        name (Union[Unset, str]): A helpful name to label the list Example: Newsletter.
        created (Union[Unset, datetime.datetime]): Date and time when the list was created, in ISO 8601 format (YYYY-MM-
            DDTHH:MM:SS.mmmmmm) Example: 2022-11-08T00:00:00.
        updated (Union[Unset, datetime.datetime]): Date and time when the list was last updated, in ISO 8601 format
            (YYYY-MM-DDTHH:MM:SS.mmmmmm) Example: 2022-11-08T00:00:00.
        opt_in_process (Union[Unset, PostListCreateResponseDataAttributesOptInProcess]): The opt-in process for this
            list.  Could be either 'single_opt_in' or 'double_opt_in'.
    """

    name: Union[Unset, str] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    updated: Union[Unset, datetime.datetime] = UNSET
    opt_in_process: Union[Unset, PostListCreateResponseDataAttributesOptInProcess] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        updated: Union[Unset, str] = UNSET
        if not isinstance(self.updated, Unset):
            updated = self.updated.isoformat()

        opt_in_process: Union[Unset, str] = UNSET
        if not isinstance(self.opt_in_process, Unset):
            opt_in_process = self.opt_in_process.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if created is not UNSET:
            field_dict["created"] = created
        if updated is not UNSET:
            field_dict["updated"] = updated
        if opt_in_process is not UNSET:
            field_dict["opt_in_process"] = opt_in_process

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

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

        _opt_in_process = d.pop("opt_in_process", UNSET)
        opt_in_process: Union[Unset, PostListCreateResponseDataAttributesOptInProcess]
        if isinstance(_opt_in_process, Unset):
            opt_in_process = UNSET
        else:
            opt_in_process = PostListCreateResponseDataAttributesOptInProcess(_opt_in_process)

        post_list_create_response_data_attributes = cls(
            name=name,
            created=created,
            updated=updated,
            opt_in_process=opt_in_process,
        )

        post_list_create_response_data_attributes.additional_properties = d
        return post_list_create_response_data_attributes

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
