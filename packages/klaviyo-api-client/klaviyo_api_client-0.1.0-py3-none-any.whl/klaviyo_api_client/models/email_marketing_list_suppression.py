import datetime
from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="EmailMarketingListSuppression")


@_attrs_define
class EmailMarketingListSuppression:
    """
    Attributes:
        list_id (str): The ID of list to which the suppression applies. Example: Y6nRLr.
        reason (str): The reason the profile was suppressed from the list. Example: USER_SUPPRESSED.
        timestamp (datetime.datetime): The timestamp when the profile was suppressed from the list, in ISO 8601 format
            (YYYY-MM-DDTHH:MM:SS.mmmmmm). Example: 2023-02-21T20:07:38+00:00.
    """

    list_id: str
    reason: str
    timestamp: datetime.datetime
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        list_id = self.list_id

        reason = self.reason

        timestamp = self.timestamp.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "list_id": list_id,
                "reason": reason,
                "timestamp": timestamp,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        list_id = d.pop("list_id")

        reason = d.pop("reason")

        timestamp = isoparse(d.pop("timestamp"))

        email_marketing_list_suppression = cls(
            list_id=list_id,
            reason=reason,
            timestamp=timestamp,
        )

        email_marketing_list_suppression.additional_properties = d
        return email_marketing_list_suppression

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
