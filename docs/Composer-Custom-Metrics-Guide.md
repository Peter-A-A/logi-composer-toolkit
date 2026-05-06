# Logi Composer Custom Metrics — Instructions for Claude

Use these instructions when creating, updating, or managing custom metrics on Logi Composer data sources via the REST API.

## What custom metrics are

Custom metrics are calculated fields defined on a Composer data source. They let you create ratios, filtered aggregations, period comparisons, and other derived measures without modifying the underlying database. Custom metrics are computed at query time and respect whatever GROUP BY / filters the visual applies, so a single definition works at any level of granularity.

Every source gets a default custom metric called **Volume** (`count(*)`) automatically. You can reference existing custom metrics inside new ones.

## API endpoint

```
PUT /api/sources/{sourceId}/custom-metrics/{customMetricName}
```

This creates a new custom metric or updates an existing one.

**Required headers:** `Content-Type: application/vnd.composer.v3+json` (this is critical — `application/json` returns a 415 error).

**Path parameters:**
- `sourceId` — the Composer source ID (lowercase, dashes allowed, max 36 chars)
- `customMetricName` — the metric's internal name (use snake_case, e.g. `conversion_rate`)

**Request body (JSON):**

```json
{
  "label": "Conversion Rate",
  "expression": "sum(ad_orders) / sum(clicks)",
  "dataType": "NUMBER"
}
```

**Body fields:**
- `label` (string, required) — display name shown in the UI
- `expression` (string, required) — the calculation formula (see syntax below)
- `dataType` (string, required) — always `"NUMBER"` for numeric metrics

**Do NOT include** `format`, `numberFormat`, or `visible` in the request body — these are set automatically by Composer and including them causes a 400 error.

**Successful response (201 Created):**

```json
{
  "name": "conversion_rate",
  "label": "Conversion Rate",
  "visible": true,
  "numberFormat": {
    "type": "PLAIN",
    "decimals": 2,
    "separator": true,
    "negative": "SIGNED",
    "standardUnit": "NONE"
  },
  "expression": "sum(ad_orders) / sum(clicks)",
  "dataType": "NUMBER"
}
```

## Other custom metric endpoints

**Get:** `GET /api/sources/{sourceId}/custom-metrics/{customMetricName}`

**Delete:** `DELETE /api/sources/{sourceId}/custom-metrics/{customMetricName}`

**Patch (visibility only):** `PATCH /api/sources/{sourceId}/custom-metrics/{customMetricName}`

## Expression syntax

Custom metric expressions use aggregation functions applied to source field names (the `name` property of the field, not the label). Fields are referenced by their internal field name as it appears in the source definition.

### Aggregation functions

| Function | Description | Example |
|---|---|---|
| `sum(field)` | Sum of values | `sum(revenue)` |
| `avg(field)` | Average | `avg(unit_price)` |
| `min(field)` | Minimum value | `min(order_date)` |
| `max(field)` | Maximum value | `max(ad_spend_eur)` |
| `count(*)` | Count of all rows | `count(*)` |
| `count(field)` | Count of non-null values | `count(order_id)` |
| `distinct_count(field)` | Count of distinct values | `distinct_count(product_id)` |
| `last_value(field)` | Last value by time | `last_value(status)` |

### Arithmetic operators

Use standard arithmetic between aggregated values: `+`, `-`, `*`, `/`

Division by zero returns null — Composer handles this gracefully in visuals.

### WHERE clause (filtered aggregations)

Apply filters within an aggregation using `WHERE`:

```
sum(revenue) WHERE is_ad_attributed = true
```

```
count(*) WHERE campaign_type IN ('Sponsored Product', 'Sponsored Brand')
```

```
sum(total_fatal_injuries) WHERE event_year >= 2020
```

### TRANSFORM clause (time comparisons)

Use `TRANSFORM` with time functions for period-over-period calculations:

```
sum(revenue) - (sum(revenue) TRANSFORM order_date = PreviousPeriod())
```

This computes the difference between current period and previous period revenue.

### Combining expressions

You can combine multiple aggregations, filters, and arithmetic:

```
sum(ad_orders) / sum(clicks)
```

```
(sum(revenue) WHERE is_ad_attributed = true) / sum(ad_spend_eur)
```

```
sum(profit) / (sum(sales) WHERE zipcode IN (90210, 94107, 92101))
```

### Referencing other custom metrics

You can reference an existing custom metric by its internal name:

```
conversion_rate * 100
```

## Common patterns for business metrics

### Ratio metrics (rate, percentage, efficiency)

```
expression: "sum(numerator_field) / sum(denominator_field)"
```

Examples:
- **Conversion Rate:** `sum(ad_orders) / sum(clicks)`
- **ROAS:** `sum(ad_revenue_eur) / sum(ad_spend_eur)`
- **Yield Rate:** `sum(good_units) / (sum(good_units) + sum(rejected_units))`

### Filtered ratio metrics

```
expression: "(sum(revenue) WHERE is_ad_attributed = true) / sum(ad_spend_eur)"
```

### Period-over-period change

```
expression: "sum(revenue) - (sum(revenue) TRANSFORM order_date = PreviousPeriod())"
```

### Percentage of total

```
expression: "sum(revenue) / sum(revenue) WHERE category = 'Electronics'"
```

## MCP tool usage pattern

When using the Logi Composer MCP server, call `update_source_custom_metrics` with:

```
sourceId: "your-source-id"
customMetricName: "metric_snake_case_name"
body: {
  "label": "Human Readable Label",
  "expression": "sum(field_a) / sum(field_b)",
  "dataType": "NUMBER"
}
```

### Step-by-step workflow

1. **Identify the source** — use `composer_api_request` with `GET /api/sources` to find the source ID
2. **Check available fields** — use `get_source_fields` to see field names you can reference in expressions
3. **Create the metric** — use `update_source_custom_metrics` with the expression
4. **Verify** — use `composer_api_request` with `GET /api/sources/{sourceId}/custom-metrics/{name}` to confirm creation

### Naming conventions

- `customMetricName` (path parameter): use `snake_case`, lowercase, no spaces (e.g. `conversion_rate`, `roas`, `sales_per_click`)
- `label` (body field): use title case with spaces for display (e.g. `"Conversion Rate"`, `"ROAS"`, `"Sales per Click"`)
- Field references in expressions: use the field's `name` property from the source definition, not the `label`

### Important notes

- The `Content-Type` header MUST be `application/vnd.composer.v3+json` — the standard `application/json` will return HTTP 415
- The `sourceId` must follow Composer's ID format: max 36 chars, lowercase letters, numbers, or dashes only, no underscores, cannot start or end with a dash
- Do not include `format`, `numberFormat`, `visible`, or any fields beyond `label`, `expression`, and `dataType` in the request body — extra fields cause HTTP 400 errors
- `dataType` should always be `"NUMBER"` for calculated metrics
- Expressions use field names (the `name` property), not labels — e.g. use `ad_spend_eur` not `Ad Spend Eur`

## Worked example

Given a source `opc-view-c-combined-metrics` with fields: `clicks`, `impressions`, `ad_spend_eur`, `ad_orders`, `ad_revenue_eur`, `total_revenue_eur`, `total_orders`

**Creating three business metrics:**

```
PUT /api/sources/opc-view-c-combined-metrics/custom-metrics/conversion_rate
Body: {"label": "Conversion Rate", "expression": "sum(ad_orders) / sum(clicks)", "dataType": "NUMBER"}

PUT /api/sources/opc-view-c-combined-metrics/custom-metrics/roas
Body: {"label": "ROAS", "expression": "sum(ad_revenue_eur) / sum(ad_spend_eur)", "dataType": "NUMBER"}

PUT /api/sources/opc-view-c-combined-metrics/custom-metrics/sales_per_click
Body: {"label": "Sales per Click", "expression": "sum(total_revenue_eur) / sum(clicks)", "dataType": "NUMBER"}
```

All three return HTTP 201 with the full metric definition including auto-generated `numberFormat` settings.
