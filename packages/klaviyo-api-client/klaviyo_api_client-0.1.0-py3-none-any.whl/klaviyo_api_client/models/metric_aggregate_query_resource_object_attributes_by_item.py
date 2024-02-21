from enum import Enum


class MetricAggregateQueryResourceObjectAttributesByItem(str, Enum):
    BOUNCE_TYPE = "Bounce Type"
    CAMPAIGN_NAME = "Campaign Name"
    CLIENT_CANONICAL = "Client Canonical"
    CLIENT_NAME = "Client Name"
    CLIENT_TYPE = "Client Type"
    EMAIL_DOMAIN = "Email Domain"
    FAILURE_SOURCE = "Failure Source"
    FAILURE_TYPE = "Failure Type"
    FORM_ID = "form_id"
    FROM_NUMBER = "From Number"
    FROM_PHONE_REGION = "From Phone Region"
    LIST = "List"
    MESSAGE_NAME = "Message Name"
    MESSAGE_TYPE = "Message Type"
    METHOD = "Method"
    SUBJECT = "Subject"
    TO_NUMBER = "To Number"
    TO_PHONE_REGION = "To Phone Region"
    URL = "URL"
    VALUE_0 = "$attributed_channel"
    VALUE_1 = "$attributed_flow"
    VALUE_10 = "$variation_send_cohort"
    VALUE_2 = "$attributed_message"
    VALUE_3 = "$attributed_variation"
    VALUE_4 = "$campaign_channel"
    VALUE_5 = "$flow"
    VALUE_6 = "$flow_channel"
    VALUE_7 = "$message"
    VALUE_8 = "$message_send_cohort"
    VALUE_9 = "$variation"

    def __str__(self) -> str:
        return str(self.value)
