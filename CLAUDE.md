# Logi Composer Toolkit — Guide for Claude

This repository is a comprehensive reference and toolset for working with Logi Composer (also called Logi Symphony), an embedded analytics platform by insightsoftware. Use this guide to navigate the repo and understand what's available.

## Who uses this

Internal insightsoftware team members working with Logi Composer — specifically the **Discovery / Visual Data Discovery (VDD)** embed layer. Do NOT reference Dundas BI managed layer concepts (Dundas view parameters, managed dashboards, managed reports). Stay within the Composer Discovery API.

## Repository Structure

```
logi-composer-toolkit/
├── CLAUDE.md                  ← You are here (start here for orientation)
├── README.md                  ← Human-readable project overview
├── docs/
│   ├── Logi-Composer-Symphony-Embedding-Reference.md   ← Embedding API reference
│   ├── Logi Composer REST API Reference.md             ← REST API endpoint reference
│   ├── Composer-Custom-Metrics-Guide.md                ← Custom metrics creation guide
│   ├── Composer-Data-Sources-Guide.md                  ← Data source creation guide (SQL, table joins, global settings)
│   ├── Composer-Visual-Types-Guide.md                  ← Visual/chart creation guide (bars, pie, KPI, table, pivot, etc.)
│   ├── Composer-Dashboards-Guide.md                    ← Dashboard creation guide (layout, cross-filtering, drill-through)
│   └── logi_composer_api_spec_raw.json                 ← Raw OpenAPI 3.1 spec (JSON)
├── examples/
│   └── composer-dashboard-embed.html                   ← Working dashboard embed example
└── mcp-server/
    ├── CLAUDE.md              ← MCP-specific guide (resource hierarchy, workflows)
    ├── README.md              ← MCP server technical reference
    ├── USER_GUIDE.md          ← Setup and usage guide for humans
    ├── server.py              ← The MCP server (133 tools)
    ├── requirements.txt       ← Python dependencies
    └── .env.example           ← Configuration template
```

## What to read and when

### "How do I embed a dashboard/visual?"
Read `docs/Logi-Composer-Symphony-Embedding-Reference.md`. This is the primary reference for:
- Setting up `embed.js` and `initComposerEmbedManager`
- Trusted Access authentication
- Embedding dashboards, visuals, and components
- Passing filter parameters (initial filters)
- Cross-visual filtering (pub/sub)
- Event listeners and context menus
- Data query objects (ZoomdataSDK)
- Custom chart controller API
- Action templates and keysets

For a working code example, see `examples/composer-dashboard-embed.html`.

### "How do I create a data source?"
Read `docs/Composer-Data-Sources-Guide.md`. This covers:
- **Prefer built-in joins over custom SQL** — when combining tables, use `SINGLE_COLLECTION` entities with `joinsInfo` rather than custom SQL JOINs. Only use custom SQL when the query requires subqueries, UNIONs, window functions, or database-specific syntax.
- Why you must use POST (not PUT) to create sources — Composer must generate the hex ID
- The full `storage.dataEntities` payload format (the `entities` shorthand does NOT work via the REST API)
- Custom SQL sources (`CUSTOM_SQL` type with `sql` field, not `query`)
- Multi-table join sources (`SINGLE_COLLECTION` type with `joinsInfo` at top level, entity `id` fields required)
- Setting global timebar/date range after creation — always default to full range (`+$start_of_data` to `+$end_of_data`)
- Complete error reference for common 400/415/500 errors
- Use the MCP tool `create_source` for POST, or `composer_api_request(method="POST", path="/api/sources", body={...})`

### "How do I create a visual / chart?"
Read `docs/Composer-Visual-Types-Guide.md`. This covers:
- POST `/api/visuals` creation structure and required fields
- Variable templates for every chart type: UBER_BARS, BUBBLES, DONUT/PIE, KPI, RAW_DATA_TABLE, PIVOT_TABLE, FLOATING_BUBBLES, HEAT_MAP
- Visual type IDs for the UAT environment (query `get_source_visual_types` for other instances)
- Common pitfalls (e.g. UBER_BARS requires `Bar Color`, BUBBLES/DONUT use `Group By` as object not array)

### "How do I create a dashboard?"
Read `docs/Composer-Dashboards-Guide.md`. This covers:
- POST `/api/dashboards` creation structure with widgets and responsive layout
- Dashboard layout system (`path`, `params` for responsive grid positioning)
- Unified time bar configuration (`unifiedBarCfgs` linking widgets to shared time controls)
- Cross-visual filtering (automatic same-source and explicit `fieldLinks` for different sources)
- Drill-through navigation (`dashboardLink` on widgets to navigate to target dashboards with filter inheritance)
- Interactivity settings (controlling export, comments, sharing features)
- Real-world examples: simple 2-widget, multi-widget with KPI row, drill-through source/target

### "How do I create a custom metric?"
Read `docs/Composer-Custom-Metrics-Guide.md`. This covers:
- The PUT endpoint and required headers (`application/vnd.composer.v3+json`)
- Expression syntax (aggregation functions, WHERE filters, TRANSFORM for time comparisons)
- Common business metric patterns (ratios, filtered aggregations, period-over-period)
- Step-by-step MCP workflow (find source → check fields → create metric → verify)
- Naming conventions and important gotchas (minimal body fields, field names vs labels)

### "What REST API endpoints are available?"
Read `docs/Logi Composer REST API Reference.md` for a structured list of all 175 endpoints organized by category (sources, dashboards, visuals, connections, users, permissions, etc.).

For the raw OpenAPI spec with full request/response schemas, see `docs/logi_composer_api_spec_raw.json`. Note: this spec was truncated at ~109K characters during fetch; some later endpoints and component schemas may be incomplete.

### "How do I call the API programmatically via Claude?"
Read `mcp-server/CLAUDE.md`. This explains:
- The resource hierarchy (how sources, dashboards, connections relate)
- Common API workflows (inspecting sources, managing permissions, etc.)
- Parameter conventions and response format
- How to use the generic passthrough tool for uncovered endpoints

### "How do I set up the MCP server?"
Read `mcp-server/USER_GUIDE.md` for step-by-step setup instructions, or `mcp-server/README.md` for a quick technical reference.

## Key concepts

### Authentication
- **Embedding:** Uses Trusted Access tokens (see embedding reference, section 3)
- **REST API:** Uses HTTP Basic authentication (username:password, Base64-encoded)
- **MCP Server:** Credentials configured via `.env` file or Claude Desktop config

### Base paths
The API base path varies by deployment:
- **Cloud / UAT:** `https://<server>/discovery/api/...`
- **Local installs:** `http://localhost:8008/composer/api/...`

The embed script path follows the same pattern:
- **Cloud / UAT:** `https://<server>/discovery/embed/embed.js`
- **Local installs:** `http://localhost:8008/composer/embed/embed.js`

### Core resource types
- **Connections** — database/API connections (the data plumbing)
- **Sources** — data sources built on connections (what users query)
- **Fields** — columns and measures within a source
- **Dashboards** — collections of visuals arranged in a layout
- **Visuals** — individual charts, tables, or KPIs
- **Visual Types** — chart type definitions (bar, line, pivot, etc.)

### Embedding flow (simplified)
1. Load `embed.js` from your Composer server
2. Call `initComposerEmbedManager()` with server URL
3. Authenticate via Trusted Access (`embedManager.setAccessToken()`)
4. Create a component (`embedManager.createComponent()`) with dashboard/visual ID
5. Render into a DOM element (`component.render()`)

## Creating new embedded content

When asked to create embedded Composer content:
1. Use `examples/composer-dashboard-embed.html` as a starting template
2. Refer to `docs/Logi-Composer-Symphony-Embedding-Reference.md` for API details
3. Always use `initComposerEmbedManager` (not the legacy `initLogiEmbedManager`)
4. Use Trusted Access for authentication in embedded contexts

## Calling the REST API

When the MCP server is connected:
1. Refer to `mcp-server/CLAUDE.md` for the resource hierarchy and workflows
2. Use the specific tool for the endpoint (e.g., `get_sources`, `get_dashboards`)
3. Fall back to `composer_api_request` for endpoints without a dedicated tool
4. Always check `status_code` in responses before processing `data`

When the MCP server is NOT connected:
1. Refer to `docs/Logi Composer REST API Reference.md` for endpoint details
2. Generate curl commands or code snippets using Basic auth
3. Remember the base path varies by deployment (`/discovery` vs `/composer`)
