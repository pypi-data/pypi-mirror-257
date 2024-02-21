import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.email_marketing_list_suppression import EmailMarketingListSuppression
    from ..models.email_marketing_suppression import EmailMarketingSuppression


T = TypeVar("T", bound="EmailMarketing")


@_attrs_define
class EmailMarketing:
    """
    Attributes:
        can_receive_email_marketing (bool): Whether or not this profile has implicit consent to receive email marketing.
            True if it does profile does not have any global suppressions.
        consent (str): The consent status for email marketing. Example: SUBSCRIBED.
        consent_timestamp (Union[Unset, datetime.datetime]): The timestamp when consent was recorded or updated for
            email marketing, in ISO 8601 format (YYYY-MM-DDTHH:MM:SS.mmmmmm). Example: 2023-02-21T20:07:38+00:00.
        last_updated (Union[Unset, datetime.datetime]): The timestamp when a field on the email marketing object was
            last modified. Example: 2023-02-21T20:07:38+00:00.
        method (Union[Unset, str]): The method by which the profile was subscribed to email marketing. Example:
            PREFERENCE_PAGE.
        method_detail (Union[Unset, str]): Additional details about the method by which the profile was subscribed to
            email marketing. This may be empty if no details were provided. Default: ''. Example: mydomain.com/signup.
        custom_method_detail (Union[Unset, str]): Additional detail provided by the caller when the profile was
            subscribed. This may be empty if no details were provided. Example: marketing drive.
        double_optin (Union[Unset, bool]): Whether the profile was subscribed to email marketing using a double opt-in.
            Example: True.
        suppression (Union[Unset, List['EmailMarketingSuppression']]): The global email marketing suppression for this
            profile.
        list_suppressions (Union[Unset, List['EmailMarketingListSuppression']]): The list suppressions for this profile.
    """

    can_receive_email_marketing: bool
    consent: str
    consent_timestamp: Union[Unset, datetime.datetime] = UNSET
    last_updated: Union[Unset, datetime.datetime] = UNSET
    method: Union[Unset, str] = UNSET
    method_detail: Union[Unset, str] = ""
    custom_method_detail: Union[Unset, str] = UNSET
    double_optin: Union[Unset, bool] = UNSET
    suppression: Union[Unset, List["EmailMarketingSuppression"]] = UNSET
    list_suppressions: Union[Unset, List["EmailMarketingListSuppression"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        can_receive_email_marketing = self.can_receive_email_marketing

        consent = self.consent

        consent_timestamp: Union[Unset, str] = UNSET
        if not isinstance(self.consent_timestamp, Unset):
            consent_timestamp = self.consent_timestamp.isoformat()

        last_updated: Union[Unset, str] = UNSET
        if not isinstance(self.last_updated, Unset):
            last_updated = self.last_updated.isoformat()

        method = self.method

        method_detail = self.method_detail

        custom_method_detail = self.custom_method_detail

        double_optin = self.double_optin

        suppression: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.suppression, Unset):
            suppression = []
            for suppression_item_data in self.suppression:
                suppression_item = suppression_item_data.to_dict()
                suppression.append(suppression_item)

        list_suppressions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.list_suppressions, Unset):
            list_suppressions = []
            for list_suppressions_item_data in self.list_suppressions:
                list_suppressions_item = list_suppressions_item_data.to_dict()
                list_suppressions.append(list_suppressions_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "can_receive_email_marketing": can_receive_email_marketing,
                "consent": consent,
            }
        )
        if consent_timestamp is not UNSET:
            field_dict["consent_timestamp"] = consent_timestamp
        if last_updated is not UNSET:
            field_dict["last_updated"] = last_updated
        if method is not UNSET:
            field_dict["method"] = method
        if method_detail is not UNSET:
            field_dict["method_detail"] = method_detail
        if custom_method_detail is not UNSET:
            field_dict["custom_method_detail"] = custom_method_detail
        if double_optin is not UNSET:
            field_dict["double_optin"] = double_optin
        if suppression is not UNSET:
            field_dict["suppression"] = suppression
        if list_suppressions is not UNSET:
            field_dict["list_suppressions"] = list_suppressions

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.email_marketing_list_suppression import EmailMarketingListSuppression
        from ..models.email_marketing_suppression import EmailMarketingSuppression

        d = src_dict.copy()
        can_receive_email_marketing = d.pop("can_receive_email_marketing")

        consent = d.pop("consent")

        _consent_timestamp = d.pop("consent_timestamp", UNSET)
        consent_timestamp: Union[Unset, datetime.datetime]
        if isinstance(_consent_timestamp, Unset):
            consent_timestamp = UNSET
        else:
            consent_timestamp = isoparse(_consent_timestamp)

        _last_updated = d.pop("last_updated", UNSET)
        last_updated: Union[Unset, datetime.datetime]
        if isinstance(_last_updated, Unset):
            last_updated = UNSET
        else:
            last_updated = isoparse(_last_updated)

        method = d.pop("method", UNSET)

        method_detail = d.pop("method_detail", UNSET)

        custom_method_detail = d.pop("custom_method_detail", UNSET)

        double_optin = d.pop("double_optin", UNSET)

        suppression = []
        _suppression = d.pop("suppression", UNSET)
        for suppression_item_data in _suppression or []:
            suppression_item = EmailMarketingSuppression.from_dict(suppression_item_data)

            suppression.append(suppression_item)

        list_suppressions = []
        _list_suppressions = d.pop("list_suppressions", UNSET)
        for list_suppressions_item_data in _list_suppressions or []:
            list_suppressions_item = EmailMarketingListSuppression.from_dict(list_suppressions_item_data)

            list_suppressions.append(list_suppressions_item)

        email_marketing = cls(
            can_receive_email_marketing=can_receive_email_marketing,
            consent=consent,
            consent_timestamp=consent_timestamp,
            last_updated=last_updated,
            method=method,
            method_detail=method_detail,
            custom_method_detail=custom_method_detail,
            double_optin=double_optin,
            suppression=suppression,
            list_suppressions=list_suppressions,
        )

        email_marketing.additional_properties = d
        return email_marketing

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
