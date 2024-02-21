from enum import Enum


class PushTokenCreateQueryResourceObjectAttributesVendor(str, Enum):
    APNS = "apns"
    FCM = "fcm"

    def __str__(self) -> str:
        return str(self.value)
