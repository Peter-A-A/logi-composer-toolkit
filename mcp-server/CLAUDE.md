# Logi Composer MCP Server — Guide for Claude

This MCP server provides 133 tools that map to the Logi Composer Discovery REST API. Use this guide to understand the API's structure, resource relationships, and common workflows.

## What is Logi Composer?

Logi Composer (also called Logi Symphony) is an embedded analytics platform by insightsoftware. The Discovery API manages the backend resources: data connections, sources, dashboards, visuals, users, and permissions.

## Base URL

All API calls go to `{COMPOSER_HOST}{COMPOSER_BASE_PATH}/api/...`. The base URL is assembled from two environment variables:
- `COMPOSER_HOST` — the server hostname (e.g. `http://localhost:8008` or `https://uat.logi-symphony.com`)
- `COMPOSER_BASE_PATH` — either `/composer` (local installs) or `/discovery` (cloud/UAT)

## Authentication

The API uses **HTTP Basic authentication**. Credentials are loaded from `COMPOSER_USERNAME` and `COMPOSER_PASSWORD` environment variables and sent as a Base64-encoded `Authorization: Basic ...` header. If the user hasn't set credentials, remind them to configure `.env`.

## Resource Hierarchy

Understanding how resources relate to each other is critical for chaining API calls correctly:

```
accounts
  └── users                    (account members)

connections                    (database/API connections)
  └── schema/configuration     (per-schema settings)

connection/types               (available connection type definitions)
  └── accounts                 (accounts linked to a connection type)

connectors                     (connector definitions)

sources                        (data sources built on connections)
  ├── fields                   (columns/measures in the source)
  ├── custom-metrics           (user-defined calculated fields)
  ├── visual-types             (chart types available for this source)
  ├── dictionaries             (localized labels, per language)
  ├── cache-settings           (caching configuration)
  ├── global-settings          (source-level settings)
  ├── unique-key               (deduplication key)
  ├── security                 (security overview)
  │   ├── filters              (row-level security / forced filters)
  │   ├── fields               (field-level security)
  │   ├── attributes           (security attribute settings)
  │   └── custom-metrics       (security on custom metrics)
  └── acls/bulk                (permissions)

dashboards                     (dashboard definitions)
  ├── reports                  (report widgets within the dashboard)
  ├── interactivity            (cross-filter / drill settings)
  ├── comments                 (annotations on the dashboard)
  └── acls/bulk                (permissions)

visuals                        (individual chart/visual definitions)
  └── acls/bulk                (permissions)

visual-types                   (chart type definitions)

filter-sets                    (saved filter configurations)
uploads                        (uploaded data files)
  └── data                     (the actual file data)

users                          (user accounts)
  └── permissions              (user segregation conditions)

groups                         (user groups)

customization
  └── themes                   (UI themes)

branding                       (branding configuration)
branding-extensions            (extended branding)

alerts                         (alert definitions)
actions                        (action templates triggered by alerts)
calendars                      (calendar definitions)
snippets                       (reusable content snippets)
keysets                        (encryption/security keysets)
quota                          (usage quotas)
materialized-views             (deprecated since v23.1)

security/global                (global security configuration)
system/activity                (activity logging toggles)
toggles                        (feature toggles)
```

## Common Workflows

### List and inspect data sources
1. There is no "list all sources" endpoint in the spec. You may need to use `composer_api_request("GET", "/api/sources")` or ask the user for a source ID.
2. `get_sources(sourceId=...)` — get source details
3. `get_source_fields(sourceId=...)` — list all fields in the source
4. `get_source_fields_1(sourceId=..., fieldName=...)` — get a specific field
5. `get_source_visual_types(sourceId=...)` — see what chart types are available

### Inspect a dashboard
1. `get_dashboards(id=...)` — load the dashboard definition
2. `get_dashboard_reports(dashboardId=..., reportId=...)` — get a specific report/widget
3. `get_dashboard_interactivity(dashboardId=...)` — see cross-filtering setup
4. `get_dashboard_comments(dashboardId=..., commentId=...)` — read annotations

### Manage permissions
Permissions use ACL (Access Control List) bulk operations:
- `update_dashboard_acl_bulk(dashboardId=..., body=...)` — set dashboard permissions
- `update_source_acl_bulk(sourceId=..., body=...)` — set source permissions
- `update_visual_acl_bulk(id=..., body=...)` — set visual permissions
- `patch_*_acl_bulk` variants do partial updates instead of full replacement

### Manage source security (row-level / field-level)
1. `get_source_security(sourceId=...)` — overview of security settings
2. `get_source_fields(sourceId=...)` → then `update_source_security_fields(sourceId=..., id=..., body=...)` for field-level
3. `update_source_security_filters(sourceId=..., id=..., body=...)` — set forced filters (row-level security)

### User and account management
1. `get_users(id=...)` — load a user
2. `get_accounts(id=...)` — load an account
3. `get_account_users(accountId=...)` — list members of an account
4. `get_groups()` — list all groups
5. `get_user_permissions(sid=...)` — get user segregation conditions

### Connections and connectors
1. `get_connections(connectionId=...)` — load a connection
2. `get_connection_types(id=...)` — get a connection type definition
3. `get_connectors(id=...)` — get a connector
4. `update_connection_schema_configuration(connectionId=..., schemaName=..., body=...)` — configure schema

## Generic Passthrough Tool

If you need to call an endpoint that doesn't have a dedicated tool (e.g., list endpoints, or endpoints that were truncated from the spec), use:

```
composer_api_request(method="GET", path="/api/sources", query_params={"limit": "100"})
```

This accepts any method, path, query params, and body.

## Parameter Conventions

- **Path parameters** like `sourceId`, `id`, `dashboardId` are always strings (typically UUIDs or numeric IDs)
- **Query parameters** are optional strings passed as keyword arguments
- **Body parameters** are Python dicts passed as `body={...}` for PUT/POST/PATCH requests
- All tools return a JSON string with `status_code` and `data` (or `text` for non-JSON responses)

## Response Format

Every tool returns a JSON string:
```json
{
  "status_code": 200,
  "data": { ... }
}
```

If the response isn't JSON:
```json
{
  "status_code": 200,
  "text": "..."
}
```

Check `status_code` first. Common codes: 200 (OK), 201 (Created), 204 (No Content for deletes), 401 (token expired), 403 (insufficient permissions), 404 (not found).

## Important Notes

- The user (Peter) works specifically with **Composer Discovery / VDD** (Visual Data Discovery). Do NOT reference Dundas BI managed layer concepts.
- The API spec was truncated during fetch, so some endpoints may be missing dedicated tools. Use `composer_api_request` as a fallback.
- Some endpoints are marked **(experimental)** or **(deprecated)** in their summaries — flag these to the user.
- For PUT operations, you typically need to GET the resource first, modify the returned data, then PUT it back.
