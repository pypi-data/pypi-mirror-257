from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.device_metadata_environment import DeviceMetadataEnvironment
from ..models.device_metadata_klaviyo_sdk import DeviceMetadataKlaviyoSdk
from ..models.device_metadata_os_name import DeviceMetadataOsName
from ..types import UNSET, Unset

T = TypeVar("T", bound="DeviceMetadata")


@_attrs_define
class DeviceMetadata:
    """
    Attributes:
        device_id (Union[Unset, str]): Relatively stable ID for the device. Will update on app uninstall and reinstall
            Example: 1234567890.
        klaviyo_sdk (Union[Unset, DeviceMetadataKlaviyoSdk]): The name of the SDK used to create the push token.
            Example: swift.
        sdk_version (Union[Unset, str]): The version of the SDK used to create the push token Example: 1.0.0.
        device_model (Union[Unset, str]): The model of the device Example: iPhone12,1.
        os_name (Union[Unset, DeviceMetadataOsName]): The name of the operating system on the device. Example: ios.
        os_version (Union[Unset, str]): The version of the operating system on the device Example: 14.0.
        manufacturer (Union[Unset, str]): The manufacturer of the device Example: Apple.
        app_name (Union[Unset, str]): The name of the app that created the push token Example: Klaviyo.
        app_version (Union[Unset, str]): The version of the app that created the push token Example: 1.0.0.
        app_build (Union[Unset, str]): The build of the app that created the push token Example: 1.
        app_id (Union[Unset, str]): The ID of the app that created the push token Example: com.klaviyo.app.
        environment (Union[Unset, DeviceMetadataEnvironment]): The environment in which the push token was created
            Example: release.
    """

    device_id: Union[Unset, str] = UNSET
    klaviyo_sdk: Union[Unset, DeviceMetadataKlaviyoSdk] = UNSET
    sdk_version: Union[Unset, str] = UNSET
    device_model: Union[Unset, str] = UNSET
    os_name: Union[Unset, DeviceMetadataOsName] = UNSET
    os_version: Union[Unset, str] = UNSET
    manufacturer: Union[Unset, str] = UNSET
    app_name: Union[Unset, str] = UNSET
    app_version: Union[Unset, str] = UNSET
    app_build: Union[Unset, str] = UNSET
    app_id: Union[Unset, str] = UNSET
    environment: Union[Unset, DeviceMetadataEnvironment] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        device_id = self.device_id

        klaviyo_sdk: Union[Unset, str] = UNSET
        if not isinstance(self.klaviyo_sdk, Unset):
            klaviyo_sdk = self.klaviyo_sdk.value

        sdk_version = self.sdk_version

        device_model = self.device_model

        os_name: Union[Unset, str] = UNSET
        if not isinstance(self.os_name, Unset):
            os_name = self.os_name.value

        os_version = self.os_version

        manufacturer = self.manufacturer

        app_name = self.app_name

        app_version = self.app_version

        app_build = self.app_build

        app_id = self.app_id

        environment: Union[Unset, str] = UNSET
        if not isinstance(self.environment, Unset):
            environment = self.environment.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if device_id is not UNSET:
            field_dict["device_id"] = device_id
        if klaviyo_sdk is not UNSET:
            field_dict["klaviyo_sdk"] = klaviyo_sdk
        if sdk_version is not UNSET:
            field_dict["sdk_version"] = sdk_version
        if device_model is not UNSET:
            field_dict["device_model"] = device_model
        if os_name is not UNSET:
            field_dict["os_name"] = os_name
        if os_version is not UNSET:
            field_dict["os_version"] = os_version
        if manufacturer is not UNSET:
            field_dict["manufacturer"] = manufacturer
        if app_name is not UNSET:
            field_dict["app_name"] = app_name
        if app_version is not UNSET:
            field_dict["app_version"] = app_version
        if app_build is not UNSET:
            field_dict["app_build"] = app_build
        if app_id is not UNSET:
            field_dict["app_id"] = app_id
        if environment is not UNSET:
            field_dict["environment"] = environment

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        device_id = d.pop("device_id", UNSET)

        _klaviyo_sdk = d.pop("klaviyo_sdk", UNSET)
        klaviyo_sdk: Union[Unset, DeviceMetadataKlaviyoSdk]
        if isinstance(_klaviyo_sdk, Unset):
            klaviyo_sdk = UNSET
        else:
            klaviyo_sdk = DeviceMetadataKlaviyoSdk(_klaviyo_sdk)

        sdk_version = d.pop("sdk_version", UNSET)

        device_model = d.pop("device_model", UNSET)

        _os_name = d.pop("os_name", UNSET)
        os_name: Union[Unset, DeviceMetadataOsName]
        if isinstance(_os_name, Unset):
            os_name = UNSET
        else:
            os_name = DeviceMetadataOsName(_os_name)

        os_version = d.pop("os_version", UNSET)

        manufacturer = d.pop("manufacturer", UNSET)

        app_name = d.pop("app_name", UNSET)

        app_version = d.pop("app_version", UNSET)

        app_build = d.pop("app_build", UNSET)

        app_id = d.pop("app_id", UNSET)

        _environment = d.pop("environment", UNSET)
        environment: Union[Unset, DeviceMetadataEnvironment]
        if isinstance(_environment, Unset):
            environment = UNSET
        else:
            environment = DeviceMetadataEnvironment(_environment)

        device_metadata = cls(
            device_id=device_id,
            klaviyo_sdk=klaviyo_sdk,
            sdk_version=sdk_version,
            device_model=device_model,
            os_name=os_name,
            os_version=os_version,
            manufacturer=manufacturer,
            app_name=app_name,
            app_version=app_version,
            app_build=app_build,
            app_id=app_id,
            environment=environment,
        )

        device_metadata.additional_properties = d
        return device_metadata

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
