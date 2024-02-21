from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_list_additional_fieldslist_item import GetListAdditionalFieldslistItem
from ...models.get_list_fieldslist_item import GetListFieldslistItem
from ...models.get_list_fieldstag_item import GetListFieldstagItem
from ...models.get_list_include_item import GetListIncludeItem
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    *,
    additional_fieldslist: Union[Unset, List[GetListAdditionalFieldslistItem]] = UNSET,
    fieldslist: Union[Unset, List[GetListFieldslistItem]] = UNSET,
    fieldstag: Union[Unset, List[GetListFieldstagItem]] = UNSET,
    include: Union[Unset, List[GetListIncludeItem]] = UNSET,
    revision: str = "2024-02-15",
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    headers["revision"] = revision

    params: Dict[str, Any] = {}

    json_additional_fieldslist: Union[Unset, List[str]] = UNSET
    if not isinstance(additional_fieldslist, Unset):
        json_additional_fieldslist = []
        for additional_fieldslist_item_data in additional_fieldslist:
            additional_fieldslist_item = additional_fieldslist_item_data.value
            json_additional_fieldslist.append(additional_fieldslist_item)

    params["additional-fields[list]"] = json_additional_fieldslist

    json_fieldslist: Union[Unset, List[str]] = UNSET
    if not isinstance(fieldslist, Unset):
        json_fieldslist = []
        for fieldslist_item_data in fieldslist:
            fieldslist_item = fieldslist_item_data.value
            json_fieldslist.append(fieldslist_item)

    params["fields[list]"] = json_fieldslist

    json_fieldstag: Union[Unset, List[str]] = UNSET
    if not isinstance(fieldstag, Unset):
        json_fieldstag = []
        for fieldstag_item_data in fieldstag:
            fieldstag_item = fieldstag_item_data.value
            json_fieldstag.append(fieldstag_item)

    params["fields[tag]"] = json_fieldstag

    json_include: Union[Unset, List[str]] = UNSET
    if not isinstance(include, Unset):
        json_include = []
        for include_item_data in include:
            include_item = include_item_data.value
            json_include.append(include_item)

    params["include"] = json_include

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/api/lists/{id}/",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if response.status_code == HTTPStatus.BAD_REQUEST:
        return None
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        return None
    if response.status_code == HTTPStatus.PAYMENT_REQUIRED:
        return None
    if response.status_code == HTTPStatus.FORBIDDEN:
        return None
    if response.status_code == HTTPStatus.NOT_FOUND:
        return None
    if response.status_code == HTTPStatus.METHOD_NOT_ALLOWED:
        return None
    if response.status_code == HTTPStatus.NOT_ACCEPTABLE:
        return None
    if response.status_code == HTTPStatus.PROXY_AUTHENTICATION_REQUIRED:
        return None
    if response.status_code == HTTPStatus.REQUEST_TIMEOUT:
        return None
    if response.status_code == HTTPStatus.CONFLICT:
        return None
    if response.status_code == HTTPStatus.GONE:
        return None
    if response.status_code == HTTPStatus.LENGTH_REQUIRED:
        return None
    if response.status_code == HTTPStatus.PRECONDITION_FAILED:
        return None
    if response.status_code == HTTPStatus.REQUEST_ENTITY_TOO_LARGE:
        return None
    if response.status_code == HTTPStatus.REQUEST_URI_TOO_LONG:
        return None
    if response.status_code == HTTPStatus.UNSUPPORTED_MEDIA_TYPE:
        return None
    if response.status_code == HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE:
        return None
    if response.status_code == HTTPStatus.EXPECTATION_FAILED:
        return None
    if response.status_code == HTTPStatus.IM_A_TEAPOT:
        return None
    if response.status_code == HTTPStatus.MISDIRECTED_REQUEST:
        return None
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        return None
    if response.status_code == HTTPStatus.LOCKED:
        return None
    if response.status_code == HTTPStatus.FAILED_DEPENDENCY:
        return None
    if response.status_code == HTTPStatus.TOO_EARLY:
        return None
    if response.status_code == HTTPStatus.UPGRADE_REQUIRED:
        return None
    if response.status_code == HTTPStatus.PRECONDITION_REQUIRED:
        return None
    if response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
        return None
    if response.status_code == HTTPStatus.REQUEST_HEADER_FIELDS_TOO_LARGE:
        return None
    if response.status_code == HTTPStatus.UNAVAILABLE_FOR_LEGAL_REASONS:
        return None
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        return None
    if response.status_code == HTTPStatus.NOT_IMPLEMENTED:
        return None
    if response.status_code == HTTPStatus.BAD_GATEWAY:
        return None
    if response.status_code == HTTPStatus.SERVICE_UNAVAILABLE:
        return None
    if response.status_code == HTTPStatus.GATEWAY_TIMEOUT:
        return None
    if response.status_code == HTTPStatus.HTTP_VERSION_NOT_SUPPORTED:
        return None
    if response.status_code == HTTPStatus.VARIANT_ALSO_NEGOTIATES:
        return None
    if response.status_code == HTTPStatus.INSUFFICIENT_STORAGE:
        return None
    if response.status_code == HTTPStatus.LOOP_DETECTED:
        return None
    if response.status_code == HTTPStatus.NOT_EXTENDED:
        return None
    if response.status_code == HTTPStatus.NETWORK_AUTHENTICATION_REQUIRED:
        return None
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    additional_fieldslist: Union[Unset, List[GetListAdditionalFieldslistItem]] = UNSET,
    fieldslist: Union[Unset, List[GetListFieldslistItem]] = UNSET,
    fieldstag: Union[Unset, List[GetListFieldstagItem]] = UNSET,
    include: Union[Unset, List[GetListIncludeItem]] = UNSET,
    revision: str = "2024-02-15",
) -> Response[Any]:
    """Get List

     Get a list with the given list ID.<br><br>*Rate limits*:<br>Burst: `75/s`<br>Steady:
    `700/m`<br><br>Rate limits when using the `additional-fields[list]=profile_count` parameter in your
    API request:<br>Burst: `1/s`<br>Steady: `15/m`<br><br>To learn more about how the `additional-
    fields` parameter impacts rate limits, check out our [Rate limits, status codes, and
    errors](https://developers.klaviyo.com/en/v2024-02-15/docs/rate_limits_and_error_handling) guide.

    **Scopes:**
    `lists:read`

    Args:
        id (str): Primary key that uniquely identifies this list. Generated by Klaviyo. Example:
            Y6nRLr.
        additional_fieldslist (Union[Unset, List[GetListAdditionalFieldslistItem]]):
        fieldslist (Union[Unset, List[GetListFieldslistItem]]):
        fieldstag (Union[Unset, List[GetListFieldstagItem]]):
        include (Union[Unset, List[GetListIncludeItem]]):
        revision (str):  Default: '2024-02-15'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        id=id,
        additional_fieldslist=additional_fieldslist,
        fieldslist=fieldslist,
        fieldstag=fieldstag,
        include=include,
        revision=revision,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    additional_fieldslist: Union[Unset, List[GetListAdditionalFieldslistItem]] = UNSET,
    fieldslist: Union[Unset, List[GetListFieldslistItem]] = UNSET,
    fieldstag: Union[Unset, List[GetListFieldstagItem]] = UNSET,
    include: Union[Unset, List[GetListIncludeItem]] = UNSET,
    revision: str = "2024-02-15",
) -> Response[Any]:
    """Get List

     Get a list with the given list ID.<br><br>*Rate limits*:<br>Burst: `75/s`<br>Steady:
    `700/m`<br><br>Rate limits when using the `additional-fields[list]=profile_count` parameter in your
    API request:<br>Burst: `1/s`<br>Steady: `15/m`<br><br>To learn more about how the `additional-
    fields` parameter impacts rate limits, check out our [Rate limits, status codes, and
    errors](https://developers.klaviyo.com/en/v2024-02-15/docs/rate_limits_and_error_handling) guide.

    **Scopes:**
    `lists:read`

    Args:
        id (str): Primary key that uniquely identifies this list. Generated by Klaviyo. Example:
            Y6nRLr.
        additional_fieldslist (Union[Unset, List[GetListAdditionalFieldslistItem]]):
        fieldslist (Union[Unset, List[GetListFieldslistItem]]):
        fieldstag (Union[Unset, List[GetListFieldstagItem]]):
        include (Union[Unset, List[GetListIncludeItem]]):
        revision (str):  Default: '2024-02-15'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        id=id,
        additional_fieldslist=additional_fieldslist,
        fieldslist=fieldslist,
        fieldstag=fieldstag,
        include=include,
        revision=revision,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
