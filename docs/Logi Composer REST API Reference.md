# Logi Composer REST API Reference

**OpenAPI Version:** 3.1.0
**Base URL:** `https://<server>/discovery`
**Spec Source:** https://uat.logi-symphony.com/discovery/api-docs
**Note:** This spec was fetched 2026-05-05 and was truncated at ~109K chars. Some endpoints (especially later POST/DELETE operations and component schemas) may be incomplete.

## Authentication

The API uses Bearer token authentication. Include `Authorization: Bearer <token>` header.

## Endpoints by Category

### accounts

**`GET /api/actions/{id}`**
- Operation: `load`
- Summary: Load account
- Description: Supervisor authority is required to access this endpoint
- Parameters: id (in path), id (in path), id (in path), accountId (in path)

**`GET /api/accounts/{id}`**
- Operation: `load`
- Summary: Load account
- Description: Supervisor authority is required to access this endpoint
- Parameters: id (in path), id (in path), id (in path), accountId (in path)

**`PUT /api/accounts/{id}`**
- Operation: `updateOrCreateAccount`
- Summary: Update or create account
- Description: Supervisor authority is required to access this endpoint
- Parameters: id (in path), id (in path), accountId (in path)

**`DELETE /api/accounts/{id}`**
- Operation: `delete_19`
- Summary: Delete account
- Description: Supervisor authority is required to access this endpoint
- Parameters: id (in path), accountId (in path), accountId (in path)

### accounts / users

**`GET /api/accounts/{accountId}/users`**
- Operation: `get_11`
- Summary: Returns a list of account members
- Description: Supervisor or ROLE_ADMINISTER_USERS authority is required to access this endpoint
- Parameters: accountId (in path), accountId (in path)

**`PUT /api/accounts/{accountId}/users`**
- Operation: `update_20`
- Summary: Updates account members
- Description: Supervisor or ROLE_ADMINISTER_USERS authority is required to access this endpoint
- Parameters: accountId (in path)

### actions

**`PUT /api/actions/{id}`**
- Operation: `update_19`
- Summary: Update an existing Action Template
- Description: OK
- Parameters: id (in path), id (in path), id (in path), id (in path), id (in path)

**`DELETE /api/actions/{id}`**
- Operation: `delete_18`
- Summary: Delete an Action Template
- Description: No Content
- Parameters: id (in path), id (in path), id (in path), id (in path), accountId (in path)

### activity

**`GET /api/system/activity/type/{activityType}`**
- Operation: `getActivityLoggingSettings`
- Summary: Get the toggle status of a specific activity type
- Description: Supervisor authority is required to access this endpoint
- Parameters: activityType (in path), activityType (in path), sourceId (in path)

**`PUT /api/system/activity/type/{activityType}`**
- Operation: `updateActivityLoggingSettings`
- Summary: Update an activity type to toggle its logging
- Description: Supervisor authority is required to access this endpoint
- Parameters: activityType (in path), sourceId (in path), sourceId (in path), suppressWarnings (in query)

### alerts

**`DELETE /api/branding`**
- Operation: `deleteAlert`
- Summary: Delete the existing alert
- Description: Alert identifier
- Parameters: id (in path), id (in path)

**`PATCH /api/branding`**
- Operation: `patchAlert`
- Summary: Patch the existing alert (modify selected attributes)
- Description: Alert identifier
- Parameters: id (in path), id (in path), id (in path)

**`DELETE /api/branding-extensions`**
- Operation: `deleteAlert`
- Summary: Delete the existing alert
- Description: Alert identifier
- Parameters: id (in path), id (in path)

**`PATCH /api/branding-extensions`**
- Operation: `patchAlert`
- Summary: Patch the existing alert (modify selected attributes)
- Description: Alert identifier
- Parameters: id (in path), id (in path), id (in path)

**`GET /api/alerts/{id}`**
- Operation: `getAlert`
- Summary: Return an alert by id
- Description: Alert identifier
- Parameters: id (in path), id (in path)

**`PUT /api/alerts/{id}`**
- Operation: `updateAlert`
- Summary: Update the existing alert (completely replace the previous version)
- Description: Alert identifier
- Parameters: id (in path), id (in path)

**`DELETE /api/alerts/{id}`**
- Operation: `deleteAlert`
- Summary: Delete the existing alert
- Description: Alert identifier
- Parameters: id (in path), id (in path)

**`PATCH /api/alerts/{id}`**
- Operation: `patchAlert`
- Summary: Patch the existing alert (modify selected attributes)
- Description: Alert identifier
- Parameters: id (in path), id (in path), id (in path)

### branding

**`POST /api/connection/types/{id}/accounts`**
- Operation: `updateBrandingPost`
- Summary: Update branding configuration
- Description: Supervisor authority is required to access this endpoint
- Parameters: id (in path)

**`POST /api/calendars/{calendarId}`**
- Operation: `updateBrandingPost`
- Summary: Update branding configuration
- Description: Supervisor authority is required to access this endpoint
- Parameters: id (in path)

**`GET /api/branding`**
- Operation: `getBrandingConfig`
- Summary: Get branding configuration
- Description: OK
- Parameters: id (in path)

**`POST /api/branding`**
- Operation: `updateBrandingPost`
- Summary: Update branding configuration
- Description: Supervisor authority is required to access this endpoint
- Parameters: id (in path)

**`PUT /api/branding`**
- Operation: `updateBrandingPut`
- Summary: Update branding configuration
- Description: Supervisor authority is required to access this endpoint
- Parameters: id (in path)

### branding-extentions

**`GET /api/branding-extensions`**
- Operation: `getExtensions`
- Summary: Load branding extensions
- Description: OK
- Parameters: id (in path), id (in path)

**`PUT /api/branding-extensions`**
- Operation: `updateExtensions`
- Summary: Update branding extensions
- Description: Supervisor authority is required to access this endpoint
- Parameters: id (in path), id (in path)

### calendars

**`DELETE /api/connection/types/{id}/accounts`**
- Operation: `delete_17`
- Summary: (experimental) Delete calendar by id
- Description: Requires ADMINISTER_CALENDARS role
- Parameters: calendarId (in path)

**`GET /api/calendars/{calendarId}`**
- Operation: `get_10`
- Summary: (experimental) Load calendar by its id
- Description: The calendar was retrieved
- Parameters: calendarId (in path), calendarId (in path)

**`PUT /api/calendars/{calendarId}`**
- Operation: `update_18`
- Summary: (experimental) Update calendar
- Description: Requires ADMINISTER_CALENDARS role
- Parameters: calendarId (in path), calendarId (in path)

**`DELETE /api/calendars/{calendarId}`**
- Operation: `delete_17`
- Summary: (experimental) Delete calendar by id
- Description: Requires ADMINISTER_CALENDARS role
- Parameters: calendarId (in path)

### comments

**`GET /api/dashboards/{dashboardId}/comments/{commentId}`**
- Operation: `getCommentById`
- Summary: Get related dashboard comment
- Description: The comment was retrieved successfully
- Parameters: dashboardId (in path), commentId (in path), dashboardId (in path), commentId (in path)

**`PUT /api/dashboards/{dashboardId}/comments/{commentId}`**
- Operation: `update_14`
- Summary: Update related dashboard comment
- Description: The comment was updated successfully
- Parameters: dashboardId (in path), commentId (in path), dashboardId (in path), commentId (in path)

**`DELETE /api/dashboards/{dashboardId}/comments/{commentId}`**
- Operation: `delete_13`
- Summary: Delete related dashboard comment
- Description: The comment was deleted successfully
- Parameters: dashboardId (in path), commentId (in path), dashboardId (in path), dashboardId (in path)

### connection-types

**`GET /api/connections/{connectionId}/schema/{schemaName}/configuration`**
- Operation: `get_9`
- Summary: Retrieve specific Connection Type by Id
- Description: OK
- Parameters: id (in path), id (in path), id (in path), id (in path)

**`DELETE /api/connections/{connectionId}/schema/{schemaName}/configuration`**
- Operation: `delete_16`
- Summary: Delete specific Connection Type by Id
- Description: Supervisor authority is required to access this endpoint
- Parameters: id (in path), id (in path), id (in path), id (in path)

**`PATCH /api/connections/{connectionId}/schema/{schemaName}/configuration`**
- Operation: `updateProperties`
- Summary: Update properties of a specific Connection Type by Id
- Description: Supervisor authority is required to access this endpoint
- Parameters: id (in path), id (in path), id (in path), calendarId (in path)

**`GET /api/connection/types/{id}`**
- Operation: `get_9`
- Summary: Retrieve specific Connection Type by Id
- Description: OK
- Parameters: id (in path), id (in path), id (in path), id (in path)

**`PUT /api/connection/types/{id}`**
- Operation: `update_17`
- Summary: Update specific Connection Type by Id
- Description: Supervisor authority is required to access this endpoint
- Parameters: id (in path), id (in path), id (in path), id (in path)

**`DELETE /api/connection/types/{id}`**
- Operation: `delete_16`
- Summary: Delete specific Connection Type by Id
- Description: Supervisor authority is required to access this endpoint
- Parameters: id (in path), id (in path), id (in path), id (in path)

**`PATCH /api/connection/types/{id}`**
- Operation: `updateProperties`
- Summary: Update properties of a specific Connection Type by Id
- Description: Supervisor authority is required to access this endpoint
- Parameters: id (in path), id (in path), id (in path), calendarId (in path)

**`GET /api/connection/types/{id}/accounts`**
- Operation: `getAccounts`
- Summary: Retrieve Connection Type accounts
- Description: Supervisor authority is required to access this endpoint
- Parameters: id (in path), id (in path), calendarId (in path)

**`PUT /api/connection/types/{id}/accounts`**
- Operation: `setAccounts`
- Summary: Update Connection Type accounts. Empty list - available to all accounts
- Description: Supervisor authority is required to access this endpoint
- Parameters: id (in path), calendarId (in path), calendarId (in path)

### connections

**`GET /api/connections/{connectionId}`**
- Operation: `getConnection`
- Summary: Load connection
- Description: The response to this API endpoint may return a validation error with a list of problems. Each problem has a level (ERROR, WARNING). Passing suppressWarnings=true will suppress all warnings and the request will succeed if there are no errors
- Parameters: connectionId (in path), validate (in query), suppressWarnings (in query), connectionId (in path), connectionTypeMatchingStrategy (in query), suppressWarnings (in query)

**`PUT /api/connections/{connectionId}`**
- Operation: `createOrUpdateConnection`
- Summary: Update or create connection (requires the ROLE_MANAGE_CONNECTIONS privilege)
- Description: Connection ID
- Parameters: connectionId (in path), connectionTypeMatchingStrategy (in query), suppressWarnings (in query), connectionId (in path), connectionId (in path), schemaName (in path)

**`DELETE /api/connections/{connectionId}`**
- Operation: `deleteConnection`
- Summary: Delete connection (requires the ROLE_MANAGE_CONNECTIONS privilege)
- Description: No Content
- Parameters: connectionId (in path), connectionId (in path), schemaName (in path), id (in path)

**`PUT /api/connections/{connectionId}/schema/{schemaName}/configuration`**
- Operation: `createOrUpdateConnectionSchemaInfo`
- Summary: Updates or creates a connection schema configuration
- Description: The connection schema configuration was updated
- Parameters: connectionId (in path), schemaName (in path), id (in path), id (in path)

### connectors

**`GET /api/connectors/{id}`**
- Operation: `get_8`
- Summary: Retrieve a Connector with a specific id
- Description: Supervisor authority is required to access this endpoint
- Parameters: id (in path), id (in path), id (in path), connectionId (in path), validate (in query), suppressWarnings (in query)

**`PUT /api/connectors/{id}`**
- Operation: `update_16`
- Summary: Update a Connector with a specific id
- Description: Supervisor authority is required to access this endpoint
- Parameters: id (in path), id (in path), connectionId (in path), validate (in query), suppressWarnings (in query), connectionId (in path)

**`DELETE /api/connectors/{id}`**
- Operation: `delete_15`
- Summary: Delete a connector with a specific id
- Description: Supervisor authority is required to access this endpoint
- Parameters: id (in path), connectionId (in path), validate (in query), suppressWarnings (in query), connectionId (in path), connectionTypeMatchingStrategy (in query), suppressWarnings (in query)

### customization

**`PATCH /api/dashboards/{dashboardId}/comments/{commentId}`**
- Operation: `updatePermissionsOnDashboard`
- Summary: Grant/revoke permissions on the dashboard to/from a list of Security Identities (groups, users, account)
- Description: Dashboard identifier
- Parameters: dashboardId (in path), id (in path), id (in path), id (in path), id (in path)

**`GET /api/dashboards/{dashboardId}/acls/bulk`**
- Operation: `read_1`
- Summary: Read theme
- Description: OK
- Parameters: id (in path), id (in path), id (in path), id (in path), id (in path)

**`DELETE /api/dashboards/{dashboardId}/acls/bulk`**
- Operation: `delete_14`
- Summary: Delete theme
- Description: No Content
- Parameters: id (in path), id (in path), id (in path), id (in path), id (in path)

**`PATCH /api/dashboards/{dashboardId}/acls/bulk`**
- Operation: `updatePermissionsOnDashboard`
- Summary: Grant/revoke permissions on the dashboard to/from a list of Security Identities (groups, users, account)
- Description: Dashboard identifier
- Parameters: dashboardId (in path), id (in path), id (in path), id (in path), id (in path)

**`GET /api/customization/themes/{id}`**
- Operation: `read_1`
- Summary: Read theme
- Description: OK
- Parameters: id (in path), id (in path), id (in path), id (in path), id (in path)

**`PUT /api/customization/themes/{id}`**
- Operation: `update_15`
- Summary: Update theme
- Description: OK
- Parameters: id (in path), id (in path), id (in path), id (in path), id (in path)

**`DELETE /api/customization/themes/{id}`**
- Operation: `delete_14`
- Summary: Delete theme
- Description: No Content
- Parameters: id (in path), id (in path), id (in path), id (in path), id (in path)

**`PATCH /api/customization/themes/{id}`**
- Operation: `patch_1`
- Summary: Patch theme
- Description: OK
- Parameters: id (in path), id (in path), id (in path), id (in path), connectionId (in path), validate (in query)

### dashboard-reports

**`GET /api/dashboards/{dashboardId}/reports/{reportId}`**
- Operation: `findReportById`
- Summary: Retrieve dashboard report settings by report ID
- Description: Dashboard ID
- Parameters: dashboardId (in path), reportId (in path), dashboardId (in path), reportId (in path), deliverNow (in query), dashboardId (in path), reportId (in path)

**`PUT /api/dashboards/{dashboardId}/reports/{reportId}`**
- Operation: `updateReport`
- Summary: Update dashboard report settings
- Description: Dashboard ID
- Parameters: dashboardId (in path), reportId (in path), deliverNow (in query), dashboardId (in path), reportId (in path), dashboardId (in path), dashboardId (in path)

**`DELETE /api/dashboards/{dashboardId}/reports/{reportId}`**
- Operation: `deleteReport`
- Summary: Delete dashboard report settings
- Description: Dashboard ID
- Parameters: dashboardId (in path), reportId (in path), dashboardId (in path), dashboardId (in path), dashboardId (in path), dashboardId (in path), commentId (in path)

### dashboards

**`GET /api/dashboards/{id}`**
- Operation: `get_7`
- Summary: Loads a dashboard (requires READ permission to the dashboard)
- Description: Defines a dashboard identifier
- Parameters: id (in path), interactivityProfile (in query), id (in path), suppressWarnings (in query), warningTags (in query)

**`PUT /api/dashboards/{id}`**
- Operation: `update_13`
- Summary: Updates a dashboard (requires WRITE permission to the dashboard) or creates a new dashboard with custom id (requires the ROLE_CREATE_DASHBOARDS privilege)
- Description: Defines a dashboard identifier
- Parameters: id (in path), suppressWarnings (in query), warningTags (in query)

**`DELETE /api/dashboards/{id}`**
- Operation: `delete_12`
- Summary: Deletes a dashboard (requires DELETE permission to the dashboard)
- Description: Defines a dashboard identifier
- Parameters: id (in path), dashboardId (in path), reportId (in path), dashboardId (in path), reportId (in path), deliverNow (in query)

### filter-sets

**`DELETE /api/keysets/upload/{keySetId}`**
- Operation: `delete_11`
- Summary: Delete filter
- Description: No Content
- Parameters: id (in path), id (in path), interactivityProfile (in query), id (in path), suppressWarnings (in query)

**`DELETE /api/groups`**
- Operation: `delete_11`
- Summary: Delete filter
- Description: No Content
- Parameters: id (in path), id (in path), interactivityProfile (in query), id (in path), suppressWarnings (in query)

**`GET /api/filter-sets/{id}`**
- Operation: `get_6`
- Summary: Get filter
- Description: OK
- Parameters: id (in path), id (in path), id (in path), id (in path), interactivityProfile (in query)

**`PUT /api/filter-sets/{id}`**
- Operation: `update_12`
- Summary: Update filter
- Description: No Content
- Parameters: id (in path), id (in path), id (in path), interactivityProfile (in query), id (in path)

**`DELETE /api/filter-sets/{id}`**
- Operation: `delete_11`
- Summary: Delete filter
- Description: No Content
- Parameters: id (in path), id (in path), interactivityProfile (in query), id (in path), suppressWarnings (in query)

### global

**`GET /api/security/global`**
- Operation: `get_4`
- Summary: Get global security config
- Description: Supervisor authority or role Administer Users is required to access this endpoint
- Parameters: id (in path), id (in path)

**`PUT /api/security/global`**
- Operation: `update_10`
- Summary: Update global security config
- Description: Supervisor authority is required to access this endpoint
- Parameters: id (in path), id (in path), id (in path)

### groups

**`POST /api/quota`**
- Operation: `createGroup`
- Summary: Create group
- Description: OK
- Parameters: id (in path), id (in path), id (in path), id (in path), interactivityProfile (in query)

**`POST /api/materialized-views/{id}`**
- Operation: `createGroup`
- Summary: Create group
- Description: OK
- Parameters: id (in path), id (in path), id (in path), id (in path), interactivityProfile (in query)

**`GET /api/keysets/upload/{keySetId}`**
- Operation: `list_1`
- Summary: Returns a list of groups
- Description: OK
- Parameters: limit (in query), offset (in query), id (in path), id (in path), id (in path)

**`POST /api/keysets/upload/{keySetId}`**
- Operation: `createGroup`
- Summary: Create group
- Description: OK
- Parameters: id (in path), id (in path), id (in path), id (in path), interactivityProfile (in query)

**`GET /api/groups`**
- Operation: `list_1`
- Summary: Returns a list of groups
- Description: OK
- Parameters: limit (in query), offset (in query), id (in path), id (in path), id (in path)

**`POST /api/groups`**
- Operation: `createGroup`
- Summary: Create group
- Description: OK
- Parameters: id (in path), id (in path), id (in path), id (in path), interactivityProfile (in query)

**`PUT /api/groups`**
- Operation: `updateGroup`
- Summary: Update or create group
- Description: No Content
- Parameters: id (in path), id (in path), id (in path), id (in path), interactivityProfile (in query)

### interactivity

**`GET /api/dashboards/{dashboardId}/interactivity`**
- Operation: `getProfileById`
- Summary: (experimental) Get related dashboard interactivity
- Description: OK
- Parameters: dashboardId (in path), dashboardId (in path), dashboardId (in path), dashboardId (in path), commentId (in path)

**`PUT /api/dashboards/{dashboardId}/interactivity`**
- Operation: `createOrUpdateProfileForDashboard`
- Summary: (experimental) Create or update related dashboard interactivity
- Description: OK
- Parameters: dashboardId (in path), dashboardId (in path), dashboardId (in path), commentId (in path)

**`DELETE /api/dashboards/{dashboardId}/interactivity`**
- Operation: `deleteInteractivityForDashboard`
- Summary: (experimental) Delete related dashboard interactivity
- Description: No Content
- Parameters: dashboardId (in path), dashboardId (in path), commentId (in path), dashboardId (in path), commentId (in path)

### keyset

**`PUT /api/keysets/upload/{keySetId}`**
- Operation: `updateFromUpload`
- Summary: (experimental) Update keyset from uploaded data as CSV body. CSV should not contain header
- Description: The keyset was updated successfully
- Parameters: keySetId (in path), fileName (in query), sourceId (in query), keySetName (in query), keySetDescription (in query), limit (in query), offset (in query)

### materialized-view

**`DELETE /api/security/global`**
- Operation: `delete_10`
- Summary: (deprecated since 23.1)Delete Materialized view.
- Description: No Content
- Parameters: id (in path), id (in path), keySetId (in path), fileName (in query), sourceId (in query), keySetName (in query), keySetDescription (in query)

**`PATCH /api/security/global`**
- Operation: `patch`
- Summary: (deprecated since 23.1)Update only specific properties (name, description, enabled) of a Materialized view.
- Description: OK
- Parameters: id (in path), keySetId (in path), fileName (in query), sourceId (in query), keySetName (in query), keySetDescription (in query)

**`GET /api/quota`**
- Operation: `get_5`
- Summary: (deprecated since 23.1)Get Materialized view by id.
- Description: OK
- Parameters: id (in path), id (in path), id (in path), id (in path)

**`DELETE /api/quota`**
- Operation: `delete_10`
- Summary: (deprecated since 23.1)Delete Materialized view.
- Description: No Content
- Parameters: id (in path), id (in path), keySetId (in path), fileName (in query), sourceId (in query), keySetName (in query), keySetDescription (in query)

**`PATCH /api/quota`**
- Operation: `patch`
- Summary: (deprecated since 23.1)Update only specific properties (name, description, enabled) of a Materialized view.
- Description: OK
- Parameters: id (in path), keySetId (in path), fileName (in query), sourceId (in query), keySetName (in query), keySetDescription (in query)

**`GET /api/materialized-views/{id}`**
- Operation: `get_5`
- Summary: (deprecated since 23.1)Get Materialized view by id.
- Description: OK
- Parameters: id (in path), id (in path), id (in path), id (in path)

**`PUT /api/materialized-views/{id}`**
- Operation: `update_11`
- Summary: (deprecated since 23.1)Update Materialized view
- Description: OK
- Parameters: id (in path), id (in path), id (in path), keySetId (in path), fileName (in query), sourceId (in query), keySetName (in query), keySetDescription (in query)

**`DELETE /api/materialized-views/{id}`**
- Operation: `delete_10`
- Summary: (deprecated since 23.1)Delete Materialized view.
- Description: No Content
- Parameters: id (in path), id (in path), keySetId (in path), fileName (in query), sourceId (in query), keySetName (in query), keySetDescription (in query)

**`PATCH /api/materialized-views/{id}`**
- Operation: `patch`
- Summary: (deprecated since 23.1)Update only specific properties (name, description, enabled) of a Materialized view.
- Description: OK
- Parameters: id (in path), keySetId (in path), fileName (in query), sourceId (in query), keySetName (in query), keySetDescription (in query)

### permissions

**`PATCH /api/visuals/{id}`**
- Operation: `updatePermissionsOnVisual`
- Summary: Grant/revoke permissions on the visual to/from a list of Security Identities (groups, users, account)
- Description: Visual identifier
- Parameters: id (in path), id (in path), componentBody (in query), id (in path), id (in path), id (in path)

**`PUT /api/visuals/{id}/acls/bulk`**
- Operation: `setPermissionsOnVisual`
- Summary: Assign permissions on the visual to a list of Security Identities (groups, users, account)
- Description: Visual identifier
- Parameters: id (in path), id (in path), id (in path), componentBody (in query)

**`PATCH /api/visuals/{id}/acls/bulk`**
- Operation: `updatePermissionsOnVisual`
- Summary: Grant/revoke permissions on the visual to/from a list of Security Identities (groups, users, account)
- Description: Visual identifier
- Parameters: id (in path), id (in path), componentBody (in query), id (in path), id (in path), id (in path)

**`PATCH /api/sources/{sourceId}/cache-settings`**
- Operation: `updatePermissionsOnSource`
- Summary: Grant/revoke permissions on the source to/from a list of Security Identities (groups, users, account)
- Description: Source identifier
- Parameters: sourceId (in path), snippetId (in path), snippetId (in path)

**`PUT /api/sources/{sourceId}/acls/bulk`**
- Operation: `setPermissionsOnSource`
- Summary: Assign permissions on the source to a list of Security Identities (groups, users, account)
- Description: Source identifier
- Parameters: sourceId (in path), sourceId (in path), snippetId (in path)

**`PATCH /api/sources/{sourceId}/acls/bulk`**
- Operation: `updatePermissionsOnSource`
- Summary: Grant/revoke permissions on the source to/from a list of Security Identities (groups, users, account)
- Description: Source identifier
- Parameters: sourceId (in path), snippetId (in path), snippetId (in path)

**`PUT /api/dashboards/{dashboardId}/acls/bulk`**
- Operation: `setPermissionsOnDashboard`
- Summary: Assign permissions on the dashboard to a list of Security Identities (groups, users, account)
- Description: Dashboard identifier
- Parameters: dashboardId (in path), dashboardId (in path), id (in path)

### quota

**`PUT /api/quota`**
- Operation: `upsertQuota`
- Summary: Update or create quota for an account
- Description: Supervisor authority is required to access this endpoint
- Parameters: id (in path), id (in path), id (in path), id (in path)

### snippets

**`GET /api/sources/{sourceId}/acls/bulk`**
- Operation: `get_3`
- Summary: (experimental) Returns the snippet by ID
- Description: The snippet was retrieved successfully
- Parameters: snippetId (in path), snippetId (in path)

**`DELETE /api/sources/{sourceId}/acls/bulk`**
- Operation: `delete_9`
- Summary: (experimental) Deletes the snippet
- Description: The snippet was deleted successfully
- Parameters: snippetId (in path)

**`GET /api/snippets/{snippetId}`**
- Operation: `get_3`
- Summary: (experimental) Returns the snippet by ID
- Description: The snippet was retrieved successfully
- Parameters: snippetId (in path), snippetId (in path)

**`PUT /api/snippets/{snippetId}`**
- Operation: `update_9`
- Summary: (experimental) Updates the snippet. Creates a new one if snippet with provided ID does not exist
- Description: The snippet was updated
- Parameters: snippetId (in path), snippetId (in path)

**`DELETE /api/snippets/{snippetId}`**
- Operation: `delete_9`
- Summary: (experimental) Deletes the snippet
- Description: The snippet was deleted successfully
- Parameters: snippetId (in path)

### sources

**`DELETE /api/system/activity/type/{activityType}`**
- Operation: `delete_5`
- Summary: Deletes a source
- Description: Requires DELETE permission on the source
- Parameters: sourceId (in path), sourceId (in path), maxResults (in query), pageToken (in query), includeDisabled (in query), includeRestriction (in query)

**`GET /api/sources/{sourceId}`**
- Operation: `findById`
- Summary: Returns a data source by id
- Description: Requires READ permission on the source
- Parameters: sourceId (in path), sourceId (in path), suppressWarnings (in query), warningTags (in query)

**`PUT /api/sources/{sourceId}`**
- Operation: `createOrUpdate`
- Summary: Updates or creates a source
- Description: Requires WRITE permission on the source for updating and CREATE_SOURCES privilege for creation
- Parameters: sourceId (in path), suppressWarnings (in query), warningTags (in query)

**`DELETE /api/sources/{sourceId}`**
- Operation: `delete_5`
- Summary: Deletes a source
- Description: Requires DELETE permission on the source
- Parameters: sourceId (in path), sourceId (in path), maxResults (in query), pageToken (in query), includeDisabled (in query), includeRestriction (in query)

### sources / cache-settings

**`GET /api/sources/{sourceId}/custom-metrics/{customMetricName}`**
- Operation: `findSourceCacheSettings`
- Summary: Returns cache settings for the data source
- Description: Requires READ permission on the source
- Parameters: sourceId (in path), sourceId (in path)

**`GET /api/sources/{sourceId}/cache-settings`**
- Operation: `findSourceCacheSettings`
- Summary: Returns cache settings for the data source
- Description: Requires READ permission on the source
- Parameters: sourceId (in path), sourceId (in path)

**`PUT /api/sources/{sourceId}/cache-settings`**
- Operation: `saveSourceCacheSettings`
- Summary: Updates cache settings for data source
- Description: Requires WRITE permission on the source
- Parameters: sourceId (in path), sourceId (in path)

### sources / custom-metrics

**`PATCH /api/sources/{sourceId}/dictionaries/{language}`**
- Operation: `update_8`
- Summary: Updates custom metric visibility
- Description: Requires WRITE permission on the source or READ permission on the source and ROLE_EDIT_FORMULAS
- Parameters: sourceId (in path), customMetricName (in path), sourceId (in path)

**`PUT /api/sources/{sourceId}/custom-metrics/{customMetricName}`**
- Operation: `update_7`
- Summary: Updates existing custom metric or creates a new one if custom metric with {customMetricName} doesn't exist
- Description: Requires WRITE permission on the source or READ permission on the source and ROLE_EDIT_FORMULAS
- Parameters: sourceId (in path), customMetricName (in path), sourceId (in path)

**`DELETE /api/sources/{sourceId}/custom-metrics/{customMetricName}`**
- Operation: `delete_8`
- Summary: Deletes a custom metric
- Description: Requires WRITE permission on the source or READ permission on the source and ROLE_EDIT_FORMULAS
- Parameters: sourceId (in path), customMetricName (in path), sourceId (in path), customMetricName (in path)

**`PATCH /api/sources/{sourceId}/custom-metrics/{customMetricName}`**
- Operation: `update_8`
- Summary: Updates custom metric visibility
- Description: Requires WRITE permission on the source or READ permission on the source and ROLE_EDIT_FORMULAS
- Parameters: sourceId (in path), customMetricName (in path), sourceId (in path)

### sources / dictionaries

**`GET /api/sources/{sourceId}/dictionaries`**
- Operation: `getDictionaries`
- Summary: Returns a list of source dictionaries
- Description: OK
- Parameters: sourceId (in path), sourceId (in path), sourceId (in path), sourceId (in path), language (in path)

**`PUT /api/sources/{sourceId}/dictionaries`**
- Operation: `bulkSave`
- Summary: Bulk create or update from file with replace all source dictionaries
- Description: File must have specific structure:\n\n``` \n\nField Label,languageLocaleId1,languageLocaleId2 \n\nfieldLabel1,labelTranslate1,labelTranslate2\n\n ```
- Parameters: sourceId (in path), sourceId (in path), sourceId (in path), language (in path), sourceId (in path), language (in path)

**`DELETE /api/sources/{sourceId}/dictionaries`**
- Operation: `delete_7`
- Summary: Delete all source dictionaries
- Description: No Content
- Parameters: sourceId (in path), sourceId (in path), language (in path), sourceId (in path), language (in path), sourceId (in path), language (in path)

**`GET /api/sources/{sourceId}/dictionaries/{language}`**
- Operation: `findByLanguage`
- Summary: Read source dictionary by language
- Description: OK
- Parameters: sourceId (in path), language (in path), sourceId (in path), language (in path), sourceId (in path), language (in path), sourceId (in path), customMetricName (in path)

**`PUT /api/sources/{sourceId}/dictionaries/{language}`**
- Operation: `save`
- Summary: Create or update source dictionary by language
- Description: OK
- Parameters: sourceId (in path), language (in path), sourceId (in path), language (in path), sourceId (in path), customMetricName (in path)

**`DELETE /api/sources/{sourceId}/dictionaries/{language}`**
- Operation: `deleteByLanguage`
- Summary: Delete source dictionary by language
- Description: No Content
- Parameters: sourceId (in path), language (in path), sourceId (in path), customMetricName (in path)

### sources / fields

**`GET /api/sources/{sourceId}/fields`**
- Operation: `list`
- Summary: Returns a list of fields for the source
- Description: Requires READ permission on the source
- Parameters: sourceId (in path), maxResults (in query), pageToken (in query), sourceId (in path), suppressWarnings (in query), warningTags (in query)

**`POST /api/sources/{sourceId}/fields`**
- Operation: `create`
- Summary: Creates a data source field
- Description: Requires WRITE permission on the source or READ permission on the source and ROLE_EDIT_FORMULAS for derived field creation
- Parameters: sourceId (in path), suppressWarnings (in query), sourceId (in path), fieldName (in path)

**`PUT /api/sources/{sourceId}/fields`**
- Operation: `update_4`
- Summary: Updates a data source fields (requires WRITE permission to the source)
- Description: The response to this API endpoint may return a validation error with a list of problems. Each problem has a level (ERROR, WARNING). Passing suppressWarnings=true will suppress all warnings and the request will succeed if there are no errors
- Parameters: sourceId (in path), suppressWarnings (in query), warningTags (in query)

**`GET /api/sources/{sourceId}/fields/{fieldName}`**
- Operation: `get_2`
- Summary: Returns a data source field by name
- Description: Requires READ permission on the source
- Parameters: sourceId (in path), fieldName (in path), sourceId (in path), fieldName (in path), suppressWarnings (in query)

**`PUT /api/sources/{sourceId}/fields/{fieldName}`**
- Operation: `update_5`
- Summary: Updates or creates a data source field
- Description: Requires WRITE permission on the source or READ permission on the source and ROLE_EDIT_FORMULAS for derived field editing
- Parameters: sourceId (in path), fieldName (in path), suppressWarnings (in query), warningTags (in query)

**`DELETE /api/sources/{sourceId}/fields/{fieldName}`**
- Operation: `delete_6`
- Summary: Deletes a data source field by name
- Description: Requires WRITE permission on the source
- Parameters: sourceId (in path), fieldName (in path), suppressWarnings (in query), warningTags (in query)

### sources / global-settings

**`GET /api/sources/{sourceId}/security/filters/{id}`**
- Operation: `findSourceGlobalSettings`
- Summary: Returns global settings for the data source
- Description: Requires READ or DATA_ACCESS permission on the source
- Parameters: sourceId (in path), sourceId (in path)

**`GET /api/sources/{sourceId}/security/custom-metrics/{id}`**
- Operation: `findSourceGlobalSettings`
- Summary: Returns global settings for the data source
- Description: Requires READ or DATA_ACCESS permission on the source
- Parameters: sourceId (in path), sourceId (in path)

**`GET /api/sources/{sourceId}/security/attributes/{id}`**
- Operation: `findSourceGlobalSettings`
- Summary: Returns global settings for the data source
- Description: Requires READ or DATA_ACCESS permission on the source
- Parameters: sourceId (in path), sourceId (in path)

**`GET /api/sources/{sourceId}/security/fields/{id}`**
- Operation: `findSourceGlobalSettings`
- Summary: Returns global settings for the data source
- Description: Requires READ or DATA_ACCESS permission on the source
- Parameters: sourceId (in path), sourceId (in path)

**`GET /api/sources/{sourceId}/global-settings`**
- Operation: `findSourceGlobalSettings`
- Summary: Returns global settings for the data source
- Description: Requires READ or DATA_ACCESS permission on the source
- Parameters: sourceId (in path), sourceId (in path)

**`PUT /api/sources/{sourceId}/global-settings`**
- Operation: `updateSourceGlobalSettings`
- Summary: Updates global settings for the data source
- Description: Requires WRITE permission on the source
- Parameters: sourceId (in path), sourceId (in path), maxResults (in query), pageToken (in query)

### sources / security

**`GET /api/sources/{sourceId}/security`**
- Operation: `getSourceSecuritySettings`
- Summary: (experimental) Returns source security settings
- Description: OK
- Parameters: sourceId (in path), sourceId (in path), sourceId (in path), id (in path), sourceId (in path), id (in path)

**`PUT /api/sources/{sourceId}/security`**
- Operation: `updateSourceSecuritySettings`
- Summary: (experimental) Updates source security settings
- Description: OK
- Parameters: sourceId (in path), sourceId (in path), id (in path), sourceId (in path), id (in path), sourceId (in path), id (in path)

### sources / security / custom metrics

**`PUT /api/sources/{sourceId}/security/custom-metrics/{id}`**
- Operation: `updateAttributeSettings`
- Summary: (experimental) Update custom metric security setting
- Description: OK
- Parameters: sourceId (in path), id (in path), sourceId (in path), id (in path), sourceId (in path), id (in path), sourceId (in path), id (in path)

**`DELETE /api/sources/{sourceId}/security/custom-metrics/{id}`**
- Operation: `deleteAttributeSetting`
- Summary: (experimental) Delete custom metric security setting
- Description: No Content
- Parameters: sourceId (in path), id (in path), sourceId (in path), id (in path), sourceId (in path), id (in path), sourceId (in path), id (in path)

### sources / security / fields

**`PUT /api/sources/{sourceId}/security/attributes/{id}`**
- Operation: `updateAttributeSettings_1`
- Summary: Update SecurityAttributeSetting
- Description: OK
- Parameters: sourceId (in path), id (in path), sourceId (in path), id (in path), sourceId (in path), id (in path), sourceId (in path), id (in path)

**`DELETE /api/sources/{sourceId}/security/attributes/{id}`**
- Operation: `deleteAttributeSetting_1`
- Summary: Delete SecurityAttributeSetting
- Description: No Content
- Parameters: sourceId (in path), id (in path), sourceId (in path), id (in path), sourceId (in path), id (in path), sourceId (in path)

**`PUT /api/sources/{sourceId}/security/fields/{id}`**
- Operation: `updateAttributeSettings_2`
- Summary: Update SecurityAttributeSetting
- Description: OK
- Parameters: sourceId (in path), id (in path), sourceId (in path), id (in path), sourceId (in path)

**`DELETE /api/sources/{sourceId}/security/fields/{id}`**
- Operation: `deleteAttributeSetting_2`
- Summary: Delete SecurityAttributeSetting
- Description: No Content
- Parameters: sourceId (in path), id (in path), sourceId (in path), sourceId (in path)

### sources / security / row

**`DELETE /api/sources/{sourceId}/unique-key`**
- Operation: `deleteFilter`
- Summary: Delete forced filter by id
- Description: No Content
- Parameters: sourceId (in path), id (in path), sourceId (in path), id (in path), sourceId (in path), id (in path), sourceId (in path), id (in path)

**`PATCH /api/sources/{sourceId}/unique-key`**
- Operation: `updateSourcePatch`
- Summary: Update forced filter partially
- Description: OK
- Parameters: sourceId (in path), id (in path), sourceId (in path), id (in path), sourceId (in path), id (in path), sourceId (in path), id (in path)

**`DELETE /api/sources/{sourceId}/security`**
- Operation: `deleteFilter`
- Summary: Delete forced filter by id
- Description: No Content
- Parameters: sourceId (in path), id (in path), sourceId (in path), id (in path), sourceId (in path), id (in path), sourceId (in path), id (in path)

**`PATCH /api/sources/{sourceId}/security`**
- Operation: `updateSourcePatch`
- Summary: Update forced filter partially
- Description: OK
- Parameters: sourceId (in path), id (in path), sourceId (in path), id (in path), sourceId (in path), id (in path), sourceId (in path), id (in path)

**`PUT /api/sources/{sourceId}/security/filters/{id}`**
- Operation: `updateFilter`
- Summary: Update forced filter, replacing it completely
- Description: OK
- Parameters: sourceId (in path), id (in path), sourceId (in path), id (in path), sourceId (in path), id (in path), sourceId (in path), id (in path)

**`DELETE /api/sources/{sourceId}/security/filters/{id}`**
- Operation: `deleteFilter`
- Summary: Delete forced filter by id
- Description: No Content
- Parameters: sourceId (in path), id (in path), sourceId (in path), id (in path), sourceId (in path), id (in path), sourceId (in path), id (in path)

**`PATCH /api/sources/{sourceId}/security/filters/{id}`**
- Operation: `updateSourcePatch`
- Summary: Update forced filter partially
- Description: OK
- Parameters: sourceId (in path), id (in path), sourceId (in path), id (in path), sourceId (in path), id (in path), sourceId (in path), id (in path)

### sources / unique-key

**`GET /api/sources/{sourceId}/unique-key`**
- Operation: `getUniqueKey`
- Summary: Returns unique key for the data source
- Description: Requires READ permission on the source
- Parameters: sourceId (in path), sourceId (in path)

**`PUT /api/sources/{sourceId}/unique-key`**
- Operation: `updateUniqueKey`
- Summary: Updates unique key for the data source
- Description: Requires WRITE permission on the source
- Parameters: sourceId (in path), sourceId (in path), sourceId (in path)

### sources / visual-types

**`GET /api/sources/{sourceId}/visual-types`**
- Operation: `listVisualTypesForSource`
- Summary: Returns visual types for the data source
- Description: Requires READ or DATA_ACCESS permission on the source
- Parameters: sourceId (in path), maxResults (in query), pageToken (in query), includeDisabled (in query), includeRestriction (in query), sourceId (in path)

**`PUT /api/sources/{sourceId}/visual-types`**
- Operation: `update_3`
- Summary: Updates source visual types
- Description: Requires WRITE permission on the source
- Parameters: sourceId (in path), sourceId (in path)

### toggle

**`GET /api/uploads/{id}/data`**
- Operation: `getByPrefixAndKey`
- Summary: Get variable by prefix and key
- Description: OK
- Parameters: prefix (in path), key (in path), prefix (in path), key (in path), prefix (in path), key (in path), activityType (in path)

**`GET /api/toggles/{prefix}/{key}`**
- Operation: `getByPrefixAndKey`
- Summary: Get variable by prefix and key
- Description: OK
- Parameters: prefix (in path), key (in path), prefix (in path), key (in path), prefix (in path), key (in path), activityType (in path)

**`PUT /api/toggles/{prefix}/{key}`**
- Operation: `setByPrefixAndKey`
- Summary: Set variable by prefix and key
- Description: Supervisor authority is required to access this endpoint
- Parameters: prefix (in path), key (in path), prefix (in path), key (in path), activityType (in path), activityType (in path)

**`DELETE /api/toggles/{prefix}/{key}`**
- Operation: `deleteByPrefixAndKey`
- Summary: Delete variable by prefix and key
- Description: Supervisor authority is required to access this endpoint
- Parameters: prefix (in path), key (in path), activityType (in path), activityType (in path), sourceId (in path)

### uploads

**`GET /api/uploads/{id}`**
- Operation: `read`
- Summary: Returns an upload by id
- Description: Requires READ permission to the upload
- Parameters: id (in path), id (in path)

**`POST /api/uploads/{id}`**
- Operation: `appendData`
- Summary: Appends data to the upload
- Description: Requires MANAGE_CONNECTIONS or MANAGE_FILE_UPLOADS role
- Parameters: id (in path), id (in path)

**`PUT /api/uploads/{id}`**
- Operation: `update_2`
- Summary: Updates uploads
- Description: Requires MANAGE_CONNECTIONS or MANAGE_FILE_UPLOADS role
- Parameters: id (in path), id (in path)

**`DELETE /api/uploads/{id}`**
- Operation: `delete_4`
- Summary: Deletes an upload
- Description: Requires MANAGE_CONNECTIONS or MANAGE_FILE_UPLOADS role
- Parameters: id (in path), id (in path)

**`POST /api/uploads/{id}/data`**
- Operation: `appendData`
- Summary: Appends data to the upload
- Description: Requires MANAGE_CONNECTIONS or MANAGE_FILE_UPLOADS role
- Parameters: id (in path), id (in path)

**`PUT /api/uploads/{id}/data`**
- Operation: `replaceData`
- Summary: Replaces upload data
- Description: Requires MANAGE_CONNECTIONS or MANAGE_FILE_UPLOADS role
- Parameters: id (in path), id (in path)

**`DELETE /api/uploads/{id}/data`**
- Operation: `clearData`
- Summary: Deletes upload data
- Description: Requires MANAGE_CONNECTIONS or MANAGE_FILE_UPLOADS role
- Parameters: id (in path), prefix (in path), key (in path), prefix (in path), key (in path), prefix (in path)

### users

**`GET /api/users/{id}`**
- Operation: `getUser`
- Summary: Load user
- Description: OK
- Parameters: id (in path), id (in path), id (in path), sid (in path)

**`PUT /api/users/{id}`**
- Operation: `updateUser`
- Summary: Update user
- Description: Supervisor authority or role Administer Users is required to access this endpoint
- Parameters: id (in path), id (in path), sid (in path), sid (in path)

**`DELETE /api/users/{id}`**
- Operation: `delete_2`
- Summary: Delete user
- Description: Supervisor authority or role Administer Users is required to access this endpoint
- Parameters: id (in path), sid (in path), sid (in path)

### users segregation

**`GET /api/users/permissions/{sid}`**
- Operation: `get_1`
- Summary: Get the conditions for user segregation in the account
- Description: Successful operation
- Parameters: sid (in path), sid (in path)

**`PUT /api/users/permissions/{sid}`**
- Operation: `update_1`
- Summary: Update the conditions for user segregation in the account
- Description: The permissions on condition were updated
- Parameters: sid (in path), sid (in path)

**`DELETE /api/users/permissions/{sid}`**
- Operation: `delete_3`
- Summary: Delete the conditions for user segregation in the account
- Description: The user must be logged in
- Parameters: sid (in path), id (in path), id (in path)

### visual-types

**`GET /api/visuals/{id}/acls/bulk`**
- Operation: `getVisualType`
- Summary: Get Visual Type by id
- Description: OK
- Parameters: id (in path), componentBody (in query), id (in path), id (in path), id (in path), id (in path)

**`DELETE /api/visuals/{id}/acls/bulk`**
- Operation: `delete_1`
- Summary: Delete Visual Type
- Description: No Content
- Parameters: id (in path), id (in path), id (in path), id (in path), sid (in path)

**`GET /api/visual-types/{id}`**
- Operation: `getVisualType`
- Summary: Get Visual Type by id
- Description: OK
- Parameters: id (in path), componentBody (in query), id (in path), id (in path), id (in path), id (in path)

**`PUT /api/visual-types/{id}`**
- Operation: `updateVis`
- Summary: Update Visual Type
- Description: No Content
- Parameters: id (in path), id (in path), id (in path), id (in path), id (in path), sid (in path)

**`DELETE /api/visual-types/{id}`**
- Operation: `delete_1`
- Summary: Delete Visual Type
- Description: No Content
- Parameters: id (in path), id (in path), id (in path), id (in path), sid (in path)

### visuals

**`GET /api/visuals/{id}`**
- Operation: `get`
- Summary: Retrieve a visual (requires READ permission to the visual)
- Description: Returns a visual specified by id
- Parameters: id (in path), id (in path), suppressWarnings (in query), warningTags (in query)

**`PUT /api/visuals/{id}`**
- Operation: `update`
- Summary: Updates a visual (requires WRITE permission to the visual) or creates a new visual with custom id (requires the ROLE_CREATE_VISUALS privilege)
- Description: Defines a visual identifier
- Parameters: id (in path), suppressWarnings (in query), warningTags (in query)

**`DELETE /api/visuals/{id}`**
- Operation: `delete`
- Summary: Deletes a visual (requires DELETE permission to the visual)
- Description: Defines a visual identifier
- Parameters: id (in path), id (in path), id (in path)

## Raw Spec Location

The full (truncated) OpenAPI 3.1 JSON spec is saved at:
`/sessions/serene-festive-faraday/mnt/.auto-memory/logi_composer_api_spec_raw.json`

To get the complete spec, fetch: `https://uat.logi-symphony.com/discovery/api-docs`