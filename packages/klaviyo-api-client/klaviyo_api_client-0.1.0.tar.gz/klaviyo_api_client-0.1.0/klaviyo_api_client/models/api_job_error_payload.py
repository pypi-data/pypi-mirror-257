from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.error_source import ErrorSource


T = TypeVar("T", bound="APIJobErrorPayload")


@_attrs_define
class APIJobErrorPayload:
    """
    Attributes:
        id (str): Unique identifier for the error. Example: e4eebb08-b055-4a6f-bb13-c8cb69c9eb94.
        code (str): A code for classifying the error type. Example: invalid.
        title (str): A high-level message about the error. Example: Invalid input.
        detail (str): Specific details about the error. Example: The payload provided in the request is invalid..
        source (ErrorSource):
    """

    id: str
    code: str
    title: str
    detail: str
    source: "ErrorSource"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        code = self.code

        title = self.title

        detail = self.detail

        source = self.source.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "code": code,
                "title": title,
                "detail": detail,
                "source": source,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.error_source import ErrorSource

        d = src_dict.copy()
        id = d.pop("id")

        code = d.pop("code")

        title = d.pop("title")

        detail = d.pop("detail")

        source = ErrorSource.from_dict(d.pop("source"))

        api_job_error_payload = cls(
            id=id,
            code=code,
            title=title,
            detail=detail,
            source=source,
        )

        api_job_error_payload.additional_properties = d
        return api_job_error_payload

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
