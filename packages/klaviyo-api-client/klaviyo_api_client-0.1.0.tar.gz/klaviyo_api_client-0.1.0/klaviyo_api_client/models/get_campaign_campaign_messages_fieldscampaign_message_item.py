from enum import Enum


class GetCampaignCampaignMessagesFieldscampaignMessageItem(str, Enum):
    CHANNEL = "channel"
    CONTENT = "content"
    CREATED_AT = "created_at"
    LABEL = "label"
    RENDER_OPTIONS = "render_options"
    RENDER_OPTIONS_ADD_INFO_LINK = "render_options.add_info_link"
    RENDER_OPTIONS_ADD_OPT_OUT_LANGUAGE = "render_options.add_opt_out_language"
    RENDER_OPTIONS_ADD_ORG_PREFIX = "render_options.add_org_prefix"
    RENDER_OPTIONS_SHORTEN_LINKS = "render_options.shorten_links"
    SEND_TIMES = "send_times"
    UPDATED_AT = "updated_at"

    def __str__(self) -> str:
        return str(self.value)
