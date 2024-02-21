from enum import Enum


class GetEventsFieldsprofileItem(str, Enum):
    CREATED = "created"
    EMAIL = "email"
    EXTERNAL_ID = "external_id"
    FIRST_NAME = "first_name"
    IMAGE = "image"
    LAST_EVENT_DATE = "last_event_date"
    LAST_NAME = "last_name"
    LOCATION = "location"
    LOCATION_ADDRESS1 = "location.address1"
    LOCATION_ADDRESS2 = "location.address2"
    LOCATION_CITY = "location.city"
    LOCATION_COUNTRY = "location.country"
    LOCATION_IP = "location.ip"
    LOCATION_LATITUDE = "location.latitude"
    LOCATION_LONGITUDE = "location.longitude"
    LOCATION_REGION = "location.region"
    LOCATION_TIMEZONE = "location.timezone"
    LOCATION_ZIP = "location.zip"
    ORGANIZATION = "organization"
    PHONE_NUMBER = "phone_number"
    PROPERTIES = "properties"
    TITLE = "title"
    UPDATED = "updated"

    def __str__(self) -> str:
        return str(self.value)
