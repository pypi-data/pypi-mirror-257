from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_bulk_profile_import_job_profiles_additional_fieldsprofile_item import (
    GetBulkProfileImportJobProfilesAdditionalFieldsprofileItem,
)
from ...models.get_bulk_profile_import_job_profiles_fieldsprofile_item import (
    GetBulkProfileImportJobProfilesFieldsprofileItem,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    *,
    additional_fieldsprofile: Union[Unset, List[GetBulkProfileImportJobProfilesAdditionalFieldsprofileItem]] = UNSET,
    fieldsprofile: Union[Unset, List[GetBulkProfileImportJobProfilesFieldsprofileItem]] = UNSET,
    pagecursor: Union[Unset, str] = UNSET,
    pagesize: Union[Unset, int] = 20,
    revision: str = "2024-02-15",
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    headers["revision"] = revision

    params: Dict[str, Any] = {}

    json_additional_fieldsprofile: Union[Unset, List[str]] = UNSET
    if not isinstance(additional_fieldsprofile, Unset):
        json_additional_fieldsprofile = []
        for additional_fieldsprofile_item_data in additional_fieldsprofile:
            additional_fieldsprofile_item = additional_fieldsprofile_item_data.value
            json_additional_fieldsprofile.append(additional_fieldsprofile_item)

    params["additional-fields[profile]"] = json_additional_fieldsprofile

    json_fieldsprofile: Union[Unset, List[str]] = UNSET
    if not isinstance(fieldsprofile, Unset):
        json_fieldsprofile = []
        for fieldsprofile_item_data in fieldsprofile:
            fieldsprofile_item = fieldsprofile_item_data.value
            json_fieldsprofile.append(fieldsprofile_item)

    params["fields[profile]"] = json_fieldsprofile

    params["page[cursor]"] = pagecursor

    params["page[size]"] = pagesize

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/api/profile-bulk-import-jobs/{id}/profiles/",
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
    additional_fieldsprofile: Union[Unset, List[GetBulkProfileImportJobProfilesAdditionalFieldsprofileItem]] = UNSET,
    fieldsprofile: Union[Unset, List[GetBulkProfileImportJobProfilesFieldsprofileItem]] = UNSET,
    pagecursor: Union[Unset, str] = UNSET,
    pagesize: Union[Unset, int] = 20,
    revision: str = "2024-02-15",
) -> Response[Any]:
    """Get Bulk Profile Import Job Profiles

     Get profiles for the bulk profile import job with the given ID.<br><br>*Rate limits*:<br>Burst:
    `10/s`<br>Steady: `150/m`

    **Scopes:**
    `profiles:read`

    Args:
        id (str):
        additional_fieldsprofile (Union[Unset,
            List[GetBulkProfileImportJobProfilesAdditionalFieldsprofileItem]]):
        fieldsprofile (Union[Unset, List[GetBulkProfileImportJobProfilesFieldsprofileItem]]):
        pagecursor (Union[Unset, str]):
        pagesize (Union[Unset, int]):  Default: 20.
        revision (str):  Default: '2024-02-15'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        id=id,
        additional_fieldsprofile=additional_fieldsprofile,
        fieldsprofile=fieldsprofile,
        pagecursor=pagecursor,
        pagesize=pagesize,
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
    additional_fieldsprofile: Union[Unset, List[GetBulkProfileImportJobProfilesAdditionalFieldsprofileItem]] = UNSET,
    fieldsprofile: Union[Unset, List[GetBulkProfileImportJobProfilesFieldsprofileItem]] = UNSET,
    pagecursor: Union[Unset, str] = UNSET,
    pagesize: Union[Unset, int] = 20,
    revision: str = "2024-02-15",
) -> Response[Any]:
    """Get Bulk Profile Import Job Profiles

     Get profiles for the bulk profile import job with the given ID.<br><br>*Rate limits*:<br>Burst:
    `10/s`<br>Steady: `150/m`

    **Scopes:**
    `profiles:read`

    Args:
        id (str):
        additional_fieldsprofile (Union[Unset,
            List[GetBulkProfileImportJobProfilesAdditionalFieldsprofileItem]]):
        fieldsprofile (Union[Unset, List[GetBulkProfileImportJobProfilesFieldsprofileItem]]):
        pagecursor (Union[Unset, str]):
        pagesize (Union[Unset, int]):  Default: 20.
        revision (str):  Default: '2024-02-15'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        id=id,
        additional_fieldsprofile=additional_fieldsprofile,
        fieldsprofile=fieldsprofile,
        pagecursor=pagecursor,
        pagesize=pagesize,
        revision=revision,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
