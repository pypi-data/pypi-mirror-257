import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.post_catalog_item_create_job_response_data_attributes_status import (
    PostCatalogItemCreateJobResponseDataAttributesStatus,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.api_job_error_payload import APIJobErrorPayload


T = TypeVar("T", bound="PostCatalogItemCreateJobResponseDataAttributes")


@_attrs_define
class PostCatalogItemCreateJobResponseDataAttributes:
    """
    Attributes:
        status (PostCatalogItemCreateJobResponseDataAttributesStatus): Status of the asynchronous job. Example:
            processing.
        created_at (datetime.datetime): The date and time the job was created in ISO 8601 format (YYYY-MM-
            DDTHH:MM:SS.mmmmmm). Example: 2022-11-08T00:00:00.
        total_count (int): The total number of operations to be processed by the job. See `completed_count` for the
            job's current progress. Example: 10.
        completed_count (Union[Unset, int]): The total number of operations that have been completed by the job.
            Default: 0. Example: 9.
        failed_count (Union[Unset, int]): The total number of operations that have failed as part of the job. Default:
            0. Example: 1.
        completed_at (Union[Unset, datetime.datetime]): Date and time the job was completed in ISO 8601 format (YYYY-MM-
            DDTHH:MM:SS.mmmmmm). Example: 2022-11-08T00:00:00.
        errors (Union[Unset, List['APIJobErrorPayload']]): Array of errors encountered during the processing of the job.
        expires_at (Union[Unset, datetime.datetime]): Date and time the job expires in ISO 8601 format (YYYY-MM-
            DDTHH:MM:SS.mmmmmm). Example: 2022-11-08T00:00:00.
    """

    status: PostCatalogItemCreateJobResponseDataAttributesStatus
    created_at: datetime.datetime
    total_count: int
    completed_count: Union[Unset, int] = 0
    failed_count: Union[Unset, int] = 0
    completed_at: Union[Unset, datetime.datetime] = UNSET
    errors: Union[Unset, List["APIJobErrorPayload"]] = UNSET
    expires_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        status = self.status.value

        created_at = self.created_at.isoformat()

        total_count = self.total_count

        completed_count = self.completed_count

        failed_count = self.failed_count

        completed_at: Union[Unset, str] = UNSET
        if not isinstance(self.completed_at, Unset):
            completed_at = self.completed_at.isoformat()

        errors: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.errors, Unset):
            errors = []
            for errors_item_data in self.errors:
                errors_item = errors_item_data.to_dict()
                errors.append(errors_item)

        expires_at: Union[Unset, str] = UNSET
        if not isinstance(self.expires_at, Unset):
            expires_at = self.expires_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
                "created_at": created_at,
                "total_count": total_count,
            }
        )
        if completed_count is not UNSET:
            field_dict["completed_count"] = completed_count
        if failed_count is not UNSET:
            field_dict["failed_count"] = failed_count
        if completed_at is not UNSET:
            field_dict["completed_at"] = completed_at
        if errors is not UNSET:
            field_dict["errors"] = errors
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.api_job_error_payload import APIJobErrorPayload

        d = src_dict.copy()
        status = PostCatalogItemCreateJobResponseDataAttributesStatus(d.pop("status"))

        created_at = isoparse(d.pop("created_at"))

        total_count = d.pop("total_count")

        completed_count = d.pop("completed_count", UNSET)

        failed_count = d.pop("failed_count", UNSET)

        _completed_at = d.pop("completed_at", UNSET)
        completed_at: Union[Unset, datetime.datetime]
        if isinstance(_completed_at, Unset):
            completed_at = UNSET
        else:
            completed_at = isoparse(_completed_at)

        errors = []
        _errors = d.pop("errors", UNSET)
        for errors_item_data in _errors or []:
            errors_item = APIJobErrorPayload.from_dict(errors_item_data)

            errors.append(errors_item)

        _expires_at = d.pop("expires_at", UNSET)
        expires_at: Union[Unset, datetime.datetime]
        if isinstance(_expires_at, Unset):
            expires_at = UNSET
        else:
            expires_at = isoparse(_expires_at)

        post_catalog_item_create_job_response_data_attributes = cls(
            status=status,
            created_at=created_at,
            total_count=total_count,
            completed_count=completed_count,
            failed_count=failed_count,
            completed_at=completed_at,
            errors=errors,
            expires_at=expires_at,
        )

        post_catalog_item_create_job_response_data_attributes.additional_properties = d
        return post_catalog_item_create_job_response_data_attributes

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
