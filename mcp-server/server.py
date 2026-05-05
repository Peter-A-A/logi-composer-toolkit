#!/usr/bin/env python3
"""
Logi Composer REST API — MCP Server
Auto-generated from OpenAPI 3.1.0 spec (fetched 2026-05-05)
Exposes 132 endpoints + 1 generic passthrough tool.
"""

import os
import json
import logging
import httpx
from pathlib import Path
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
load_dotenv()  # loads .env file from cwd or parent dirs

COMPOSER_HOST = os.getenv("COMPOSER_HOST", "https://uat.logi-symphony.com")
COMPOSER_BASE_PATH = os.getenv("COMPOSER_BASE_PATH", "/discovery")  # or /composer
BASE_URL = f"{COMPOSER_HOST.rstrip('/')}{COMPOSER_BASE_PATH}"
COMPOSER_USERNAME = os.getenv("COMPOSER_USERNAME", "")
COMPOSER_PASSWORD = os.getenv("COMPOSER_PASSWORD", "")
VERIFY_SSL = os.getenv("COMPOSER_VERIFY_SSL", "true").lower() == "true"
TIMEOUT = int(os.getenv("COMPOSER_TIMEOUT", "30"))

if not COMPOSER_USERNAME or not COMPOSER_PASSWORD:
    logging.warning(
        "COMPOSER_USERNAME and/or COMPOSER_PASSWORD are not set. API calls will fail. "
        "Set them in your .env file or as environment variables."
    )

# ---------------------------------------------------------------------------
# MCP Server
# ---------------------------------------------------------------------------
mcp = FastMCP(
    "logi-composer",
    instructions="Logi Composer REST API — 132 endpoints for managing connections, sources, dashboards, visuals, users, permissions, and more.",
)


import base64


def _headers(has_body: bool = False):
    """Build request headers. Matches the pattern from the Composer API docs:
    only Authorization on GETs; Authorization + Content-Type on POST/PUT/PATCH."""
    credentials = base64.b64encode(
        f"{COMPOSER_USERNAME}:{COMPOSER_PASSWORD}".encode()
    ).decode()
    headers = {
        "Authorization": f"Basic {credentials}",
    }
    if has_body:
        headers["Content-Type"] = "application/vnd.composer.v3+json"
    return headers


def _build_url(path_template: str, path_params: dict) -> str:
    """Substitute {param} placeholders in the path."""
    url = path_template
    for key, value in path_params.items():
        url = url.replace("{" + key + "}", str(value))
    return f"{BASE_URL}{url}"


async def _call_api(method: str, path_template: str, path_params: dict = None,
                    query_params: dict = None, body: dict = None) -> str:
    """Execute an HTTP request against the Composer API."""
    path_params = path_params or {}
    query_params = {k: v for k, v in (query_params or {}).items() if v is not None}

    url = _build_url(path_template, path_params)

    has_body = body is not None and method.upper() in ("POST", "PUT", "PATCH")

    async with httpx.AsyncClient(verify=VERIFY_SSL, timeout=TIMEOUT) as client:
        response = await client.request(
            method=method.upper(),
            url=url,
            headers=_headers(has_body=has_body),
            params=query_params or None,
            json=body if body else None,
        )

    # Return structured result
    try:
        data = response.json()
        result = {"status_code": response.status_code, "data": data}
    except Exception:
        result = {"status_code": response.status_code, "text": response.text[:5000]}

    return json.dumps(result, indent=2, default=str)


# ---------------------------------------------------------------------------
# Generic passthrough tool (covers any endpoint, including those not in spec)
# ---------------------------------------------------------------------------
@mcp.tool()
async def composer_api_request(
    method: str,
    path: str,
    query_params: dict | None = None,
    body: dict | None = None,
) -> str:
    """
    Generic Logi Composer API request. Use this for any endpoint not covered
    by the specific tools, or when you need full control.

    Args:
        method: HTTP method (GET, POST, PUT, DELETE, PATCH)
        path: API path starting with /api/ (e.g. /api/sources)
        query_params: Optional query string parameters as key-value dict
        body: Optional JSON request body as dict
    """
    return await _call_api(method, path, {}, query_params, body)


# ---------------------------------------------------------------------------
# Auto-generated endpoint tools
# ---------------------------------------------------------------------------

@mcp.tool()
async def get_visuals(
    id: str,
    suppressWarnings: str | None = None,
    warningTags: str | None = None,
    body: dict | None = None,
) -> str:
    """
    Retrieve a visual (requires READ permission to the visual)
    
    Returns a visual specified by id
    
    API: GET /api/visuals/{id}
    Tag: visuals
    
    Args:
        id: Path parameter
        suppressWarnings: Query parameter (optional)
        warningTags: Query parameter (optional)
        body: JSON request body (optional)
    """
    return await _call_api(
        "get",
        "/api/visuals/{id}",
        {"id": id},
        {"suppressWarnings": suppressWarnings, "warningTags": warningTags},
        body,
    )


@mcp.tool()
async def update_visuals(
    id: str,
    suppressWarnings: str | None = None,
    warningTags: str | None = None,
    body: dict | None = None,
) -> str:
    """
    Updates a visual (requires WRITE permission to the visual) or creates a new visual with custom id (requires the ROLE_CREATE_VISUALS privilege)
    
    Defines a visual identifier
    
    API: PUT /api/visuals/{id}
    Tag: visuals
    
    Args:
        id: Path parameter
        suppressWarnings: Query parameter (optional)
        warningTags: Query parameter (optional)
        body: JSON request body (optional)
    """
    return await _call_api(
        "put",
        "/api/visuals/{id}",
        {"id": id},
        {"suppressWarnings": suppressWarnings, "warningTags": warningTags},
        body,
    )


@mcp.tool()
async def delete_visuals(
    id: str,
) -> str:
    """
    Deletes a visual (requires DELETE permission to the visual)
    
    Defines a visual identifier
    
    API: DELETE /api/visuals/{id}
    Tag: visuals
    
    Args:
        id: Path parameter
    """
    return await _call_api(
        "delete",
        "/api/visuals/{id}",
        {"id": id},
        {},
        None,
    )


@mcp.tool()
async def update_visual_acl_bulk(
    id: str,
    body: dict | None = None,
) -> str:
    """
    Assign permissions on the visual to a list of Security Identities (groups, users, account)
    
    Visual identifier
    
    API: PUT /api/visuals/{id}/acls/bulk
    Tag: permissions
    
    Args:
        id: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "put",
        "/api/visuals/{id}/acls/bulk",
        {"id": id},
        {},
        body,
    )


@mcp.tool()
async def patch_visual_acl_bulk(
    id: str,
    body: dict | None = None,
) -> str:
    """
    Grant/revoke permissions on the visual to/from a list of Security Identities (groups, users, account)
    
    Visual identifier
    
    API: PATCH /api/visuals/{id}/acls/bulk
    Tag: permissions
    
    Args:
        id: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "patch",
        "/api/visuals/{id}/acls/bulk",
        {"id": id},
        {},
        body,
    )


@mcp.tool()
async def get_visual_types(
    id: str,
    componentBody: str | None = None,
    body: dict | None = None,
) -> str:
    """
    Get Visual Type by id
    
    OK
    
    API: GET /api/visual-types/{id}
    Tag: visual-types
    
    Args:
        id: Path parameter
        componentBody: Query parameter (optional)
        body: JSON request body (optional)
    """
    return await _call_api(
        "get",
        "/api/visual-types/{id}",
        {"id": id},
        {"componentBody": componentBody},
        body,
    )


@mcp.tool()
async def update_visual_types(
    id: str,
    body: dict | None = None,
) -> str:
    """
    Update Visual Type
    
    No Content
    
    API: PUT /api/visual-types/{id}
    Tag: visual-types
    
    Args:
        id: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "put",
        "/api/visual-types/{id}",
        {"id": id},
        {},
        body,
    )


@mcp.tool()
async def delete_visual_types(
    id: str,
) -> str:
    """
    Delete Visual Type
    
    No Content
    
    API: DELETE /api/visual-types/{id}
    Tag: visual-types
    
    Args:
        id: Path parameter
    """
    return await _call_api(
        "delete",
        "/api/visual-types/{id}",
        {"id": id},
        {},
        None,
    )


@mcp.tool()
async def get_users(
    id: str,
    body: dict | None = None,
) -> str:
    """
    Load user
    
    OK
    
    API: GET /api/users/{id}
    Tag: users
    
    Args:
        id: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "get",
        "/api/users/{id}",
        {"id": id},
        {},
        body,
    )


@mcp.tool()
async def update_users(
    id: str,
    body: dict | None = None,
) -> str:
    """
    Update user
    
    Supervisor authority or role Administer Users is required to access this endpoint
    
    API: PUT /api/users/{id}
    Tag: users
    
    Args:
        id: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "put",
        "/api/users/{id}",
        {"id": id},
        {},
        body,
    )


@mcp.tool()
async def delete_users(
    id: str,
) -> str:
    """
    Delete user
    
    Supervisor authority or role Administer Users is required to access this endpoint
    
    API: DELETE /api/users/{id}
    Tag: users
    
    Args:
        id: Path parameter
    """
    return await _call_api(
        "delete",
        "/api/users/{id}",
        {"id": id},
        {},
        None,
    )


@mcp.tool()
async def get_user_permissions(
    sid: str,
    body: dict | None = None,
) -> str:
    """
    Get the conditions for user segregation in the account
    
    Successful operation
    
    API: GET /api/users/permissions/{sid}
    Tag: users segregation
    
    Args:
        sid: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "get",
        "/api/users/permissions/{sid}",
        {"sid": sid},
        {},
        body,
    )


@mcp.tool()
async def update_user_permissions(
    sid: str,
    body: dict | None = None,
) -> str:
    """
    Update the conditions for user segregation in the account
    
    The permissions on condition were updated
    
    API: PUT /api/users/permissions/{sid}
    Tag: users segregation
    
    Args:
        sid: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "put",
        "/api/users/permissions/{sid}",
        {"sid": sid},
        {},
        body,
    )


@mcp.tool()
async def delete_user_permissions(
    sid: str,
) -> str:
    """
    Delete the conditions for user segregation in the account
    
    The user must be logged in
    
    API: DELETE /api/users/permissions/{sid}
    Tag: users segregation
    
    Args:
        sid: Path parameter
    """
    return await _call_api(
        "delete",
        "/api/users/permissions/{sid}",
        {"sid": sid},
        {},
        None,
    )


@mcp.tool()
async def get_uploads(
    id: str,
    body: dict | None = None,
) -> str:
    """
    Returns an upload by id
    
    Requires READ permission to the upload
    
    API: GET /api/uploads/{id}
    Tag: uploads
    
    Args:
        id: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "get",
        "/api/uploads/{id}",
        {"id": id},
        {},
        body,
    )


@mcp.tool()
async def update_uploads(
    id: str,
    body: dict | None = None,
) -> str:
    """
    Updates uploads
    
    Requires MANAGE_CONNECTIONS or MANAGE_FILE_UPLOADS role
    
    API: PUT /api/uploads/{id}
    Tag: uploads
    
    Args:
        id: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "put",
        "/api/uploads/{id}",
        {"id": id},
        {},
        body,
    )


@mcp.tool()
async def delete_uploads(
    id: str,
) -> str:
    """
    Deletes an upload
    
    Requires MANAGE_CONNECTIONS or MANAGE_FILE_UPLOADS role
    
    API: DELETE /api/uploads/{id}
    Tag: uploads
    
    Args:
        id: Path parameter
    """
    return await _call_api(
        "delete",
        "/api/uploads/{id}",
        {"id": id},
        {},
        None,
    )


@mcp.tool()
async def create_upload_data(
    id: str,
    body: dict | None = None,
) -> str:
    """
    Appends data to the upload
    
    Requires MANAGE_CONNECTIONS or MANAGE_FILE_UPLOADS role
    
    API: POST /api/uploads/{id}/data
    Tag: uploads
    
    Args:
        id: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "post",
        "/api/uploads/{id}/data",
        {"id": id},
        {},
        body,
    )


@mcp.tool()
async def update_upload_data(
    id: str,
    body: dict | None = None,
) -> str:
    """
    Replaces upload data
    
    Requires MANAGE_CONNECTIONS or MANAGE_FILE_UPLOADS role
    
    API: PUT /api/uploads/{id}/data
    Tag: uploads
    
    Args:
        id: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "put",
        "/api/uploads/{id}/data",
        {"id": id},
        {},
        body,
    )


@mcp.tool()
async def delete_upload_data(
    id: str,
) -> str:
    """
    Deletes upload data
    
    Requires MANAGE_CONNECTIONS or MANAGE_FILE_UPLOADS role
    
    API: DELETE /api/uploads/{id}/data
    Tag: uploads
    
    Args:
        id: Path parameter
    """
    return await _call_api(
        "delete",
        "/api/uploads/{id}/data",
        {"id": id},
        {},
        None,
    )


@mcp.tool()
async def get_toggles(
    prefix: str,
    key: str,
    body: dict | None = None,
) -> str:
    """
    Get variable by prefix and key
    
    OK
    
    API: GET /api/toggles/{prefix}/{key}
    Tag: toggle
    
    Args:
        prefix: Path parameter
        key: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "get",
        "/api/toggles/{prefix}/{key}",
        {"prefix": prefix, "key": key},
        {},
        body,
    )


@mcp.tool()
async def update_toggles(
    prefix: str,
    key: str,
    body: dict | None = None,
) -> str:
    """
    Set variable by prefix and key
    
    Supervisor authority is required to access this endpoint
    
    API: PUT /api/toggles/{prefix}/{key}
    Tag: toggle
    
    Args:
        prefix: Path parameter
        key: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "put",
        "/api/toggles/{prefix}/{key}",
        {"prefix": prefix, "key": key},
        {},
        body,
    )


@mcp.tool()
async def delete_toggles(
    prefix: str,
    key: str,
) -> str:
    """
    Delete variable by prefix and key
    
    Supervisor authority is required to access this endpoint
    
    API: DELETE /api/toggles/{prefix}/{key}
    Tag: toggle
    
    Args:
        prefix: Path parameter
        key: Path parameter
    """
    return await _call_api(
        "delete",
        "/api/toggles/{prefix}/{key}",
        {"prefix": prefix, "key": key},
        {},
        None,
    )


@mcp.tool()
async def get_system_activity_type(
    activityType: str,
    body: dict | None = None,
) -> str:
    """
    Get the toggle status of a specific activity type
    
    Supervisor authority is required to access this endpoint
    
    API: GET /api/system/activity/type/{activityType}
    Tag: activity
    
    Args:
        activityType: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "get",
        "/api/system/activity/type/{activityType}",
        {"activityType": activityType},
        {},
        body,
    )


@mcp.tool()
async def update_system_activity_type(
    activityType: str,
    body: dict | None = None,
) -> str:
    """
    Update an activity type to toggle its logging
    
    Supervisor authority is required to access this endpoint
    
    API: PUT /api/system/activity/type/{activityType}
    Tag: activity
    
    Args:
        activityType: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "put",
        "/api/system/activity/type/{activityType}",
        {"activityType": activityType},
        {},
        body,
    )


@mcp.tool()
async def get_sources(
    sourceId: str,
    suppressWarnings: str | None = None,
    warningTags: str | None = None,
    body: dict | None = None,
) -> str:
    """
    Returns a data source by id
    
    Requires READ permission on the source
    
    API: GET /api/sources/{sourceId}
    Tag: sources
    
    Args:
        sourceId: Path parameter
        suppressWarnings: Query parameter (optional)
        warningTags: Query parameter (optional)
        body: JSON request body (optional)
    """
    return await _call_api(
        "get",
        "/api/sources/{sourceId}",
        {"sourceId": sourceId},
        {"suppressWarnings": suppressWarnings, "warningTags": warningTags},
        body,
    )


@mcp.tool()
async def update_sources(
    sourceId: str,
    suppressWarnings: str | None = None,
    warningTags: str | None = None,
    body: dict | None = None,
) -> str:
    """
    Updates or creates a source
    
    Requires WRITE permission on the source for updating and CREATE_SOURCES privilege for creation
    
    API: PUT /api/sources/{sourceId}
    Tag: sources
    
    Args:
        sourceId: Path parameter
        suppressWarnings: Query parameter (optional)
        warningTags: Query parameter (optional)
        body: JSON request body (optional)
    """
    return await _call_api(
        "put",
        "/api/sources/{sourceId}",
        {"sourceId": sourceId},
        {"suppressWarnings": suppressWarnings, "warningTags": warningTags},
        body,
    )


@mcp.tool()
async def delete_sources(
    sourceId: str,
) -> str:
    """
    Deletes a source
    
    Requires DELETE permission on the source
    
    API: DELETE /api/sources/{sourceId}
    Tag: sources
    
    Args:
        sourceId: Path parameter
    """
    return await _call_api(
        "delete",
        "/api/sources/{sourceId}",
        {"sourceId": sourceId},
        {},
        None,
    )


@mcp.tool()
async def get_source_visual_types(
    sourceId: str,
    maxResults: str | None = None,
    pageToken: str | None = None,
    includeDisabled: str | None = None,
    includeRestriction: str | None = None,
    body: dict | None = None,
) -> str:
    """
    Returns visual types for the data source
    
    Requires READ or DATA_ACCESS permission on the source
    
    API: GET /api/sources/{sourceId}/visual-types
    Tag: sources / visual-types
    
    Args:
        sourceId: Path parameter
        maxResults: Query parameter (optional)
        pageToken: Query parameter (optional)
        includeDisabled: Query parameter (optional)
        includeRestriction: Query parameter (optional)
        body: JSON request body (optional)
    """
    return await _call_api(
        "get",
        "/api/sources/{sourceId}/visual-types",
        {"sourceId": sourceId},
        {"maxResults": maxResults, "pageToken": pageToken, "includeDisabled": includeDisabled, "includeRestriction": includeRestriction},
        body,
    )


@mcp.tool()
async def update_source_visual_types(
    sourceId: str,
    body: dict | None = None,
) -> str:
    """
    Updates source visual types
    
    Requires WRITE permission on the source
    
    API: PUT /api/sources/{sourceId}/visual-types
    Tag: sources / visual-types
    
    Args:
        sourceId: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "put",
        "/api/sources/{sourceId}/visual-types",
        {"sourceId": sourceId},
        {},
        body,
    )


@mcp.tool()
async def get_source_unique_key(
    sourceId: str,
    body: dict | None = None,
) -> str:
    """
    Returns unique key for the data source
    
    Requires READ permission on the source
    
    API: GET /api/sources/{sourceId}/unique-key
    Tag: sources / unique-key
    
    Args:
        sourceId: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "get",
        "/api/sources/{sourceId}/unique-key",
        {"sourceId": sourceId},
        {},
        body,
    )


@mcp.tool()
async def update_source_unique_key(
    sourceId: str,
    body: dict | None = None,
) -> str:
    """
    Updates unique key for the data source
    
    Requires WRITE permission on the source
    
    API: PUT /api/sources/{sourceId}/unique-key
    Tag: sources / unique-key
    
    Args:
        sourceId: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "put",
        "/api/sources/{sourceId}/unique-key",
        {"sourceId": sourceId},
        {},
        body,
    )


@mcp.tool()
async def get_source_security(
    sourceId: str,
    body: dict | None = None,
) -> str:
    """
    (experimental) Returns source security settings
    
    OK
    
    API: GET /api/sources/{sourceId}/security
    Tag: sources / security
    
    Args:
        sourceId: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "get",
        "/api/sources/{sourceId}/security",
        {"sourceId": sourceId},
        {},
        body,
    )


@mcp.tool()
async def update_source_security(
    sourceId: str,
    body: dict | None = None,
) -> str:
    """
    (experimental) Updates source security settings
    
    OK
    
    API: PUT /api/sources/{sourceId}/security
    Tag: sources / security
    
    Args:
        sourceId: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "put",
        "/api/sources/{sourceId}/security",
        {"sourceId": sourceId},
        {},
        body,
    )


@mcp.tool()
async def update_source_security_filters(
    sourceId: str,
    id: str,
    body: dict | None = None,
) -> str:
    """
    Update forced filter, replacing it completely
    
    OK
    
    API: PUT /api/sources/{sourceId}/security/filters/{id}
    Tag: sources / security / row
    
    Args:
        sourceId: Path parameter
        id: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "put",
        "/api/sources/{sourceId}/security/filters/{id}",
        {"sourceId": sourceId, "id": id},
        {},
        body,
    )


@mcp.tool()
async def delete_source_security_filters(
    sourceId: str,
    id: str,
    body: dict | None = None,
) -> str:
    """
    Delete forced filter by id
    
    No Content
    
    API: DELETE /api/sources/{sourceId}/security/filters/{id}
    Tag: sources / security / row
    
    Args:
        sourceId: Path parameter
        id: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "delete",
        "/api/sources/{sourceId}/security/filters/{id}",
        {"sourceId": sourceId, "id": id},
        {},
        body,
    )


@mcp.tool()
async def patch_source_security_filters(
    sourceId: str,
    id: str,
    body: dict | None = None,
) -> str:
    """
    Update forced filter partially
    
    OK
    
    API: PATCH /api/sources/{sourceId}/security/filters/{id}
    Tag: sources / security / row
    
    Args:
        sourceId: Path parameter
        id: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "patch",
        "/api/sources/{sourceId}/security/filters/{id}",
        {"sourceId": sourceId, "id": id},
        {},
        body,
    )


@mcp.tool()
async def update_source_security_custom_metrics(
    sourceId: str,
    id: str,
    body: dict | None = None,
) -> str:
    """
    (experimental) Update custom metric security setting
    
    OK
    
    API: PUT /api/sources/{sourceId}/security/custom-metrics/{id}
    Tag: sources / security / custom metrics
    
    Args:
        sourceId: Path parameter
        id: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "put",
        "/api/sources/{sourceId}/security/custom-metrics/{id}",
        {"sourceId": sourceId, "id": id},
        {},
        body,
    )


@mcp.tool()
async def delete_source_security_custom_metrics(
    sourceId: str,
    id: str,
) -> str:
    """
    (experimental) Delete custom metric security setting
    
    No Content
    
    API: DELETE /api/sources/{sourceId}/security/custom-metrics/{id}
    Tag: sources / security / custom metrics
    
    Args:
        sourceId: Path parameter
        id: Path parameter
    """
    return await _call_api(
        "delete",
        "/api/sources/{sourceId}/security/custom-metrics/{id}",
        {"sourceId": sourceId, "id": id},
        {},
        None,
    )


@mcp.tool()
async def update_source_security_attributes(
    sourceId: str,
    id: str,
    body: dict | None = None,
) -> str:
    """
    Update SecurityAttributeSetting
    
    OK
    
    API: PUT /api/sources/{sourceId}/security/attributes/{id}
    Tag: sources / security / fields
    
    Args:
        sourceId: Path parameter
        id: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "put",
        "/api/sources/{sourceId}/security/attributes/{id}",
        {"sourceId": sourceId, "id": id},
        {},
        body,
    )


@mcp.tool()
async def delete_source_security_attributes(
    sourceId: str,
    id: str,
) -> str:
    """
    Delete SecurityAttributeSetting
    
    No Content
    
    API: DELETE /api/sources/{sourceId}/security/attributes/{id}
    Tag: sources / security / fields
    
    Args:
        sourceId: Path parameter
        id: Path parameter
    """
    return await _call_api(
        "delete",
        "/api/sources/{sourceId}/security/attributes/{id}",
        {"sourceId": sourceId, "id": id},
        {},
        None,
    )


@mcp.tool()
async def update_source_security_fields(
    sourceId: str,
    id: str,
    body: dict | None = None,
) -> str:
    """
    Update SecurityAttributeSetting
    
    OK
    
    API: PUT /api/sources/{sourceId}/security/fields/{id}
    Tag: sources / security / fields
    
    Args:
        sourceId: Path parameter
        id: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "put",
        "/api/sources/{sourceId}/security/fields/{id}",
        {"sourceId": sourceId, "id": id},
        {},
        body,
    )


@mcp.tool()
async def delete_source_security_fields(
    sourceId: str,
    id: str,
) -> str:
    """
    Delete SecurityAttributeSetting
    
    No Content
    
    API: DELETE /api/sources/{sourceId}/security/fields/{id}
    Tag: sources / security / fields
    
    Args:
        sourceId: Path parameter
        id: Path parameter
    """
    return await _call_api(
        "delete",
        "/api/sources/{sourceId}/security/fields/{id}",
        {"sourceId": sourceId, "id": id},
        {},
        None,
    )


@mcp.tool()
async def get_source_global_settings(
    sourceId: str,
    body: dict | None = None,
) -> str:
    """
    Returns global settings for the data source
    
    Requires READ or DATA_ACCESS permission on the source
    
    API: GET /api/sources/{sourceId}/global-settings
    Tag: sources / global-settings
    
    Args:
        sourceId: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "get",
        "/api/sources/{sourceId}/global-settings",
        {"sourceId": sourceId},
        {},
        body,
    )


@mcp.tool()
async def update_source_global_settings(
    sourceId: str,
    body: dict | None = None,
) -> str:
    """
    Updates global settings for the data source
    
    Requires WRITE permission on the source
    
    API: PUT /api/sources/{sourceId}/global-settings
    Tag: sources / global-settings
    
    Args:
        sourceId: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "put",
        "/api/sources/{sourceId}/global-settings",
        {"sourceId": sourceId},
        {},
        body,
    )


@mcp.tool()
async def get_source_fields(
    sourceId: str,
    maxResults: str | None = None,
    pageToken: str | None = None,
    suppressWarnings: str | None = None,
    warningTags: str | None = None,
    body: dict | None = None,
) -> str:
    """
    Returns a list of fields for the source
    
    Requires READ permission on the source
    
    API: GET /api/sources/{sourceId}/fields
    Tag: sources / fields
    
    Args:
        sourceId: Path parameter
        maxResults: Query parameter (optional)
        pageToken: Query parameter (optional)
        suppressWarnings: Query parameter (optional)
        warningTags: Query parameter (optional)
        body: JSON request body (optional)
    """
    return await _call_api(
        "get",
        "/api/sources/{sourceId}/fields",
        {"sourceId": sourceId},
        {"maxResults": maxResults, "pageToken": pageToken, "suppressWarnings": suppressWarnings, "warningTags": warningTags},
        body,
    )


@mcp.tool()
async def create_source_fields(
    sourceId: str,
    suppressWarnings: str | None = None,
    body: dict | None = None,
) -> str:
    """
    Creates a data source field
    
    Requires WRITE permission on the source or READ permission on the source and ROLE_EDIT_FORMULAS for derived field creation
    
    API: POST /api/sources/{sourceId}/fields
    Tag: sources / fields
    
    Args:
        sourceId: Path parameter
        suppressWarnings: Query parameter (optional)
        body: JSON request body (optional)
    """
    return await _call_api(
        "post",
        "/api/sources/{sourceId}/fields",
        {"sourceId": sourceId},
        {"suppressWarnings": suppressWarnings},
        body,
    )


@mcp.tool()
async def update_source_fields(
    sourceId: str,
    suppressWarnings: str | None = None,
    warningTags: str | None = None,
    body: dict | None = None,
) -> str:
    """
    Updates a data source fields (requires WRITE permission to the source)
    
    The response to this API endpoint may return a validation error with a list of problems. Each problem has a level (ERROR, WARNING). Passing suppressWarnings=true will suppress all warnings and the request will succeed if there are no errors
    
    API: PUT /api/sources/{sourceId}/fields
    Tag: sources / fields
    
    Args:
        sourceId: Path parameter
        suppressWarnings: Query parameter (optional)
        warningTags: Query parameter (optional)
        body: JSON request body (optional)
    """
    return await _call_api(
        "put",
        "/api/sources/{sourceId}/fields",
        {"sourceId": sourceId},
        {"suppressWarnings": suppressWarnings, "warningTags": warningTags},
        body,
    )


@mcp.tool()
async def get_source_fields_1(
    sourceId: str,
    fieldName: str,
    suppressWarnings: str | None = None,
    warningTags: str | None = None,
    body: dict | None = None,
) -> str:
    """
    Returns a data source field by name
    
    Requires READ permission on the source
    
    API: GET /api/sources/{sourceId}/fields/{fieldName}
    Tag: sources / fields
    
    Args:
        sourceId: Path parameter
        fieldName: Path parameter
        suppressWarnings: Query parameter (optional)
        warningTags: Query parameter (optional)
        body: JSON request body (optional)
    """
    return await _call_api(
        "get",
        "/api/sources/{sourceId}/fields/{fieldName}",
        {"sourceId": sourceId, "fieldName": fieldName},
        {"suppressWarnings": suppressWarnings, "warningTags": warningTags},
        body,
    )


@mcp.tool()
async def update_source_fields_1(
    sourceId: str,
    fieldName: str,
    suppressWarnings: str | None = None,
    warningTags: str | None = None,
    body: dict | None = None,
) -> str:
    """
    Updates or creates a data source field
    
    Requires WRITE permission on the source or READ permission on the source and ROLE_EDIT_FORMULAS for derived field editing
    
    API: PUT /api/sources/{sourceId}/fields/{fieldName}
    Tag: sources / fields
    
    Args:
        sourceId: Path parameter
        fieldName: Path parameter
        suppressWarnings: Query parameter (optional)
        warningTags: Query parameter (optional)
        body: JSON request body (optional)
    """
    return await _call_api(
        "put",
        "/api/sources/{sourceId}/fields/{fieldName}",
        {"sourceId": sourceId, "fieldName": fieldName},
        {"suppressWarnings": suppressWarnings, "warningTags": warningTags},
        body,
    )


@mcp.tool()
async def delete_source_fields(
    sourceId: str,
    fieldName: str,
    suppressWarnings: str | None = None,
    warningTags: str | None = None,
    body: dict | None = None,
) -> str:
    """
    Deletes a data source field by name
    
    Requires WRITE permission on the source
    
    API: DELETE /api/sources/{sourceId}/fields/{fieldName}
    Tag: sources / fields
    
    Args:
        sourceId: Path parameter
        fieldName: Path parameter
        suppressWarnings: Query parameter (optional)
        warningTags: Query parameter (optional)
        body: JSON request body (optional)
    """
    return await _call_api(
        "delete",
        "/api/sources/{sourceId}/fields/{fieldName}",
        {"sourceId": sourceId, "fieldName": fieldName},
        {"suppressWarnings": suppressWarnings, "warningTags": warningTags},
        body,
    )


@mcp.tool()
async def patch_source_fields(
    sourceId: str,
    fieldName: str,
    body: dict | None = None,
) -> str:
    """
    Updates data source field visibility
    
    Requires WRITE permission on the source or READ permission on the source and ROLE_EDIT_FORMULAS for derived field editing
    
    API: PATCH /api/sources/{sourceId}/fields/{fieldName}
    Tag: sources / fields
    
    Args:
        sourceId: Path parameter
        fieldName: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "patch",
        "/api/sources/{sourceId}/fields/{fieldName}",
        {"sourceId": sourceId, "fieldName": fieldName},
        {},
        body,
    )


@mcp.tool()
async def get_source_dictionaries(
    sourceId: str,
    body: dict | None = None,
) -> str:
    """
    Returns a list of source dictionaries
    
    OK
    
    API: GET /api/sources/{sourceId}/dictionaries
    Tag: sources / dictionaries
    
    Args:
        sourceId: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "get",
        "/api/sources/{sourceId}/dictionaries",
        {"sourceId": sourceId},
        {},
        body,
    )


@mcp.tool()
async def update_source_dictionaries(
    sourceId: str,
    body: dict | None = None,
) -> str:
    """
    Bulk create or update from file with replace all source dictionaries
    
    File must have specific structure:\n\n``` \n\nField Label,languageLocaleId1,languageLocaleId2 \n\nfieldLabel1,labelTranslate1,labelTranslate2\n\n ```
    
    API: PUT /api/sources/{sourceId}/dictionaries
    Tag: sources / dictionaries
    
    Args:
        sourceId: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "put",
        "/api/sources/{sourceId}/dictionaries",
        {"sourceId": sourceId},
        {},
        body,
    )


@mcp.tool()
async def delete_source_dictionaries(
    sourceId: str,
) -> str:
    """
    Delete all source dictionaries
    
    No Content
    
    API: DELETE /api/sources/{sourceId}/dictionaries
    Tag: sources / dictionaries
    
    Args:
        sourceId: Path parameter
    """
    return await _call_api(
        "delete",
        "/api/sources/{sourceId}/dictionaries",
        {"sourceId": sourceId},
        {},
        None,
    )


@mcp.tool()
async def get_source_dictionaries_1(
    sourceId: str,
    language: str,
    body: dict | None = None,
) -> str:
    """
    Read source dictionary by language
    
    OK
    
    API: GET /api/sources/{sourceId}/dictionaries/{language}
    Tag: sources / dictionaries
    
    Args:
        sourceId: Path parameter
        language: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "get",
        "/api/sources/{sourceId}/dictionaries/{language}",
        {"sourceId": sourceId, "language": language},
        {},
        body,
    )


@mcp.tool()
async def update_source_dictionaries_1(
    sourceId: str,
    language: str,
    body: dict | None = None,
) -> str:
    """
    Create or update source dictionary by language
    
    OK
    
    API: PUT /api/sources/{sourceId}/dictionaries/{language}
    Tag: sources / dictionaries
    
    Args:
        sourceId: Path parameter
        language: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "put",
        "/api/sources/{sourceId}/dictionaries/{language}",
        {"sourceId": sourceId, "language": language},
        {},
        body,
    )


@mcp.tool()
async def delete_source_dictionaries_1(
    sourceId: str,
    language: str,
) -> str:
    """
    Delete source dictionary by language
    
    No Content
    
    API: DELETE /api/sources/{sourceId}/dictionaries/{language}
    Tag: sources / dictionaries
    
    Args:
        sourceId: Path parameter
        language: Path parameter
    """
    return await _call_api(
        "delete",
        "/api/sources/{sourceId}/dictionaries/{language}",
        {"sourceId": sourceId, "language": language},
        {},
        None,
    )


@mcp.tool()
async def update_source_custom_metrics(
    sourceId: str,
    customMetricName: str,
    body: dict | None = None,
) -> str:
    """
    Updates existing custom metric or creates a new one if custom metric with {customMetricName} doesn't exist
    
    Requires WRITE permission on the source or READ permission on the source and ROLE_EDIT_FORMULAS
    
    API: PUT /api/sources/{sourceId}/custom-metrics/{customMetricName}
    Tag: sources / custom-metrics
    
    Args:
        sourceId: Path parameter
        customMetricName: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "put",
        "/api/sources/{sourceId}/custom-metrics/{customMetricName}",
        {"sourceId": sourceId, "customMetricName": customMetricName},
        {},
        body,
    )


@mcp.tool()
async def delete_source_custom_metrics(
    sourceId: str,
    customMetricName: str,
    body: dict | None = None,
) -> str:
    """
    Deletes a custom metric
    
    Requires WRITE permission on the source or READ permission on the source and ROLE_EDIT_FORMULAS
    
    API: DELETE /api/sources/{sourceId}/custom-metrics/{customMetricName}
    Tag: sources / custom-metrics
    
    Args:
        sourceId: Path parameter
        customMetricName: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "delete",
        "/api/sources/{sourceId}/custom-metrics/{customMetricName}",
        {"sourceId": sourceId, "customMetricName": customMetricName},
        {},
        body,
    )


@mcp.tool()
async def patch_source_custom_metrics(
    sourceId: str,
    customMetricName: str,
    body: dict | None = None,
) -> str:
    """
    Updates custom metric visibility
    
    Requires WRITE permission on the source or READ permission on the source and ROLE_EDIT_FORMULAS
    
    API: PATCH /api/sources/{sourceId}/custom-metrics/{customMetricName}
    Tag: sources / custom-metrics
    
    Args:
        sourceId: Path parameter
        customMetricName: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "patch",
        "/api/sources/{sourceId}/custom-metrics/{customMetricName}",
        {"sourceId": sourceId, "customMetricName": customMetricName},
        {},
        body,
    )


@mcp.tool()
async def get_source_cache_settings(
    sourceId: str,
    body: dict | None = None,
) -> str:
    """
    Returns cache settings for the data source
    
    Requires READ permission on the source
    
    API: GET /api/sources/{sourceId}/cache-settings
    Tag: sources / cache-settings
    
    Args:
        sourceId: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "get",
        "/api/sources/{sourceId}/cache-settings",
        {"sourceId": sourceId},
        {},
        body,
    )


@mcp.tool()
async def update_source_cache_settings(
    sourceId: str,
    body: dict | None = None,
) -> str:
    """
    Updates cache settings for data source
    
    Requires WRITE permission on the source
    
    API: PUT /api/sources/{sourceId}/cache-settings
    Tag: sources / cache-settings
    
    Args:
        sourceId: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "put",
        "/api/sources/{sourceId}/cache-settings",
        {"sourceId": sourceId},
        {},
        body,
    )


@mcp.tool()
async def update_source_acl_bulk(
    sourceId: str,
    body: dict | None = None,
) -> str:
    """
    Assign permissions on the source to a list of Security Identities (groups, users, account)
    
    Source identifier
    
    API: PUT /api/sources/{sourceId}/acls/bulk
    Tag: permissions
    
    Args:
        sourceId: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "put",
        "/api/sources/{sourceId}/acls/bulk",
        {"sourceId": sourceId},
        {},
        body,
    )


@mcp.tool()
async def patch_source_acl_bulk(
    sourceId: str,
    body: dict | None = None,
) -> str:
    """
    Grant/revoke permissions on the source to/from a list of Security Identities (groups, users, account)
    
    Source identifier
    
    API: PATCH /api/sources/{sourceId}/acls/bulk
    Tag: permissions
    
    Args:
        sourceId: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "patch",
        "/api/sources/{sourceId}/acls/bulk",
        {"sourceId": sourceId},
        {},
        body,
    )


@mcp.tool()
async def get_snippets(
    snippetId: str,
    body: dict | None = None,
) -> str:
    """
    (experimental) Returns the snippet by ID
    
    The snippet was retrieved successfully
    
    API: GET /api/snippets/{snippetId}
    Tag: snippets
    
    Args:
        snippetId: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "get",
        "/api/snippets/{snippetId}",
        {"snippetId": snippetId},
        {},
        body,
    )


@mcp.tool()
async def update_snippets(
    snippetId: str,
    body: dict | None = None,
) -> str:
    """
    (experimental) Updates the snippet. Creates a new one if snippet with provided ID does not exist
    
    The snippet was updated
    
    API: PUT /api/snippets/{snippetId}
    Tag: snippets
    
    Args:
        snippetId: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "put",
        "/api/snippets/{snippetId}",
        {"snippetId": snippetId},
        {},
        body,
    )


@mcp.tool()
async def delete_snippets(
    snippetId: str,
) -> str:
    """
    (experimental) Deletes the snippet
    
    The snippet was deleted successfully
    
    API: DELETE /api/snippets/{snippetId}
    Tag: snippets
    
    Args:
        snippetId: Path parameter
    """
    return await _call_api(
        "delete",
        "/api/snippets/{snippetId}",
        {"snippetId": snippetId},
        {},
        None,
    )


@mcp.tool()
async def get_security_global(
    body: dict | None = None,
) -> str:
    """
    Get global security config
    
    Supervisor authority or role Administer Users is required to access this endpoint
    
    API: GET /api/security/global
    Tag: global
    """
    return await _call_api(
        "get",
        "/api/security/global",
        {},
        {},
        body,
    )


@mcp.tool()
async def update_security_global(
    body: dict | None = None,
) -> str:
    """
    Update global security config
    
    Supervisor authority is required to access this endpoint
    
    API: PUT /api/security/global
    Tag: global
    """
    return await _call_api(
        "put",
        "/api/security/global",
        {},
        {},
        body,
    )


@mcp.tool()
async def update_quota(
    body: dict | None = None,
) -> str:
    """
    Update or create quota for an account
    
    Supervisor authority is required to access this endpoint
    
    API: PUT /api/quota
    Tag: quota
    """
    return await _call_api(
        "put",
        "/api/quota",
        {},
        {},
        body,
    )


@mcp.tool()
async def get_materialized_views(
    id: str,
    body: dict | None = None,
) -> str:
    """
    (deprecated since 23.1)Get Materialized view by id.
    
    OK
    
    API: GET /api/materialized-views/{id}
    Tag: materialized-view
    
    Args:
        id: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "get",
        "/api/materialized-views/{id}",
        {"id": id},
        {},
        body,
    )


@mcp.tool()
async def update_materialized_views(
    id: str,
    body: dict | None = None,
) -> str:
    """
    (deprecated since 23.1)Update Materialized view
    
    OK
    
    API: PUT /api/materialized-views/{id}
    Tag: materialized-view
    
    Args:
        id: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "put",
        "/api/materialized-views/{id}",
        {"id": id},
        {},
        body,
    )


@mcp.tool()
async def delete_materialized_views(
    id: str,
    body: dict | None = None,
) -> str:
    """
    (deprecated since 23.1)Delete Materialized view.
    
    No Content
    
    API: DELETE /api/materialized-views/{id}
    Tag: materialized-view
    
    Args:
        id: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "delete",
        "/api/materialized-views/{id}",
        {"id": id},
        {},
        body,
    )


@mcp.tool()
async def patch_materialized_views(
    id: str,
    body: dict | None = None,
) -> str:
    """
    (deprecated since 23.1)Update only specific properties (name, description, enabled) of a Materialized view.
    
    OK
    
    API: PATCH /api/materialized-views/{id}
    Tag: materialized-view
    
    Args:
        id: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "patch",
        "/api/materialized-views/{id}",
        {"id": id},
        {},
        body,
    )


@mcp.tool()
async def update_keyset_upload(
    keySetId: str,
    fileName: str | None = None,
    sourceId: str | None = None,
    keySetName: str | None = None,
    keySetDescription: str | None = None,
    body: dict | None = None,
) -> str:
    """
    (experimental) Update keyset from uploaded data as CSV body. CSV should not contain header
    
    The keyset was updated successfully
    
    API: PUT /api/keysets/upload/{keySetId}
    Tag: keyset
    
    Args:
        keySetId: Path parameter
        fileName: Query parameter (optional)
        sourceId: Query parameter (optional)
        keySetName: Query parameter (optional)
        keySetDescription: Query parameter (optional)
        body: JSON request body (optional)
    """
    return await _call_api(
        "put",
        "/api/keysets/upload/{keySetId}",
        {"keySetId": keySetId},
        {"fileName": fileName, "sourceId": sourceId, "keySetName": keySetName, "keySetDescription": keySetDescription},
        body,
    )


@mcp.tool()
async def get_groups(
    limit: str | None = None,
    offset: str | None = None,
    body: dict | None = None,
) -> str:
    """
    Returns a list of groups
    
    OK
    
    API: GET /api/groups
    Tag: groups
    """
    return await _call_api(
        "get",
        "/api/groups",
        {},
        {"limit": limit, "offset": offset},
        body,
    )


@mcp.tool()
async def create_groups(
    body: dict | None = None,
) -> str:
    """
    Create group
    
    OK
    
    API: POST /api/groups
    Tag: groups
    """
    return await _call_api(
        "post",
        "/api/groups",
        {},
        {},
        body,
    )


@mcp.tool()
async def update_groups(
    body: dict | None = None,
) -> str:
    """
    Update or create group
    
    No Content
    
    API: PUT /api/groups
    Tag: groups
    """
    return await _call_api(
        "put",
        "/api/groups",
        {},
        {},
        body,
    )


@mcp.tool()
async def get_filter_sets(
    id: str,
    body: dict | None = None,
) -> str:
    """
    Get filter
    
    OK
    
    API: GET /api/filter-sets/{id}
    Tag: filter-sets
    
    Args:
        id: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "get",
        "/api/filter-sets/{id}",
        {"id": id},
        {},
        body,
    )


@mcp.tool()
async def update_filter_sets(
    id: str,
    body: dict | None = None,
) -> str:
    """
    Update filter
    
    No Content
    
    API: PUT /api/filter-sets/{id}
    Tag: filter-sets
    
    Args:
        id: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "put",
        "/api/filter-sets/{id}",
        {"id": id},
        {},
        body,
    )


@mcp.tool()
async def delete_filter_sets(
    id: str,
) -> str:
    """
    Delete filter
    
    No Content
    
    API: DELETE /api/filter-sets/{id}
    Tag: filter-sets
    
    Args:
        id: Path parameter
    """
    return await _call_api(
        "delete",
        "/api/filter-sets/{id}",
        {"id": id},
        {},
        None,
    )


@mcp.tool()
async def get_dashboards(
    id: str,
    interactivityProfile: str | None = None,
    suppressWarnings: str | None = None,
    warningTags: str | None = None,
    body: dict | None = None,
) -> str:
    """
    Loads a dashboard (requires READ permission to the dashboard)
    
    Defines a dashboard identifier
    
    API: GET /api/dashboards/{id}
    Tag: dashboards
    
    Args:
        id: Path parameter
        interactivityProfile: Query parameter (optional)
        suppressWarnings: Query parameter (optional)
        warningTags: Query parameter (optional)
        body: JSON request body (optional)
    """
    return await _call_api(
        "get",
        "/api/dashboards/{id}",
        {"id": id},
        {"interactivityProfile": interactivityProfile, "suppressWarnings": suppressWarnings, "warningTags": warningTags},
        body,
    )


@mcp.tool()
async def update_dashboards(
    id: str,
    suppressWarnings: str | None = None,
    warningTags: str | None = None,
    body: dict | None = None,
) -> str:
    """
    Updates a dashboard (requires WRITE permission to the dashboard) or creates a new dashboard with custom id (requires the ROLE_CREATE_DASHBOARDS privilege)
    
    Defines a dashboard identifier
    
    API: PUT /api/dashboards/{id}
    Tag: dashboards
    
    Args:
        id: Path parameter
        suppressWarnings: Query parameter (optional)
        warningTags: Query parameter (optional)
        body: JSON request body (optional)
    """
    return await _call_api(
        "put",
        "/api/dashboards/{id}",
        {"id": id},
        {"suppressWarnings": suppressWarnings, "warningTags": warningTags},
        body,
    )


@mcp.tool()
async def delete_dashboards(
    id: str,
) -> str:
    """
    Deletes a dashboard (requires DELETE permission to the dashboard)
    
    Defines a dashboard identifier
    
    API: DELETE /api/dashboards/{id}
    Tag: dashboards
    
    Args:
        id: Path parameter
    """
    return await _call_api(
        "delete",
        "/api/dashboards/{id}",
        {"id": id},
        {},
        None,
    )


@mcp.tool()
async def get_dashboard_reports(
    dashboardId: str,
    reportId: str,
    deliverNow: str | None = None,
    body: dict | None = None,
) -> str:
    """
    Retrieve dashboard report settings by report ID
    
    Dashboard ID
    
    API: GET /api/dashboards/{dashboardId}/reports/{reportId}
    Tag: dashboard-reports
    
    Args:
        dashboardId: Path parameter
        reportId: Path parameter
        deliverNow: Query parameter (optional)
        body: JSON request body (optional)
    """
    return await _call_api(
        "get",
        "/api/dashboards/{dashboardId}/reports/{reportId}",
        {"dashboardId": dashboardId, "reportId": reportId},
        {"deliverNow": deliverNow},
        body,
    )


@mcp.tool()
async def update_dashboard_reports(
    dashboardId: str,
    reportId: str,
    deliverNow: str | None = None,
    body: dict | None = None,
) -> str:
    """
    Update dashboard report settings
    
    Dashboard ID
    
    API: PUT /api/dashboards/{dashboardId}/reports/{reportId}
    Tag: dashboard-reports
    
    Args:
        dashboardId: Path parameter
        reportId: Path parameter
        deliverNow: Query parameter (optional)
        body: JSON request body (optional)
    """
    return await _call_api(
        "put",
        "/api/dashboards/{dashboardId}/reports/{reportId}",
        {"dashboardId": dashboardId, "reportId": reportId},
        {"deliverNow": deliverNow},
        body,
    )


@mcp.tool()
async def delete_dashboard_reports(
    dashboardId: str,
    reportId: str,
) -> str:
    """
    Delete dashboard report settings
    
    Dashboard ID
    
    API: DELETE /api/dashboards/{dashboardId}/reports/{reportId}
    Tag: dashboard-reports
    
    Args:
        dashboardId: Path parameter
        reportId: Path parameter
    """
    return await _call_api(
        "delete",
        "/api/dashboards/{dashboardId}/reports/{reportId}",
        {"dashboardId": dashboardId, "reportId": reportId},
        {},
        None,
    )


@mcp.tool()
async def get_dashboard_interactivity(
    dashboardId: str,
    body: dict | None = None,
) -> str:
    """
    (experimental) Get related dashboard interactivity
    
    OK
    
    API: GET /api/dashboards/{dashboardId}/interactivity
    Tag: interactivity
    
    Args:
        dashboardId: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "get",
        "/api/dashboards/{dashboardId}/interactivity",
        {"dashboardId": dashboardId},
        {},
        body,
    )


@mcp.tool()
async def update_dashboard_interactivity(
    dashboardId: str,
    body: dict | None = None,
) -> str:
    """
    (experimental) Create or update related dashboard interactivity
    
    OK
    
    API: PUT /api/dashboards/{dashboardId}/interactivity
    Tag: interactivity
    
    Args:
        dashboardId: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "put",
        "/api/dashboards/{dashboardId}/interactivity",
        {"dashboardId": dashboardId},
        {},
        body,
    )


@mcp.tool()
async def delete_dashboard_interactivity(
    dashboardId: str,
) -> str:
    """
    (experimental) Delete related dashboard interactivity
    
    No Content
    
    API: DELETE /api/dashboards/{dashboardId}/interactivity
    Tag: interactivity
    
    Args:
        dashboardId: Path parameter
    """
    return await _call_api(
        "delete",
        "/api/dashboards/{dashboardId}/interactivity",
        {"dashboardId": dashboardId},
        {},
        None,
    )


@mcp.tool()
async def get_dashboard_comments(
    dashboardId: str,
    commentId: str,
    body: dict | None = None,
) -> str:
    """
    Get related dashboard comment
    
    The comment was retrieved successfully
    
    API: GET /api/dashboards/{dashboardId}/comments/{commentId}
    Tag: comments
    
    Args:
        dashboardId: Path parameter
        commentId: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "get",
        "/api/dashboards/{dashboardId}/comments/{commentId}",
        {"dashboardId": dashboardId, "commentId": commentId},
        {},
        body,
    )


@mcp.tool()
async def update_dashboard_comments(
    dashboardId: str,
    commentId: str,
    body: dict | None = None,
) -> str:
    """
    Update related dashboard comment
    
    The comment was updated successfully
    
    API: PUT /api/dashboards/{dashboardId}/comments/{commentId}
    Tag: comments
    
    Args:
        dashboardId: Path parameter
        commentId: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "put",
        "/api/dashboards/{dashboardId}/comments/{commentId}",
        {"dashboardId": dashboardId, "commentId": commentId},
        {},
        body,
    )


@mcp.tool()
async def delete_dashboard_comments(
    dashboardId: str,
    commentId: str,
) -> str:
    """
    Delete related dashboard comment
    
    The comment was deleted successfully
    
    API: DELETE /api/dashboards/{dashboardId}/comments/{commentId}
    Tag: comments
    
    Args:
        dashboardId: Path parameter
        commentId: Path parameter
    """
    return await _call_api(
        "delete",
        "/api/dashboards/{dashboardId}/comments/{commentId}",
        {"dashboardId": dashboardId, "commentId": commentId},
        {},
        None,
    )


@mcp.tool()
async def update_dashboard_acl_bulk(
    dashboardId: str,
    body: dict | None = None,
) -> str:
    """
    Assign permissions on the dashboard to a list of Security Identities (groups, users, account)
    
    Dashboard identifier
    
    API: PUT /api/dashboards/{dashboardId}/acls/bulk
    Tag: permissions
    
    Args:
        dashboardId: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "put",
        "/api/dashboards/{dashboardId}/acls/bulk",
        {"dashboardId": dashboardId},
        {},
        body,
    )


@mcp.tool()
async def patch_dashboard_acl_bulk(
    dashboardId: str,
    body: dict | None = None,
) -> str:
    """
    Grant/revoke permissions on the dashboard to/from a list of Security Identities (groups, users, account)
    
    Dashboard identifier
    
    API: PATCH /api/dashboards/{dashboardId}/acls/bulk
    Tag: untagged
    
    Args:
        dashboardId: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "patch",
        "/api/dashboards/{dashboardId}/acls/bulk",
        {"dashboardId": dashboardId},
        {},
        body,
    )


@mcp.tool()
async def get_customization_themes(
    id: str,
    body: dict | None = None,
) -> str:
    """
    Read theme
    
    OK
    
    API: GET /api/customization/themes/{id}
    Tag: customization
    
    Args:
        id: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "get",
        "/api/customization/themes/{id}",
        {"id": id},
        {},
        body,
    )


@mcp.tool()
async def update_customization_themes(
    id: str,
    body: dict | None = None,
) -> str:
    """
    Update theme
    
    OK
    
    API: PUT /api/customization/themes/{id}
    Tag: customization
    
    Args:
        id: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "put",
        "/api/customization/themes/{id}",
        {"id": id},
        {},
        body,
    )


@mcp.tool()
async def delete_customization_themes(
    id: str,
    body: dict | None = None,
) -> str:
    """
    Delete theme
    
    No Content
    
    API: DELETE /api/customization/themes/{id}
    Tag: customization
    
    Args:
        id: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "delete",
        "/api/customization/themes/{id}",
        {"id": id},
        {},
        body,
    )


@mcp.tool()
async def patch_customization_themes(
    id: str,
    body: dict | None = None,
) -> str:
    """
    Patch theme
    
    OK
    
    API: PATCH /api/customization/themes/{id}
    Tag: customization
    
    Args:
        id: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "patch",
        "/api/customization/themes/{id}",
        {"id": id},
        {},
        body,
    )


@mcp.tool()
async def get_connectors(
    id: str,
    body: dict | None = None,
) -> str:
    """
    Retrieve a Connector with a specific id
    
    Supervisor authority is required to access this endpoint
    
    API: GET /api/connectors/{id}
    Tag: connectors
    
    Args:
        id: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "get",
        "/api/connectors/{id}",
        {"id": id},
        {},
        body,
    )


@mcp.tool()
async def update_connectors(
    id: str,
    body: dict | None = None,
) -> str:
    """
    Update a Connector with a specific id
    
    Supervisor authority is required to access this endpoint
    
    API: PUT /api/connectors/{id}
    Tag: connectors
    
    Args:
        id: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "put",
        "/api/connectors/{id}",
        {"id": id},
        {},
        body,
    )


@mcp.tool()
async def delete_connectors(
    id: str,
) -> str:
    """
    Delete a connector with a specific id
    
    Supervisor authority is required to access this endpoint
    
    API: DELETE /api/connectors/{id}
    Tag: connectors
    
    Args:
        id: Path parameter
    """
    return await _call_api(
        "delete",
        "/api/connectors/{id}",
        {"id": id},
        {},
        None,
    )


@mcp.tool()
async def get_connections(
    connectionId: str,
    validate: str | None = None,
    suppressWarnings: str | None = None,
    connectionTypeMatchingStrategy: str | None = None,
    body: dict | None = None,
) -> str:
    """
    Load connection
    
    The response to this API endpoint may return a validation error with a list of problems. Each problem has a level (ERROR, WARNING). Passing suppressWarnings=true will suppress all warnings and the request will succeed if there are no errors
    
    API: GET /api/connections/{connectionId}
    Tag: connections
    
    Args:
        connectionId: Path parameter
        validate: Query parameter (optional)
        suppressWarnings: Query parameter (optional)
        connectionTypeMatchingStrategy: Query parameter (optional)
        body: JSON request body (optional)
    """
    return await _call_api(
        "get",
        "/api/connections/{connectionId}",
        {"connectionId": connectionId},
        {"validate": validate, "suppressWarnings": suppressWarnings, "connectionTypeMatchingStrategy": connectionTypeMatchingStrategy},
        body,
    )


@mcp.tool()
async def update_connections(
    connectionId: str,
    connectionTypeMatchingStrategy: str | None = None,
    suppressWarnings: str | None = None,
    body: dict | None = None,
) -> str:
    """
    Update or create connection (requires the ROLE_MANAGE_CONNECTIONS privilege)
    
    Connection ID
    
    API: PUT /api/connections/{connectionId}
    Tag: connections
    
    Args:
        connectionId: Path parameter
        connectionTypeMatchingStrategy: Query parameter (optional)
        suppressWarnings: Query parameter (optional)
        body: JSON request body (optional)
    """
    return await _call_api(
        "put",
        "/api/connections/{connectionId}",
        {"connectionId": connectionId},
        {"connectionTypeMatchingStrategy": connectionTypeMatchingStrategy, "suppressWarnings": suppressWarnings},
        body,
    )


@mcp.tool()
async def delete_connections(
    connectionId: str,
) -> str:
    """
    Delete connection (requires the ROLE_MANAGE_CONNECTIONS privilege)
    
    No Content
    
    API: DELETE /api/connections/{connectionId}
    Tag: connections
    
    Args:
        connectionId: Path parameter
    """
    return await _call_api(
        "delete",
        "/api/connections/{connectionId}",
        {"connectionId": connectionId},
        {},
        None,
    )


@mcp.tool()
async def update_connection_schema_configuration(
    connectionId: str,
    schemaName: str,
    body: dict | None = None,
) -> str:
    """
    Updates or creates a connection schema configuration
    
    The connection schema configuration was updated
    
    API: PUT /api/connections/{connectionId}/schema/{schemaName}/configuration
    Tag: connections
    
    Args:
        connectionId: Path parameter
        schemaName: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "put",
        "/api/connections/{connectionId}/schema/{schemaName}/configuration",
        {"connectionId": connectionId, "schemaName": schemaName},
        {},
        body,
    )


@mcp.tool()
async def get_connection_types(
    id: str,
    body: dict | None = None,
) -> str:
    """
    Retrieve specific Connection Type by Id
    
    OK
    
    API: GET /api/connection/types/{id}
    Tag: connection-types
    
    Args:
        id: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "get",
        "/api/connection/types/{id}",
        {"id": id},
        {},
        body,
    )


@mcp.tool()
async def update_connection_types(
    id: str,
    body: dict | None = None,
) -> str:
    """
    Update specific Connection Type by Id
    
    Supervisor authority is required to access this endpoint
    
    API: PUT /api/connection/types/{id}
    Tag: connection-types
    
    Args:
        id: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "put",
        "/api/connection/types/{id}",
        {"id": id},
        {},
        body,
    )


@mcp.tool()
async def delete_connection_types(
    id: str,
    body: dict | None = None,
) -> str:
    """
    Delete specific Connection Type by Id
    
    Supervisor authority is required to access this endpoint
    
    API: DELETE /api/connection/types/{id}
    Tag: connection-types
    
    Args:
        id: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "delete",
        "/api/connection/types/{id}",
        {"id": id},
        {},
        body,
    )


@mcp.tool()
async def patch_connection_types(
    id: str,
    body: dict | None = None,
) -> str:
    """
    Update properties of a specific Connection Type by Id
    
    Supervisor authority is required to access this endpoint
    
    API: PATCH /api/connection/types/{id}
    Tag: connection-types
    
    Args:
        id: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "patch",
        "/api/connection/types/{id}",
        {"id": id},
        {},
        body,
    )


@mcp.tool()
async def get_connection_type_accounts(
    id: str,
    body: dict | None = None,
) -> str:
    """
    Retrieve Connection Type accounts
    
    Supervisor authority is required to access this endpoint
    
    API: GET /api/connection/types/{id}/accounts
    Tag: connection-types
    
    Args:
        id: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "get",
        "/api/connection/types/{id}/accounts",
        {"id": id},
        {},
        body,
    )


@mcp.tool()
async def update_connection_type_accounts(
    id: str,
    body: dict | None = None,
) -> str:
    """
    Update Connection Type accounts. Empty list - available to all accounts
    
    Supervisor authority is required to access this endpoint
    
    API: PUT /api/connection/types/{id}/accounts
    Tag: connection-types
    
    Args:
        id: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "put",
        "/api/connection/types/{id}/accounts",
        {"id": id},
        {},
        body,
    )


@mcp.tool()
async def get_calendars(
    calendarId: str,
    body: dict | None = None,
) -> str:
    """
    (experimental) Load calendar by its id
    
    The calendar was retrieved
    
    API: GET /api/calendars/{calendarId}
    Tag: calendars
    
    Args:
        calendarId: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "get",
        "/api/calendars/{calendarId}",
        {"calendarId": calendarId},
        {},
        body,
    )


@mcp.tool()
async def update_calendars(
    calendarId: str,
    body: dict | None = None,
) -> str:
    """
    (experimental) Update calendar
    
    Requires ADMINISTER_CALENDARS role
    
    API: PUT /api/calendars/{calendarId}
    Tag: calendars
    
    Args:
        calendarId: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "put",
        "/api/calendars/{calendarId}",
        {"calendarId": calendarId},
        {},
        body,
    )


@mcp.tool()
async def delete_calendars(
    calendarId: str,
) -> str:
    """
    (experimental) Delete calendar by id
    
    Requires ADMINISTER_CALENDARS role
    
    API: DELETE /api/calendars/{calendarId}
    Tag: calendars
    
    Args:
        calendarId: Path parameter
    """
    return await _call_api(
        "delete",
        "/api/calendars/{calendarId}",
        {"calendarId": calendarId},
        {},
        None,
    )


@mcp.tool()
async def get_branding(
    body: dict | None = None,
) -> str:
    """
    Get branding configuration
    
    OK
    
    API: GET /api/branding
    Tag: branding
    """
    return await _call_api(
        "get",
        "/api/branding",
        {},
        {},
        body,
    )


@mcp.tool()
async def create_branding(
    body: dict | None = None,
) -> str:
    """
    Update branding configuration
    
    Supervisor authority is required to access this endpoint
    
    API: POST /api/branding
    Tag: branding
    """
    return await _call_api(
        "post",
        "/api/branding",
        {},
        {},
        body,
    )


@mcp.tool()
async def update_branding(
    body: dict | None = None,
) -> str:
    """
    Update branding configuration
    
    Supervisor authority is required to access this endpoint
    
    API: PUT /api/branding
    Tag: branding
    """
    return await _call_api(
        "put",
        "/api/branding",
        {},
        {},
        body,
    )


@mcp.tool()
async def get_branding_extensions(
    body: dict | None = None,
) -> str:
    """
    Load branding extensions
    
    OK
    
    API: GET /api/branding-extensions
    Tag: branding-extentions
    """
    return await _call_api(
        "get",
        "/api/branding-extensions",
        {},
        {},
        body,
    )


@mcp.tool()
async def update_branding_extensions(
    body: dict | None = None,
) -> str:
    """
    Update branding extensions
    
    Supervisor authority is required to access this endpoint
    
    API: PUT /api/branding-extensions
    Tag: branding-extentions
    """
    return await _call_api(
        "put",
        "/api/branding-extensions",
        {},
        {},
        body,
    )


@mcp.tool()
async def get_alerts(
    id: str,
    body: dict | None = None,
) -> str:
    """
    Return an alert by id
    
    Alert identifier
    
    API: GET /api/alerts/{id}
    Tag: alerts
    
    Args:
        id: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "get",
        "/api/alerts/{id}",
        {"id": id},
        {},
        body,
    )


@mcp.tool()
async def update_alerts(
    id: str,
    body: dict | None = None,
) -> str:
    """
    Update the existing alert (completely replace the previous version)
    
    Alert identifier
    
    API: PUT /api/alerts/{id}
    Tag: alerts
    
    Args:
        id: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "put",
        "/api/alerts/{id}",
        {"id": id},
        {},
        body,
    )


@mcp.tool()
async def delete_alerts(
    id: str,
    body: dict | None = None,
) -> str:
    """
    Delete the existing alert
    
    Alert identifier
    
    API: DELETE /api/alerts/{id}
    Tag: alerts
    
    Args:
        id: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "delete",
        "/api/alerts/{id}",
        {"id": id},
        {},
        body,
    )


@mcp.tool()
async def patch_alerts(
    id: str,
    body: dict | None = None,
) -> str:
    """
    Patch the existing alert (modify selected attributes)
    
    Alert identifier
    
    API: PATCH /api/alerts/{id}
    Tag: alerts
    
    Args:
        id: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "patch",
        "/api/alerts/{id}",
        {"id": id},
        {},
        body,
    )


@mcp.tool()
async def update_actions(
    id: str,
    body: dict | None = None,
) -> str:
    """
    Update an existing Action Template
    
    OK
    
    API: PUT /api/actions/{id}
    Tag: actions
    
    Args:
        id: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "put",
        "/api/actions/{id}",
        {"id": id},
        {},
        body,
    )


@mcp.tool()
async def delete_actions(
    id: str,
) -> str:
    """
    Delete an Action Template
    
    No Content
    
    API: DELETE /api/actions/{id}
    Tag: actions
    
    Args:
        id: Path parameter
    """
    return await _call_api(
        "delete",
        "/api/actions/{id}",
        {"id": id},
        {},
        None,
    )


@mcp.tool()
async def get_accounts(
    id: str,
    body: dict | None = None,
) -> str:
    """
    Load account
    
    Supervisor authority is required to access this endpoint
    
    API: GET /api/accounts/{id}
    Tag: accounts
    
    Args:
        id: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "get",
        "/api/accounts/{id}",
        {"id": id},
        {},
        body,
    )


@mcp.tool()
async def update_accounts(
    id: str,
    body: dict | None = None,
) -> str:
    """
    Update or create account
    
    Supervisor authority is required to access this endpoint
    
    API: PUT /api/accounts/{id}
    Tag: accounts
    
    Args:
        id: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "put",
        "/api/accounts/{id}",
        {"id": id},
        {},
        body,
    )


@mcp.tool()
async def delete_accounts(
    id: str,
) -> str:
    """
    Delete account
    
    Supervisor authority is required to access this endpoint
    
    API: DELETE /api/accounts/{id}
    Tag: accounts
    
    Args:
        id: Path parameter
    """
    return await _call_api(
        "delete",
        "/api/accounts/{id}",
        {"id": id},
        {},
        None,
    )


@mcp.tool()
async def get_account_users(
    accountId: str,
    body: dict | None = None,
) -> str:
    """
    Returns a list of account members
    
    Supervisor or ROLE_ADMINISTER_USERS authority is required to access this endpoint
    
    API: GET /api/accounts/{accountId}/users
    Tag: accounts / users
    
    Args:
        accountId: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "get",
        "/api/accounts/{accountId}/users",
        {"accountId": accountId},
        {},
        body,
    )


@mcp.tool()
async def update_account_users(
    accountId: str,
    body: dict | None = None,
) -> str:
    """
    Updates account members
    
    Supervisor or ROLE_ADMINISTER_USERS authority is required to access this endpoint
    
    API: PUT /api/accounts/{accountId}/users
    Tag: accounts / users
    
    Args:
        accountId: Path parameter
        body: JSON request body (optional)
    """
    return await _call_api(
        "put",
        "/api/accounts/{accountId}/users",
        {"accountId": accountId},
        {},
        body,
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    mcp.run()
