# Logi Composer Data Sources — Instructions for Claude

Use these instructions when creating, updating, or managing data sources on Logi Composer via the REST API and MCP server.

## Overview

A Composer data source defines what data is available for dashboards and visuals. A source can reference a single database table, a custom SQL query joining multiple tables, or multiple tables joined via Composer's built-in join feature. Each source also has global settings (e.g. timebar/date range), field definitions, and optional custom metrics.

## Critical: creating sources (POST, not PUT)

Always use `POST /api/sources` to create a new source. **Never use `PUT /api/sources/{sourceId}`** for creation, because PUT requires you to specify a `sourceId` in the path, which means you are setting the source ID yourself. Composer must generate source IDs automatically — they use a hex format like `69fa8e090b70396702eb9e59`.

When using the MCP server, this means using the `composer_api_request` tool with `method: "POST"` and `path: "/api/sources"` rather than the `update_sources` tool (which maps to PUT).

### Error: setting source IDs manually

If you use `PUT /api/sources/my-custom-id`, the source will be created with the ID `my-custom-id` instead of a Composer-generated hex ID. This causes problems because the ID format doesn't match what the system expects, and the source may not behave correctly in the UI. Always let Composer generate the ID by using POST.

## MCP server issues that need fixing

### Issue 1: Content-Type header

The MCP server's `_headers()` function (around line 47 of `server.py`) currently sets:

```python
headers["Content-Type"] = "application/json"
```

The Composer API requires:

```python
headers["Content-Type"] = "application/vnd.composer.v3+json"
```

Using `application/json` causes **HTTP 415 Unsupported Media Type** errors on all POST/PUT/PATCH requests. This is the most common error when working with the MCP server and must be fixed before any write operations will succeed.

### Issue 2: no POST endpoint for source creation

The MCP server auto-generates tools from the OpenAPI spec. The `update_sources` tool maps to `PUT /api/sources/{sourceId}`, which requires a source ID in the path. There is no dedicated tool for `POST /api/sources` (creating a source without specifying an ID).

The workaround is to use the generic `composer_api_request` tool:

```
method: "POST"
path: "/api/sources"
body: { ... source definition ... }
```

Ideally, the MCP server should be updated to include a `create_source` tool that maps to `POST /api/sources`.

### Issue 3: the `entities` shorthand format

Composer's documentation shows a simplified payload format using a top-level `entities` array:

```json
{
  "name": "Source Name",
  "entities": [
    {
      "name": "entity_name",
      "connectionId": "abc123",
      "schema": "public",
      "collection": "my_table"
    }
  ]
}
```

This format does **not** work when the MCP server passes the body directly to the REST API. The API returns **HTTP 500** with the error:

```
Cannot invoke "com.zoomdata.resource.source.SourceStorageResource.getDataEntities()"
because the return value of "com.zoomdata.resource.source.SourceResource.getStorage()" is null
```

The `entities` shorthand is likely transformed by a higher-level gateway or UI layer before reaching the REST API. When calling the API directly (as the MCP server does), you must use the full `storage.dataEntities` format instead. See "Request body formats" below.

The MCP server could be updated to accept the simpler `entities` format and automatically transform it into the `storage.dataEntities` structure before sending to the API.

## Request body formats

### Single-entity source with custom SQL

Use this when you want to join tables in SQL yourself, or when pointing at a database view.

```json
{
  "name": "My Source Name",
  "storage": {
    "dataEntities": [
      {
        "name": "entity_name",
        "type": "CUSTOM_SQL",
        "customSql": {
          "connectionId": "679a5aa3796b327bb74e403e",
          "sql": "SELECT t.*, d.label FROM schema.fact_table t JOIN schema.dim_table d ON d.id = t.dim_id"
        }
      }
    ]
  },
  "folderId": "69c3780f0b70396702e7de66"
}
```

**Important:** The SQL field inside `customSql` is called `sql`, not `query`. Using `query` returns:

```
HTTP 400: Unrecognized field "storage.dataEntities.null.customSql.query"
```

For single-entity sources, you do **not** need to set an `id` field on the data entity. Composer will auto-assign the entity ID from the `name` field.

### Multi-entity source with built-in table joins

Use this when you want Composer to handle the join rather than writing SQL. Each table is a separate `SINGLE_COLLECTION` entity, and joins are defined in `joinsInfo`.

```json
{
  "name": "My Joined Source",
  "storage": {
    "dataEntities": [
      {
        "id": "fact-orders",
        "name": "fact_orders",
        "type": "SINGLE_COLLECTION",
        "singleCollection": {
          "connectionId": "679a5aa3796b327bb74e403e",
          "schema": "opc",
          "collection": "fact_orders",
          "parameters": {}
        }
      },
      {
        "id": "dim-campaign",
        "name": "dim_campaign",
        "type": "SINGLE_COLLECTION",
        "singleCollection": {
          "connectionId": "679a5aa3796b327bb74e403e",
          "schema": "opc",
          "collection": "dim_campaign",
          "parameters": {}
        }
      }
    ]
  },
  "joinsInfo": [
    {
      "leftEntityName": "fact_orders",
      "rightEntityName": "dim_campaign",
      "type": "INNER",
      "conditions": [
        {
          "leftFieldName": "campaign_id",
          "rightFieldName": "campaign_id"
        }
      ]
    }
  ],
  "folderId": "69c3780f0b70396702e7de66"
}
```

**Key rules for multi-entity (fusion) sources:**

1. **Entity IDs are required.** Unlike single-entity sources, each entity in a fusion source must have a unique `id` field. Without it, the API returns:
   ```
   HTTP 400: All fusion source data entities should contain unique id
   ```

2. **`joinsInfo` is at the top level.** It sits alongside `storage`, not inside it. Placing it inside `storage` returns:
   ```
   HTTP 400: Unrecognized field "storage.joinsInfo"
   ```

3. **`joinsInfo` references entities by `name`, not `id`.** The `leftEntityName` and `rightEntityName` fields match the `name` property of each data entity.

4. **Entity type must be `SINGLE_COLLECTION`**, not `TABLE`. Using `TABLE` returns:
   ```
   HTTP 400: Unknown data entity type: 'TABLE'
   ```

5. **`SINGLE_COLLECTION` requires a nested config block** called `singleCollection` containing `connectionId`, `schema`, `collection`, and `parameters`.

6. **Duplicate field names are auto-renamed.** When two entities share a column name (e.g. both have `campaign_id`), Composer renames the second occurrence by appending `_1` (e.g. `campaign_id_1`).

7. **Multiple joins are supported.** Add multiple entries to the `joinsInfo` array to join three or more tables (e.g. fact table to two dimension tables).

## Source ID format rules

When using PUT (which should be avoided for creation), the `sourceId` must follow these rules:
- Maximum 36 characters
- Lowercase letters, numbers, and dashes only
- No underscores (causes HTTP 400: "Value should be valid custom ID format")
- Cannot start or end with a dash
- No consecutive dashes

These rules do not apply when using POST, since Composer generates the ID automatically.

## Global settings (timebar / date range)

After creating a source, set the global datetime range using:

```
PUT /api/sources/{sourceId}/global-settings
```

Or via the MCP tool `update_source_global_settings`.

### Request body

```json
{
  "timebar": {
    "enabled": true,
    "from": "+$start_of_data",
    "to": "+$end_of_data",
    "timeField": "event_date"
  }
}
```

**Fields:**
- `enabled` (boolean) — whether the timebar is active
- `from` / `to` (string) — date range boundaries. Use `+$start_of_data` and `+$end_of_data` for the full dataset range. Relative expressions like `+$end_of_data_-1_week` are also supported.
- `timeField` (string) — the name of the TIME field in the source to filter on (e.g. `event_date`, `order_date`, `dt`)

### Response

```json
{
  "textSearchEnabled": false,
  "nestedFiltersEnabled": true,
  "timebar": {
    "enabled": true,
    "from": "+$start_of_data",
    "to": "+$end_of_data",
    "timeField": "dt",
    "sharpening": { "enabled": false },
    "player": { "enabled": false }
  },
  "defaultVisualFilters": []
}
```

## Step-by-step workflow

### Creating a custom SQL source

1. **Identify the connection** — use `composer_api_request` with `GET /api/connections` to find the connection ID for your database
2. **Create the source** — use `composer_api_request` with `POST /api/sources` and the CUSTOM_SQL entity format. Do not set a source ID.
3. **Note the returned ID** — the response includes the Composer-generated `id` (hex format). Use this for all subsequent operations.
4. **Set the timebar** — use `update_source_global_settings` with the Composer-generated source ID
5. **Add custom metrics** (if needed) — use `update_source_custom_metrics` (see the Composer Custom Metrics instructions file for details)
6. **Verify** — use `get_sources` with the Composer-generated ID to confirm

### Creating a table join source

1. **Identify the connection** — same as above
2. **Create the source** — use `composer_api_request` with `POST /api/sources` and the SINGLE_COLLECTION entity format with `joinsInfo`. Entity IDs are required. Do not set a source ID.
3. **Note the returned ID** — use for subsequent operations
4. **Set the timebar** — same as above
5. **Verify** — same as above

## Error reference

| Error | Cause | Fix |
|---|---|---|
| HTTP 415 Unsupported Media Type | MCP server sends `Content-Type: application/json` | Change `_headers()` to use `application/vnd.composer.v3+json` |
| HTTP 500 "storage is null" | Used `entities` shorthand instead of `storage.dataEntities` | Use full `storage.dataEntities` format with `type` and nested config |
| HTTP 400 "Unrecognized field customSql.query" | Used `query` inside `customSql` | Use `sql` instead of `query` |
| HTTP 400 "Unknown data entity type: TABLE" | Used `type: "TABLE"` | Use `type: "SINGLE_COLLECTION"` with `singleCollection` config |
| HTTP 400 "Unrecognized field storage.joinsInfo" | Placed `joinsInfo` inside `storage` | Move `joinsInfo` to the top level of the request body |
| HTTP 400 "All fusion source data entities should contain unique id" | Multi-entity source missing entity `id` fields | Add a unique `id` to each entity in a fusion source |
| HTTP 400 "Value should be valid custom ID format" | Used underscores or invalid chars in sourceId (via PUT) | Use dashes instead of underscores, or use POST to let Composer generate the ID |
| HTTP 400 "Unrecognized field format" (custom metrics) | Included `format`, `numberFormat`, or `visible` in custom metric body | Only include `label`, `expression`, and `dataType` |
| Source ID is a slug instead of hex | Used PUT with a custom sourceId | Use POST to let Composer generate the ID automatically |

## Worked example

Given a Supabase database with schema `opc`, connection `679a5aa3796b327bb74e403e`, and tables `fact_ad_events`, `fact_orders`, `dim_campaign`, `dim_product`, and view `v_combined_metrics`:

**Creating three custom SQL sources and one table join source:**

```
POST /api/sources

# Source 1 — Ad performance (custom SQL)
Body: {
  "name": "OPC View A — Ad Performance",
  "storage": {
    "dataEntities": [{
      "name": "ad_performance",
      "type": "CUSTOM_SQL",
      "customSql": {
        "connectionId": "679a5aa3796b327bb74e403e",
        "sql": "SELECT ae.*, c.campaign_name, c.campaign_type, c.partner_name, p.product_name, p.category, p.price_segment FROM opc.fact_ad_events ae JOIN opc.dim_campaign c ON c.campaign_id = ae.campaign_id JOIN opc.dim_product p ON p.product_id = ae.product_id"
      }
    }]
  },
  "folderId": "69c3780f0b70396702e7de66"
}

# Source 2 — Combined metrics (custom SQL pointing at a view)
Body: {
  "name": "OPC View C — Combined Metrics",
  "storage": {
    "dataEntities": [{
      "name": "combined_metrics",
      "type": "CUSTOM_SQL",
      "customSql": {
        "connectionId": "679a5aa3796b327bb74e403e",
        "sql": "SELECT * FROM opc.v_combined_metrics"
      }
    }]
  },
  "folderId": "69c3780f0b70396702e7de66"
}

# Source 3 — Table join (3 tables via joinsInfo)
Body: {
  "name": "OPC Ad Events + Campaigns + Products (Table Join)",
  "storage": {
    "dataEntities": [
      {
        "id": "fact-ad-events",
        "name": "fact_ad_events",
        "type": "SINGLE_COLLECTION",
        "singleCollection": {
          "connectionId": "679a5aa3796b327bb74e403e",
          "schema": "opc",
          "collection": "fact_ad_events",
          "parameters": {}
        }
      },
      {
        "id": "dim-campaign",
        "name": "dim_campaign",
        "type": "SINGLE_COLLECTION",
        "singleCollection": {
          "connectionId": "679a5aa3796b327bb74e403e",
          "schema": "opc",
          "collection": "dim_campaign",
          "parameters": {}
        }
      },
      {
        "id": "dim-product",
        "name": "dim_product",
        "type": "SINGLE_COLLECTION",
        "singleCollection": {
          "connectionId": "679a5aa3796b327bb74e403e",
          "schema": "opc",
          "collection": "dim_product",
          "parameters": {}
        }
      }
    ]
  },
  "joinsInfo": [
    {
      "leftEntityName": "fact_ad_events",
      "rightEntityName": "dim_campaign",
      "type": "INNER",
      "conditions": [{"leftFieldName": "campaign_id", "rightFieldName": "campaign_id"}]
    },
    {
      "leftEntityName": "fact_ad_events",
      "rightEntityName": "dim_product",
      "type": "INNER",
      "conditions": [{"leftFieldName": "product_id", "rightFieldName": "product_id"}]
    }
  ],
  "folderId": "69c3780f0b70396702e7de66"
}
```

All three return HTTP 200 with Composer-generated IDs and auto-detected fields.

**Setting timebar on each (using Composer-generated IDs from responses):**

```
PUT /api/sources/69fa8dfa0b70396702eb9e53/global-settings
Body: {"timebar": {"enabled": true, "from": "+$start_of_data", "to": "+$end_of_data", "timeField": "event_date"}}

PUT /api/sources/69fa8e090b70396702eb9e59/global-settings
Body: {"timebar": {"enabled": true, "from": "+$start_of_data", "to": "+$end_of_data", "timeField": "dt"}}
```

**Adding custom metrics to the combined metrics source:**

```
PUT /api/sources/69fa8e090b70396702eb9e59/custom-metrics/conversion_rate
Body: {"label": "Conversion Rate", "expression": "sum(ad_orders) / sum(clicks)", "dataType": "NUMBER"}

PUT /api/sources/69fa8e090b70396702eb9e59/custom-metrics/roas
Body: {"label": "ROAS", "expression": "sum(ad_revenue_eur) / sum(ad_spend_eur)", "dataType": "NUMBER"}
```
