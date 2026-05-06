# Logi Composer Visual Types — Instructions for Claude

Use these instructions when creating, updating, or inspecting visuals on Logi Composer via the REST API and MCP server.

## Overview

A Composer visual is a chart or widget definition linked to a data source. Each visual has a `type` (e.g. `UBER_BARS`, `DONUT`), a `visualTypeId` (hex ID referencing the visual type definition), and a `source.variables` object that configures what data to show and how.

## Creating visuals

Use `POST /api/visuals` via `composer_api_request` to create a visual. The key structure is:

```json
{
  "visualTypeId": "<hex ID from visual type definition>",
  "type": "<type string>",
  "visualName": "My Visual",
  "source": {
    "sourceId": "<data source ID>",
    "sourceName": "<data source name>",
    "variables": { ... },
    "filters": [],
    "aggregateFilters": [],
    "playbackMode": false,
    "live": false,
    "textSearchEnabled": false
  },
  "controlsCfg": {
    "timeControlCfg": {
      "from": "+$start_of_data",
      "to": "+$end_of_data",
      "timeField": "<time field name>"
    },
    "sharpeningCfg": {
      "prefer": false,
      "maxQueries": 10
    }
  }
}
```

**Important:** Always set `timeControlCfg` to full dataset range (`+$start_of_data` / `+$end_of_data`) unless the user explicitly requests a narrower range. Only include `timeControlCfg` if the source has a TIME field.

## Visual Type Reference

### UBER_BARS (Bar Chart)

- **visualTypeId:** `65659d06b5ca0667ef2bb2e4`
- **type:** `UBER_BARS`

**Required variables:**

| Variable | Type | Description |
|---|---|---|
| `Multi Group By` | array | Dimension(s) to group bars by |
| `Metric` | array | Measure(s) to aggregate |
| `Bar Color` | array | **Required** — metric for bar coloring. Usually same as Metric. Omitting this causes "You do not have access" errors on the Color slot. |
| `UberBarsSettings` | object | Chart layout settings |
| `Rulers` | object | Axis and gridline configuration |
| `Formatting` | array | Optional formatting rules |

**Example variables:**

```json
{
  "Multi Group By": [
    {
      "name": "category",
      "limit": 50,
      "sort": {
        "name": "total_revenue_eur",
        "dir": "desc",
        "label": "Total Revenue Eur",
        "type": "NUMBER",
        "metricFunc": "sum"
      },
      "type": "ATTRIBUTE",
      "label": "Category",
      "includeBlanks": false,
      "groupColorSet": "_inherit",
      "autoShowColorLegend": true,
      "colorNumb": 4,
      "autoColor": true,
      "groupColors": {}
    }
  ],
  "Metric": [
    { "name": "total_revenue_eur", "func": "sum" }
  ],
  "Bar Color": [
    { "name": "total_revenue_eur", "func": "sum" }
  ],
  "UberBarsSettings": {
    "chartType": "normal",
    "chartOrientation": "vertical",
    "thickness": 100,
    "showAbsoluteValues": true,
    "showRelativeValues": false,
    "showGroupLabels": false,
    "horizontalScroll": false,
    "verticalScroll": false,
    "labelsPosition": "outside",
    "labelsRotate": 0
  },
  "Rulers": {
    "gridlines": { "X1grid": true, "Y1grid": false, "X2grid": false, "Y2grid": false },
    "axis": [
      {
        "name": "Metric",
        "axis": "Metric",
        "fromAuto": true,
        "toAuto": true,
        "stepAuto": true,
        "logScaleEnabled": false,
        "metricsName": "Total Revenue Eur"
      }
    ],
    "reflines": []
  },
  "Formatting": []
}
```

**UberBarsSettings options:**
- `chartType`: `"normal"`, `"stacked"`, `"100_stacked"`
- `chartOrientation`: `"vertical"`, `"horizontal"`
- `showAbsoluteValues` / `showRelativeValues`: show value labels on bars
- `labelsPosition`: `"outside"`, `"inside"`

---

### BUBBLES (Packed Bubbles)

- **visualTypeId:** `65659d06b5ca0667ef2bb2e2`
- **type:** `BUBBLES`

**Required variables:**

| Variable | Type | Description |
|---|---|---|
| `Group By` | **object** (not array) | Single dimension to group bubbles by |
| `Bubble Size` | array | Metric controlling bubble size |
| `Bubble Color` | array | Metric controlling bubble color (with `colorConfig`) |
| `Formatting` | array | Optional formatting rules |

**Note:** `Group By` is an **object**, not an array — this differs from most other chart types.

**Example variables:**

```json
{
  "Group By": {
    "name": "treatment",
    "limit": 2500,
    "sort": {
      "name": "treatment",
      "dir": "asc",
      "label": "Treatment",
      "type": "ATTRIBUTE"
    },
    "type": "ATTRIBUTE",
    "label": "Treatment",
    "groupColorSet": "DefaultSequential",
    "autoShowColorLegend": false,
    "colorNumb": 2,
    "autoColor": true,
    "groupColors": {}
  },
  "Bubble Size": [
    { "name": "budget", "func": "avg" }
  ],
  "Bubble Color": [
    {
      "name": "budget",
      "func": "avg",
      "colorConfig": {
        "colorNumb": 3,
        "legendType": "palette",
        "colorSet": "_inherit",
        "autoShowColorLegend": true,
        "separateNegativeColor": false,
        "autoColor": true,
        "colorScaleType": "gradient"
      }
    }
  ],
  "Formatting": []
}
```

---

### DONUT (Pie / Donut Chart)

- **visualTypeId:** `65659d06b5ca0667ef2bb2f2`
- **type:** `DONUT`

**Required variables:**

| Variable | Type | Description |
|---|---|---|
| `Group By` | **object** (not array) | Dimension to split slices by |
| `Size` | array | Metric controlling slice size |
| `UberBarsSettings` | object | Label display settings |
| `Formatting` | array | Optional formatting rules |

**Note:** `Group By` is an **object**, not an array.

**Example variables:**

```json
{
  "Group By": {
    "name": "category",
    "limit": 10,
    "sort": {
      "name": "category",
      "dir": "asc",
      "label": "Category",
      "type": "ATTRIBUTE"
    },
    "type": "ATTRIBUTE",
    "label": "Category",
    "groupColorSet": "_inherit",
    "autoShowColorLegend": true,
    "colorNumb": 4,
    "autoColor": true,
    "groupColors": {}
  },
  "Size": [
    { "name": "total_revenue_eur", "func": "sum" }
  ],
  "UberBarsSettings": {
    "showAbsoluteValues": true,
    "showRelativeValues": true,
    "showGroupLabels": true
  },
  "Formatting": []
}
```

---

### PIE (Pie Chart)

- **visualTypeId:** `65659d06b5ca0667ef2bb2e8`
- **type:** `PIE`

Same variable structure as DONUT. The only difference is the visual rendering (no hole in the center).

---

### KPI (Key Performance Indicator)

- **visualTypeId:** `65659d06b5ca0667ef2bb2f4`
- **type:** `KPI`

**Required variables:**

| Variable | Type | Description |
|---|---|---|
| `Metric` | array | Primary metric to display |
| `Comparison Metric` | array | Secondary metric for comparison (optional but common) |
| `Comparison` | object | Comparison display settings |
| `Metrics Labels` | object | Custom labels for primary, comparison, and variance |
| `Position` | object | Text alignment |
| `Conditional Formatting` | array | Color rules for the KPI value |
| `Formatting` | array | Optional formatting rules |

**Example variables:**

```json
{
  "Metric": [
    { "name": "total_revenue_eur", "func": "sum" }
  ],
  "Comparison Metric": [
    { "name": "ad_spend_eur", "func": "sum" }
  ],
  "Comparison": {
    "mode": "value",
    "style": {
      "showVariance": true,
      "showArrowIndicators": true,
      "comparisonMetricLabel": false
    },
    "showNullAsZero": false
  },
  "Metrics Labels": {
    "primary": {
      "total_revenue_eursum": "Total Revenue"
    },
    "comparison": {
      "ad_spend_eursum": "Ad Spend"
    },
    "variance": {}
  },
  "Position": {
    "vertical": "center",
    "horizontal": "center"
  },
  "Conditional Formatting": [],
  "Formatting": []
}
```

---

### RAW_DATA_TABLE (Table)

- **visualTypeId:** `65659d06b5ca0667ef2bb2ea`
- **type:** `RAW_DATA_TABLE`

**Required variables:**

| Variable | Type | Description |
|---|---|---|
| `Columns` | array | Fields to display as columns |
| `Rows per Fetch` | number | Number of rows per page (e.g. `250`) |
| `ChartSettings` | object | Pagination and distinct settings |
| `Grouped Columns` | array | Columns to group by (usually empty) |
| `Metrics` | array | Aggregate metrics (usually empty for raw tables) |
| `Columns Sort` | array | Default sort configuration |
| `Column State` | array | Column widths, visibility, pinning |
| `Conditional Formatting` | array | Row/cell conditional formatting |
| `Formatting` | array | URL/image formatting for columns |

**Example variables (minimal):**

```json
{
  "Columns": [
    { "name": "campaign_name", "label": "Campaign Name", "type": "ATTRIBUTE" },
    { "name": "category", "label": "Category", "type": "ATTRIBUTE" },
    { "name": "total_revenue_eur", "label": "Total Revenue Eur", "type": "NUMBER" },
    { "name": "impressions", "label": "Impressions", "type": "NUMBER" }
  ],
  "Grouped Columns": [],
  "Metrics": [],
  "Rows per Fetch": 250,
  "ChartSettings": {
    "pagination": { "mode": "pagination" },
    "distinct": true
  },
  "Columns Sort": [],
  "Column State": [],
  "Conditional Formatting": [],
  "Formatting": [],
  "InteractivityState": { "profile": {} }
}
```

---

### PIVOT_TABLE (Pivot Table)

- **visualTypeId:** `65659d06b5ca0667ef2bb2e9`
- **type:** `PIVOT_TABLE`

**Required variables:**

| Variable | Type | Description |
|---|---|---|
| `Row Attributes` | array | Fields for row grouping. TIME fields need `"func": "MONTH"` etc. |
| `Column Attributes` | array | Fields for column headers |
| `Metrics` | array | Aggregate metrics |
| `Metric Direction` | string | `"Columns"` or `"Rows"` |
| `Column Limit` | number | Max columns (e.g. `4000`) |
| `Rows per Page` | number | Rows per page (e.g. `200`) |
| `Cell Limit` | number | Max cells (e.g. `1000000`) |
| `ChartSettings` | object | Freeze, totals, grouping settings |
| `Row Sorting` / `Column Sorting` / `Metric Sorting` / `Total Sorting` | arrays | Sort configuration |
| `Column Sizes` | array | Column width configuration |
| `Conditional Formatting` | array | Cell conditional formatting |
| `Formatting` | array | Optional formatting |

**Example variables (minimal):**

```json
{
  "Row Attributes": [
    { "name": "category" }
  ],
  "Column Attributes": [
    { "name": "brand" }
  ],
  "Metrics": [
    { "name": "total_revenue_eur", "func": "sum" }
  ],
  "Metric Direction": "Columns",
  "Column Limit": 4000,
  "Rows per Page": 200,
  "Cell Limit": 1000000,
  "ChartSettings": {
    "columns": {
      "freezeRows": false,
      "freezeTotals": true,
      "showTotalsColumn": false,
      "groupRepeatingRows": true,
      "showRollupLabels": true
    },
    "rows": { "showTotalsRow": true },
    "metrics": { "showSubtotal": false },
    "expanded": -1
  },
  "Row Sorting": [],
  "Column Sorting": [],
  "Metric Sorting": [],
  "Total Sorting": [],
  "Column Sizes": [],
  "Conditional Formatting": [],
  "Formatting": [],
  "InteractivityState": { "profile": {} }
}
```

---

### FLOATING_BUBBLES (Floating Bubbles / Scatter-like)

- **visualTypeId:** `65659d06b5ca0667ef2bb2f6`
- **type:** `FLOATING_BUBBLES`

**Required variables:**

| Variable | Type | Description |
|---|---|---|
| `Multi Group By` | array | Dimension(s) for grouping bubbles |
| `Size` | array | Metric for bubble size |
| `Y Axis` | array | Metric for vertical positioning |
| `Formatting` | array | Optional formatting |

**Example variables:**

```json
{
  "Multi Group By": [
    {
      "name": "category",
      "limit": 50,
      "sort": {
        "name": "category",
        "dir": "asc",
        "label": "Category",
        "type": "ATTRIBUTE"
      },
      "type": "ATTRIBUTE",
      "label": "Category",
      "includeBlanks": false,
      "groupColorSet": "DefaultQualitative",
      "autoShowColorLegend": true,
      "colorNumb": 4,
      "autoColor": true,
      "groupColors": {}
    }
  ],
  "Size": [
    { "name": "total_revenue_eur", "func": "sum" }
  ],
  "Y Axis": [
    { "name": "impressions", "func": "sum" }
  ],
  "Formatting": []
}
```

---

### HEAT_MAP (Heat Map)

- **visualTypeId:** `65659d06b5ca0667ef2bb2ef`
- **type:** `HEAT_MAP`

**Required variables:**

| Variable | Type | Description |
|---|---|---|
| `Multi Group By` | array | Two dimensions — one for rows, one for columns |
| `Color Metric` | array | Metric controlling cell color (with `colorConfig`) |
| `Show Metric Values` | boolean | Whether to display values in cells |
| `ShowMetricValues` | object | `{ "show": true }` |
| `Formatting` | array | Optional formatting |

**Example variables:**

```json
{
  "Multi Group By": [
    {
      "name": "category",
      "limit": 100,
      "sort": { "dir": "asc", "name": "category", "label": "Category", "type": "ATTRIBUTE" },
      "type": "ATTRIBUTE",
      "includeBlanks": false,
      "label": "Category",
      "groupColorSet": "DefaultSequential",
      "autoShowColorLegend": false,
      "colorNumb": 4,
      "autoColor": true,
      "groupColors": {}
    },
    {
      "name": "brand",
      "limit": 100,
      "sort": { "dir": "asc", "name": "brand", "label": "Brand", "type": "ATTRIBUTE" },
      "type": "ATTRIBUTE",
      "includeBlanks": false,
      "label": "Brand",
      "groupColorSet": "DefaultSequential",
      "autoShowColorLegend": false,
      "colorNumb": 4,
      "autoColor": true,
      "groupColors": {}
    }
  ],
  "Color Metric": [
    {
      "name": "total_revenue_eur",
      "func": "sum",
      "colorConfig": {
        "colorNumb": 2,
        "legendType": "palette",
        "colorSet": "_inherit",
        "autoShowColorLegend": true,
        "separateNegativeColor": false,
        "autoColor": true,
        "colorScaleType": "gradient"
      }
    }
  ],
  "Show Metric Values": true,
  "ShowMetricValues": { "show": true },
  "Formatting": []
}
```

---

## Visual Type ID Quick Reference

| Type | visualTypeId | Key Metric Variable | Key Color Variable |
|---|---|---|---|
| UBER_BARS | `65659d06b5ca0667ef2bb2e4` | `Metric` | `Bar Color` (required) |
| BUBBLES | `65659d06b5ca0667ef2bb2e2` | `Bubble Size` | `Bubble Color` |
| PIE | `65659d06b5ca0667ef2bb2e8` | `Size` | (uses Group By colors) |
| DONUT | `65659d06b5ca0667ef2bb2f2` | `Size` | (uses Group By colors) |
| KPI | `65659d06b5ca0667ef2bb2f4` | `Metric` | `Conditional Formatting` |
| RAW_DATA_TABLE | `65659d06b5ca0667ef2bb2ea` | `Columns` | N/A |
| PIVOT_TABLE | `65659d06b5ca0667ef2bb2e9` | `Metrics` | `Conditional Formatting` |
| FLOATING_BUBBLES | `65659d06b5ca0667ef2bb2f6` | `Size` + `Y Axis` | (uses Group By colors) |
| HEAT_MAP | `65659d06b5ca0667ef2bb2ef` | N/A | `Color Metric` |
| LINE_CHART | `65659d06b5ca0667ef2bb2e6` | `Metric` | (uses Group By colors) |
| COMBO_CHART | `65659d06b5ca0667ef2bb341` | `Metric` | (varies) |
| TREE_MAP | `65659d06b5ca0667ef2bb2ee` | `Size` | `Color Metric` |
| WORD_CLOUD | `65659d06b5ca0667ef2bb2e7` | `Size` | (uses Group By colors) |

## Common Pitfalls

1. **UBER_BARS requires `Bar Color`** — omitting it causes "You do not have access to view all of the data in this visual" errors on the Color slot. Always set it to the same metric as `Metric`.

2. **BUBBLES and DONUT use `Group By` as an object** — most other chart types use `Multi Group By` as an array. Passing an array for `Group By` on these types will fail.

3. **Color variables need `colorConfig`** — `Bubble Color` and `Color Metric` (Heat Map) require a `colorConfig` object with palette settings. Without it, the color legend may not render.

4. **`_inherit` vs named color sets** — use `"_inherit"` to follow the dashboard/theme colors, or named sets like `"DefaultSequential"`, `"DefaultQualitative"` for explicit palettes.

5. **Time control** — only include `timeControlCfg` in `controlsCfg` if the source has a TIME field. Some sources (like the wizard-demo BUBBLES example) omit it entirely.

6. **visualTypeId values are instance-specific** — the IDs listed here are for the UAT environment (`uat.logi-symphony.com`). Other Composer instances will have different IDs. Query `GET /api/visual-types` or `get_source_visual_types(sourceId=...)` to get the correct IDs for a given instance.
