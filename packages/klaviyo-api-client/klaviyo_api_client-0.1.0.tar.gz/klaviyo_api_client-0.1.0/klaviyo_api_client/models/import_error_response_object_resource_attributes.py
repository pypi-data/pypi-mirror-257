from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.error_source import ErrorSource
    from ..models.import_error_response_object_resource_attributes_original_payload import (
        ImportErrorResponseObjectResourceAttributesOriginalPayload,
    )


T = TypeVar("T", bound="ImportErrorResponseObjectResourceAttributes")


@_attrs_define
class ImportErrorResponseObjectResourceAttributes:
    """
    Attributes:
        code (str): A code for classifying the error type. Example: invalid.
        title (str): A high-level message about the error. Example: Invalid input.
        detail (str): Specific details about the error. Example: The payload provided in the request is invalid..
        source (ErrorSource):
        original_payload (Union[Unset, ImportErrorResponseObjectResourceAttributesOriginalPayload]):
    """

    code: str
    title: str
    detail: str
    source: "ErrorSource"
    original_payload: Union[Unset, "ImportErrorResponseObjectResourceAttributesOriginalPayload"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        code = self.code

        title = self.title

        detail = self.detail

        source = self.source.to_dict()

        original_payload: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.original_payload, Unset):
            original_payload = self.original_payload.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "title": title,
                "detail": detail,
                "source": source,
            }
        )
        if original_payload is not UNSET:
            field_dict["original_payload"] = original_payload

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.error_source import ErrorSource
        from ..models.import_error_response_object_resource_attributes_original_payload import (
            ImportErrorResponseObjectResourceAttributesOriginalPayload,
        )

        d = src_dict.copy()
        code = d.pop("code")

        title = d.pop("title")

        detail = d.pop("detail")

        source = ErrorSource.from_dict(d.pop("source"))

        _original_payload = d.pop("original_payload", UNSET)
        original_payload: Union[Unset, ImportErrorResponseObjectResourceAttributesOriginalPayload]
        if isinstance(_original_payload, Unset):
            original_payload = UNSET
        else:
            original_payload = ImportErrorResponseObjectResourceAttributesOriginalPayload.from_dict(_original_payload)

        import_error_response_object_resource_attributes = cls(
            code=code,
            title=title,
            detail=detail,
            source=source,
            original_payload=original_payload,
        )

        import_error_response_object_resource_attributes.additional_properties = d
        return import_error_response_object_resource_attributes

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
