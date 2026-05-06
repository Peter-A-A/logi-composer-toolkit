# Logi Composer / Symphony Embedding Reference

This document is a comprehensive technical reference for embedding Logi Composer (also known as Logi Symphony) dashboards, visuals, and components into web applications. It covers both the current Symphony API (`initComposerEmbedManager`) and the legacy Composer API (`initLogiEmbedManager`), authentication via Trusted Access, event listeners, filtering, cross-visual filtering, context menus, and data query objects.

---

## Table of Contents

1. [Embed Script Setup](#1-embed-script-setup)
2. [Embed Manager Initialization](#2-embed-manager-initialization)
3. [Trusted Access Authentication](#3-trusted-access-authentication)
4. [Component Types](#4-component-types)
5. [Component Configuration](#5-component-configuration)
6. [Rendering Components](#6-rendering-components)
7. [Event Listeners](#7-event-listeners)
8. [Passing Filter Parameters (Initial Filters)](#8-passing-filter-parameters-initial-filters)
9. [Cross-Visual Filtering (Pub/Sub)](#9-cross-visual-filtering-pubsub)
10. [Context Menus](#10-context-menus)
11. [Interactivity Settings](#11-interactivity-settings)
12. [Data Query Objects (ZoomdataSDK)](#12-data-query-objects-zoomdatasdk)
13. [Complete Embedding Examples](#13-complete-embedding-examples)
14. [Quick Reference Tables](#14-quick-reference-tables)
15. [Managed API Authentication Flow (LogOn + DataDiscoveryToken)](#15-managed-api-authentication-flow-logon--datadiscoverytoken)
16. [Standalone Embed Page (Self-Contained HTML)](#16-standalone-embed-page-self-contained-html)
17. [Tenant, Group & User Provisioning via Managed API](#17-tenant-group--user-provisioning-via-managed-api)
18. [Parameterization & Dynamic Data Control](#18-parameterization--dynamic-data-control)
19. [Custom Chart Controller API](#19-custom-chart-controller-api)
20. [Action Templates](#20-action-templates)
21. [Keysets](#21-keysets)
22. [Python Connector](#22-python-connector)
23. [Data Writer Microservice](#23-data-writer-microservice)
24. [File Upload Data Sources (CSV/JSON/TSV via REST API)](#24-file-upload-data-sources-csvjsontsv-via-rest-api)

---

## 1. Embed Script Setup

Include the embed script from your Logi Composer/Symphony server. This script provides the global initialization functions.

```html
<script
  data-name="composer-embed-manager"
  src="https://<YOUR_SERVER>/discovery/embed/embed.js">
</script>
```

Replace `<YOUR_SERVER>` with your Logi Symphony or Composer instance hostname (e.g., `playground.logi-symphony.com` or `yourcompany.logianalytics.com`).

---

## 2. Embed Manager Initialization

There are two initialization functions depending on your version:

### Symphony (Current) — `initComposerEmbedManager`

```javascript
const embedManagerPromise = window.initComposerEmbedManager({
  getToken: getToken
});
```

### Composer (Legacy) — `initLogiEmbedManager`

```javascript
const embedManagerPromise = window.initLogiEmbedManager({
  getToken: getToken
});
```

Both return a `Promise<EmbedManager>`. The `getToken` function must return a Promise that resolves to an object with `access_token` and `expires_in` properties.

### getToken Function Pattern

```javascript
const getToken = async () => {
  const response = await fetch('/api/token', {
    method: 'GET',
    credentials: 'same-origin'
  });
  const result = await response.json();
  return {
    access_token: result.access_token,   // or result.dataDiscoveryToken
    expires_in: result.expires_in || result.expiresIn
  };
};
```

### Legacy Pattern (with global variable)

```javascript
var embedManager;

const initEmbedManager = () => new Promise((resolve) => {
  window.initLogiEmbedManager({
    getToken: () => getToken()
  }).then((em) => {
    embedManager = em;
    setTimeout(resolve, 150);
  });
});

// Also expose globally for SDK use
window.composerGetToken = () => getToken();

const getToken = async () => {
  const response = await fetch('/token');
  return response.json();
};
```

---

## 3. Trusted Access Authentication

Trusted Access allows your backend to authenticate users with the Composer/Symphony server without requiring end-users to log in directly. There are two models: **session-based** and **token-based** (push or pull).

### 3.1 Session-Based Authentication

Create a session for a user, then use the session ID to obtain tokens.

**Create Session:**

```
POST /api/trusted-access/sessions
Content-Type: application/json

{
  "username": "user@example.com",
  "account": "account-name"
}
```

**Response:** A session ID string (plain text).

**Delete Session:**

```
DELETE /api/trusted-access/sessions/{session}
```

### 3.2 Token-Based Authentication — Push Model

The host application pushes user details (including groups, attributes) to create a token. This is the most common approach for embedded analytics.

```
POST /api/trusted-access/push/tokens
Content-Type: application/json

{
  "username": "user@example.com",
  "account": "account-name",
  "fullname": "John Doe",
  "email": "user@example.com",
  "groups": ["GroupA", "GroupB"],
  "attributes": {
    "region": ["North America"],
    "department": ["Sales"]
  }
}
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJ...",
  "expires_in": 3600,
  "token_type": "bearer"
}
```

### 3.3 Token-Based Authentication — Pull Model

The server pulls user details from its own directory. Only username and account are required.

```
POST /api/trusted-access/pull/tokens
Content-Type: application/json

{
  "username": "user@example.com",
  "account": "account-name"
}
```

**Response:** Same format as push model.

### 3.4 Delete Token

```
DELETE /api/trusted-access/tokens/{tokenId}
```

### 3.5 Backend Token Proxy Example (Node.js/Express)

```javascript
const express = require('express');
const axios = require('axios');
const app = express();

const COMPOSER_URL = 'https://your-composer-server.com';
const API_KEY = process.env.COMPOSER_API_KEY; // Trusted Access API key

app.get('/api/token', async (req, res) => {
  try {
    const response = await axios.post(
      `${COMPOSER_URL}/api/trusted-access/push/tokens`,
      {
        username: req.user.email,        // from your auth middleware
        account: 'your-account',
        fullname: req.user.displayName,
        email: req.user.email,
        groups: req.user.groups || [],
        attributes: req.user.attributes || {}
      },
      {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${API_KEY}`
        }
      }
    );
    res.json({
      access_token: response.data.access_token,
      expires_in: response.data.expires_in
    });
  } catch (error) {
    console.error('Token error:', error.message);
    res.status(500).json({ error: 'Failed to obtain token' });
  }
});
```

---

## 4. Component Types

The `createComponent` method accepts the following component type strings:

| Type | Description |
|------|-------------|
| `dashboard` | Full interactive dashboard |
| `lite-dashboard` | Lightweight dashboard (reduced UI) |
| `visual-builder` | Visual/chart builder interface |
| `inventory` | Dashboard/visual inventory browser |
| `source-editor` | Data source editor |
| `chat-bot` | AI chat bot component |
| `report` | Report component |

---

## 5. Component Configuration

### 5.1 DashboardComponentConfiguration

The primary configuration object passed to `createComponent`:

```javascript
const componentConfig = {
  // REQUIRED
  dashboardId: "64abc123def456789",      // Dashboard ID from Composer
  
  // RECOMMENDED
  originId: "64abc123def456789",          // Origin/source dashboard ID
  theme: "__platform__",                  // Theme name or "__platform__" for default
  
  // HEADER
  header: {
    visible: true,                        // Show/hide the header bar
    showTitle: true,                      // Show dashboard title
    showActions: true                     // Show action buttons (save, share, etc.)
  },
  
  // EDITOR
  editor: {
    placement: "modals"                   // "modals" | "dockRight" | "dockBottom"
  },
  
  // INTERACTIVITY
  interactivityProfileName: "interactive", // "interactive" | "viewOnly" | custom profile
  interactivityOverrides: {               // Override specific interactivity settings
    FILTER: true,
    EXPORT: true,
    MULTI_SELECTION: false
    // See Interactivity Settings section for full list
  },
  
  // CONTEXT MENUS (see Section 10)
  menuEventsConfig: { /* ... */ },
  
  // INITIAL FILTERS (see Section 8)
  initialFilters: [ /* ... */ ]
};
```

### 5.2 Theme Options

- `"__platform__"` — Uses the platform default theme
- `"dark"` — Built-in dark theme
- `"light"` — Built-in light theme
- Custom theme name — Any theme configured in the Composer admin

### 5.3 Editor Placement Options

- `"modals"` — Editor opens in modal dialogs
- `"dockRight"` — Editor docks to the right side
- `"dockBottom"` — Editor docks to the bottom

---

## 6. Rendering Components

### Create and Render

```javascript
const embedManager = await window.initComposerEmbedManager({ getToken });

const dashboard = await embedManager.createComponent('dashboard', componentConfig);

dashboard.render(document.getElementById('dashboard-container'), {
  width: "100%",
  height: "100%"
});
```

### Destroy a Component

```javascript
dashboard.destroy();
```

### Helper Function Pattern

```javascript
const createEmbedComponent = async (em, target, id, theme, type = 'dashboard') => {
  document.getElementById(target).innerHTML = "";
  
  const component = await em.createComponent(type, {
    dashboardId: id,
    originId: id,
    theme: theme,
    interactivityProfileName: "interactive",
    header: {
      visible: true,
      showTitle: true,
      showActions: false
    },
    editor: {
      placement: "modals"
    }
  });
  
  component.render(document.getElementById(target), {
    width: "100%",
    height: "100%"
  });
  
  return component;
};
```

---

## 7. Event Listeners

Add event listeners to embedded components to respond to user interactions and lifecycle events.

### 7.1 Syntax

```javascript
dashboard.addEventListener('event-name', (event) => {
  const detail = event.detail;
  // Handle event
});
```

### 7.2 Dashboard Event Names

All dashboard events are prefixed with `composer-dashboard-`:

| Event Name | Trigger |
|------------|---------|
| `composer-dashboard-loaded` | Dashboard has loaded. `event.detail.dashboard` contains the dashboard object. |
| `composer-dashboard-ready` | Dashboard is fully ready for interaction |
| `composer-dashboard-changed` | Dashboard configuration has changed |
| `composer-dashboard-dirty` | Dashboard has unsaved changes |
| `composer-dashboard-pristine` | Dashboard changes have been saved/reverted |
| `composer-dashboard-saved` | Dashboard was saved |
| `composer-dashboard-deleted` | Dashboard was deleted |
| `composer-dashboard-widget-added` | A widget was added to the dashboard |
| `composer-dashboard-widget-removed` | A widget was removed from the dashboard |

### 7.3 Visual Event Names

All visual events are prefixed with `composer-visual-`:

| Event Name | Trigger |
|------------|---------|
| `composer-visual-loaded` | Visual has loaded. `event.detail.visualization` contains the visual object. |
| `composer-visual-rendered` | Visual has finished rendering |
| `composer-visual-failed` | Visual failed to load or render |
| `composer-visual-series-clicked` | User clicked a data series/point |
| `composer-visual-series-deselected` | User deselected a data series/point |
| `composer-visual-series-mouse-over` | Mouse hovered over a data series/point |
| `composer-visual-series-mouse-out` | Mouse left a data series/point |
| `composer-visual-cell-clicked` | User clicked a cell (pivot/table visuals) |
| `composer-visual-cell-mouse-over` | Mouse hovered over a cell |
| `composer-visual-cell-mouse-out` | Mouse left a cell |
| `composer-visual-row-clicked` | User clicked a row (table visuals) |
| `composer-visual-context-menu-clicked` | Context menu item was clicked |
| `composer-visual-context-menu-closed` | Context menu was closed |

### 7.4 Event Listener Examples

```javascript
// Track loaded dashboards
const dashboards = [];
const visuals = [];

dashboard.addEventListener('composer-dashboard-loaded', (e) => {
  dashboards.push(e.detail.dashboard);
  console.log('Dashboard loaded:', e.detail.dashboard);
});

dashboard.addEventListener('composer-visual-loaded', (e) => {
  visuals.push(e.detail.visualization);
  console.log('Visual loaded:', e.detail.visualization);
});

// React to series click
dashboard.addEventListener('composer-visual-series-clicked', (e) => {
  const clickData = e.detail;
  console.log('Series clicked:', clickData);
  // clickData contains group, metric, and visual information
});

// Monitor save state
dashboard.addEventListener('composer-dashboard-dirty', () => {
  document.getElementById('save-indicator').textContent = 'Unsaved changes';
});

dashboard.addEventListener('composer-dashboard-pristine', () => {
  document.getElementById('save-indicator').textContent = 'All changes saved';
});
```

---

## 8. Passing Filter Parameters (Initial Filters)

Initial filters allow you to pre-filter an embedded dashboard when it loads. Filters are passed in the `initialFilters` array of the component configuration.

### 8.1 DashboardInitialFilters Structure

```javascript
const initialFilters = [
  {
    sourceId: "source-id-string",          // REQUIRED: data source ID
    filters: [ /* array of filter objects */ ],
    timeFilter: { /* time filter object */ },
    applyFiltersStrategy: "overrideSamePath"  // or "replaceExisting"
  }
];
```

**`applyFiltersStrategy` options:**

- `"overrideSamePath"` — Overrides only filters on the same field path; keeps other existing filters
- `"replaceExisting"` — Replaces all existing filters with the provided ones

### 8.2 Filter Types

#### TAttributeFilter (Exact match on discrete values)

```javascript
{
  type: "ATTRIBUTE",
  path: "field_path",           // e.g., "country", "product.category"
  operation: "IN",              // "IN" | "NOT_IN" | "EQUALS" | "NOT_EQUALS"
  values: ["USA", "Canada"]     // Array of values to match
}
```

#### TComparisonFilter (Numeric comparison)

```javascript
{
  type: "COMPARISON",
  path: "field_path",
  operation: "GT",             // "GT" | "GTE" | "LT" | "LTE" | "EQ" | "NE"
  value: 100
}
```

#### TRangeFilter (Numeric range)

```javascript
{
  type: "RANGE",
  path: "field_path",
  from: 10,
  to: 100
}
```

#### TTimeFilter (Date/time filtering)

```javascript
{
  type: "TIME",
  path: "date_field",
  timeWindow: {
    from: "2024-01-01T00:00:00Z",
    to: "2024-12-31T23:59:59Z"
  }
}
```

Or with relative time:

```javascript
{
  type: "TIME",
  path: "date_field",
  timeWindow: {
    type: "RELATIVE",
    amount: 30,
    unit: "DAY"        // "MINUTE" | "HOUR" | "DAY" | "WEEK" | "MONTH" | "YEAR"
  }
}
```

#### TTextSearchFilter (Text search)

```javascript
{
  type: "TEXT_SEARCH",
  path: "field_path",
  value: "search term",
  operation: "CONTAINS"       // "CONTAINS" | "STARTS_WITH" | "ENDS_WITH"
}
```

#### TWildcardFilter (Pattern matching)

```javascript
{
  type: "WILDCARD",
  path: "field_path",
  value: "pattern*"
}
```

#### THierarchyFilter (Hierarchical data)

```javascript
{
  type: "HIERARCHY",
  path: "field_path",
  values: ["Level1", "Level2"],
  operation: "IN"
}
```

#### TBooleanFilter

```javascript
{
  type: "BOOLEAN",
  path: "field_path",
  value: true
}
```

#### TKeysetFilter

```javascript
{
  type: "KEYSET",
  path: "field_path",
  keys: ["key1", "key2"],
  operation: "IN"
}
```

### 8.3 Complete Initial Filters Example

```javascript
const componentConfig = {
  dashboardId: "64abc123def456789",
  originId: "64abc123def456789",
  theme: "__platform__",
  header: { visible: true, showTitle: true, showActions: false },
  initialFilters: [
    {
      sourceId: "source-abc-123",
      applyFiltersStrategy: "overrideSamePath",
      filters: [
        {
          type: "ATTRIBUTE",
          path: "country",
          operation: "IN",
          values: ["United States", "Canada"]
        },
        {
          type: "COMPARISON",
          path: "revenue",
          operation: "GTE",
          value: 50000
        }
      ],
      timeFilter: {
        type: "TIME",
        path: "order_date",
        timeWindow: {
          from: "2024-01-01T00:00:00Z",
          to: "2024-12-31T23:59:59Z"
        }
      }
    }
  ]
};
```

---

## 9. Host-to-Dashboard Filtering (WebSocket Injection)

### 9.1 Overview — What Works and What Doesn't

**IMPORTANT:** The documented pub/sub APIs (`dashboard.trigger('EMBED/PUBLISH', ...)`, `embedManager.publish(topic, message)`, and `initialFilters` with `forTopic`) do NOT reliably push filters into embedded dashboard visuals. Testing confirmed:

- `dashboardComponent.trigger('EMBED/PUBLISH', ...)` — **fails** (`trigger is not a function` on `EmbeddedDashboard`)
- `embedManager.publish(topic, message)` — **fires without error** but the dashboard visuals do not filter. The pub/sub bus is outward-only from the dashboard's perspective: dashboard→host works (you can subscribe), but host→dashboard does not reach the query engine.
- `initialFilters` with `forTopic` — **accepted by `createComponent`** but does not register a pub/sub subscriber or filter the initial data load.
- Dispatching `CustomEvent('EMBED/PUBLISH')` on `document` or `dashboardComponent.htmlElement` — **no effect**.

**What DOES work:** Intercepting `WebSocket.prototype.send` to inject filter objects into the `START_VIS` query messages before they reach the server, then calling `dashboardComponent.refreshData()` to trigger new queries.

### 9.2 How It Works

The embed library uses WebSockets (`wss://<server>/discovery/websocket`) for all data queries. Each visual sends a `START_VIS` message with a `filters` array. By intercepting `WebSocket.prototype.send`, you can inject additional filter objects into that array before the message leaves the browser.

**Architecture:**
1. **`activeFilters`** — a global array holding the current filter state (empty = no filter)
2. **WS interceptor** — modifies outgoing `START_VIS` messages to append `activeFilters`
3. **Apply action** — user selects filter values → sets `activeFilters` → calls `dashboardComponent.refreshData()`
4. **Refresh** triggers new `START_VIS` queries → interceptor injects filters → server returns filtered data

### 9.3 Filter Object Format

Filters injected into `START_VIS.filters` use this structure (matching `TAttributeFilter`):

```javascript
// Attribute filter (IN)
{
  operation: 'IN',
  path: { name: 'field_name' },  // field name from the data source
  value: ['Value1', 'Value2']     // array of string values to include
}

// Attribute filter (NOT IN)
{
  operation: 'NOTIN',
  path: { name: 'field_name' },
  value: ['ExcludeThis']
}
```

The `path` field can be a string (`'field_name'`) or an object (`{ name: 'field_name' }`). The object form is recommended as it matches the format used by the dashboard's own internal queries.

### 9.4 WebSocket Interceptor Pattern

```javascript
// ── Active filter state ──
let activeFilters = [];  // Set by UI controls, injected into WS queries

// ── WebSocket interception ──
const SOURCE_ID = 'your-source-id';
let embedWebSocket = null;
const originalWsSend = WebSocket.prototype.send;

WebSocket.prototype.send = function(data) {
  if (typeof data === 'string' && data.includes('START_VIS')) {
    // Capture the embed library's authenticated WS connection
    if (!embedWebSocket) {
      embedWebSocket = this;
    }
    // Inject active filters into dashboard queries
    if (activeFilters.length > 0) {
      try {
        const msg = JSON.parse(data);
        if (msg.type === 'START_VIS' && msg.sourceId === SOURCE_ID) {
          // Skip our own filter-value queries (identified by cid prefix)
          if (!msg.cid || !msg.cid.startsWith('filter_')) {
            msg.filters = (msg.filters || []).concat(activeFilters);
            data = JSON.stringify(msg);
          }
        }
      } catch(e) { /* pass through unmodified */ }
    }
  }
  return originalWsSend.apply(this, arguments);
};
```

### 9.5 Applying Filters

```javascript
function applyFilter(fieldName, selectedValues) {
  if (!selectedValues || selectedValues.length === 0) {
    activeFilters = [];  // Clear = show all data
  } else {
    activeFilters = [{
      operation: 'IN',
      path: { name: fieldName },
      value: selectedValues
    }];
  }
  // Trigger refresh — new START_VIS queries will include the injected filters
  dashboardComponent.refreshData();
}

// Multiple simultaneous filters
function applyMultipleFilters(filters) {
  // filters = [{ field: 'category', values: ['Electronics'] }, { field: 'brand', values: ['Sony'] }]
  activeFilters = filters
    .filter(f => f.values && f.values.length > 0)
    .map(f => ({
      operation: 'IN',
      path: { name: f.field },
      value: f.values
    }));
  dashboardComponent.refreshData();
}
```

### 9.6 Querying Distinct Field Values via WebSocket

To populate filter dropdowns dynamically, query the data source for distinct values using the same WebSocket connection:

```javascript
function queryFieldValues(fieldName, limit) {
  limit = limit || 50;
  return new Promise((resolve, reject) => {
    if (!embedWebSocket || embedWebSocket.readyState !== WebSocket.OPEN) {
      reject(new Error('Embed WebSocket not available'));
      return;
    }
    const cid = 'filter_' + fieldName + '_' + Date.now();

    function handler(e) {
      try {
        const msg = JSON.parse(e.data);
        if (msg.cid === cid) {
          // Server sends ~6 messages per query (status, time range, activity,
          // viewport, DATA, final status). Only act on data or error.
          if (msg.data) {
            const values = msg.data
              .map(row => row.group && row.group[0])
              .filter(val => val != null && val !== '');
            embedWebSocket.removeEventListener('message', handler);
            resolve(values);
          } else if (msg.error) {
            embedWebSocket.removeEventListener('message', handler);
            reject(new Error(msg.error));
          }
          // Otherwise keep listening — the data message hasn't arrived yet
        }
      } catch (ex) { /* ignore parse errors */ }
    }

    embedWebSocket.addEventListener('message', handler);

    const queryMsg = {
      type: 'START_VIS',
      cid: cid,
      cachePolicy: 'UPDATE',
      player: null,
      metrics: [{ type: 'FIELD', field: { name: fieldName }, function: 'COUNT' }],
      time: { from: '+$start_of_data', to: '+$end_of_data', timeField: 'dt' },
      dimensions: [{
        aggregations: [{ type: 'TERMS', field: { name: fieldName } }],
        window: {
          type: 'COMPOSITE',
          aggregationWindows: [{
            limit: limit,
            sort: {
              type: 'METRIC', direction: 'DESC',
              metric: { type: 'FIELD', field: { name: fieldName }, function: 'COUNT' }
            }
          }]
        }
      }],
      sourceId: SOURCE_ID,
      filters: [],
      aggregateFilters: [],
      textSearchEnabled: false
    };
    embedWebSocket.send(JSON.stringify(queryMsg));

    setTimeout(() => {
      embedWebSocket.removeEventListener('message', handler);
      reject(new Error('Query timeout'));
    }, 10000);
  });
}
```

**Important:** The `cid` for filter-value queries must start with `'filter_'` so the WS interceptor skips them (otherwise your filter-value queries would themselves be filtered).

### 9.7 Subscribing to Dashboard Filter Events (Outbound Only)

The pub/sub system DOES work for listening to filter events the dashboard publishes outward (e.g., when a user clicks a bar in a chart):

```javascript
embedManager.subscribe('field_name', (message) => {
  console.log('Dashboard filtered by:', message);
  // message = { type: 'selection', valueType: 'ATTRIBUTE',
  //             ranges: [{ operation: 'IN', value: ['clicked_value'] }] }
});
```

Topic names match field names (e.g., `'category'`). Subscribing to the label form (e.g., `'Category'`) also works.

### 9.8 Complete Host-to-Dashboard Filter Example

See `examples/opc-revenue-dashboard-embed.html` for a full working implementation with:
- Login form with Managed API authentication (LogOn → DataDiscoveryToken)
- Dynamic filter dropdown populated via WebSocket field value query
- Apply/Reset buttons that set `activeFilters` and call `refreshData()`
- WebSocket interceptor that injects filters into `START_VIS` queries

---

## 10. Context Menus

Context menus allow you to add custom actions to the right-click or click menu on visuals within embedded dashboards.

### 10.1 menuEventsConfig Structure

```javascript
const menuEventsConfig = {
  click: 'openMenu',               // 'openMenu' triggers context menu on click
  
  customActions: [                  // Array of custom menu items
    {
      name: "Action Label",        // Display text in menu
      icon: {
        src: "https://example.com/icon.png"  // URL to icon image
      },
      action: (data) => {
        // data.data.group — array of group/dimension values
        // data.data.metric — metric values
        // Custom handler function
        console.log('Clicked:', data);
      }
    }
  ],
  
  seriesItems: [                   // Items shown when clicking on a data point
    {
      name: "Drill Into",
      action: (data) => { /* handler */ }
    }
  ],
  
  blankSpaceItems: [               // Items shown when clicking empty space
    {
      name: "Reset View",
      action: (data) => { /* handler */ }
    }
  ]
};
```

### 10.2 Context Menu Data Object

When a custom action is triggered, the callback receives a `data` object:

```javascript
{
  data: {
    group: ["value1", "value2"],   // Dimension values at clicked point
    metric: { metricName: 123 }    // Metric values at clicked point
  },
  visualization: { /* visual info */ },
  widget: { /* widget info */ }
}
```

### 10.3 Context Menu Example — Google Search

```javascript
const dashboard = await em.createComponent('dashboard', {
  dashboardId: id,
  theme: 'light',
  editor: { placement: 'dockRight' },
  header: { showActions: false, visible: true, showTitle: false },
  menuEventsConfig: {
    click: 'openMenu',
    customActions: [
      {
        icon: {
          src: 'https://help.insightsoftware.com/fileasset/logo.png'
        },
        name: "Google It",
        action: (data) => {
          window.open(
            'https://www.google.com/search?q=' + data.data.group[0],
            '_blank'
          ).focus();
        }
      },
      {
        name: "Show Details",
        action: (data) => {
          alert(`Group: ${data.data.group.join(', ')}`);
        }
      }
    ]
  }
});
```

---

## 11. Interactivity Settings

Control which UI features are available in the embedded component using `interactivityOverrides` or `interactivityProfileName`.

### 11.1 InteractivitySettings Properties

| Property | Type | Description |
|----------|------|-------------|
| `ADD_NEW` | boolean | Allow adding new visuals/widgets |
| `AVAILABLE_VISUAL_TYPES` | boolean | Show visual type picker |
| `CLEAR_CACHE` | boolean | Allow cache clearing |
| `COLUMN_SECURITY` | boolean | Enable column-level security |
| `DELETE` | boolean | Allow deleting dashboards/visuals |
| `DESCRIPTION` | boolean | Show/edit description |
| `EXPORT` | boolean | Allow exporting data/images |
| `FAVORITES` | boolean | Allow favoriting |
| `FILTER` | boolean | Show filter controls |
| `IMPORT` | boolean | Allow importing |
| `MULTI_SELECTION` | boolean | Enable multi-selection on visuals |
| `PERMISSIONS` | boolean | Show permissions UI |
| `ROW_SECURITY` | boolean | Enable row-level security |
| `SCHEDULE` | boolean | Allow scheduling |
| `SHARE` | boolean | Allow sharing |
| `TAGS` | boolean | Show/edit tags |

### 11.2 Interactivity Profiles

- `"interactive"` — Full interactivity (all features enabled)
- `"viewOnly"` — Read-only mode (most editing disabled)
- Custom profile names configured in the Composer admin

### 11.3 Example: Custom Interactivity

```javascript
const config = {
  dashboardId: "abc123",
  interactivityProfileName: "interactive",
  interactivityOverrides: {
    FILTER: true,
    EXPORT: true,
    MULTI_SELECTION: true,
    DELETE: false,
    SHARE: false,
    PERMISSIONS: false,
    ADD_NEW: false,
    SCHEDULE: false
  }
};
```

---

## 12. Data Query Objects (ZoomdataSDK)

The ZoomdataSDK allows you to query data sources directly without rendering visuals. This is useful for building custom visualizations or extracting data programmatically.

### 12.1 Prerequisites

The ZoomdataSDK is available from the Composer/Symphony server. You also need a valid token.

### 12.2 Creating a Client

```javascript
const credentials = await getToken();

const client = await ZoomdataSDK.createClient({
  credentials: credentials,
  application: {
    secure: true,
    host: 'your-server.com',
    port: 443,
    path: '/discovery'
  }
});
```

### 12.3 Query Configuration Object

```javascript
const queryConfig = {
  sourceId: 'your-source-id',
  fields: [
    { name: 'category', limit: 20, sort: { dir: 'desc', name: 'count' } },
    { name: 'revenue', func: 'sum' }
  ],
  filters: [
    {
      type: 'ATTRIBUTE',
      path: 'region',
      operation: 'IN',
      values: ['North America']
    }
  ],
  time: {
    timeField: 'order_date',
    from: '2024-01-01T00:00:00Z',
    to: '2024-12-31T23:59:59Z'
  },
  limit: 1000
};
```

### 12.4 Creating and Running a Query

```javascript
const query = client.createQuery(queryConfig);

// Run with callback
query.run((result) => {
  console.log('Query result:', result);
  
  // result.data — array of data rows
  // Each row contains grouped dimensions and aggregated metrics
  result.data.forEach((row) => {
    console.log('Group:', row.group);
    console.log('Current:', row.current);
  });
});

// Or with promise
const result = await query.run();
```

### 12.5 Finding Data in Results

Query results typically have this structure:

```javascript
{
  data: [
    {
      group: ["Category A"],        // Dimension values
      current: {
        count: 1500,                // Record count
        metrics: {
          revenue: { sum: 250000 }  // Aggregated metric
        }
      }
    },
    {
      group: ["Category B"],
      current: {
        count: 800,
        metrics: {
          revenue: { sum: 120000 }
        }
      }
    }
  ]
}
```

### 12.6 Complete Data Query Example

```javascript
async function queryData(sourceId, filters) {
  const token = await getToken();
  
  const client = await ZoomdataSDK.createClient({
    credentials: token,
    application: {
      secure: true,
      host: 'your-server.com',
      port: 443,
      path: '/discovery'
    }
  });

  const query = client.createQuery({
    sourceId: sourceId,
    fields: [
      { name: 'product_category', limit: 50, sort: { dir: 'desc', name: 'count' } },
      { name: 'sales_amount', func: 'sum' },
      { name: 'order_count', func: 'count' }
    ],
    filters: filters || [],
    limit: 500
  });

  return new Promise((resolve, reject) => {
    query.run((result) => {
      if (result.error) {
        reject(result.error);
      } else {
        resolve(result.data);
      }
    });
  });
}

// Usage
const data = await queryData('source-123', [
  {
    type: 'ATTRIBUTE',
    path: 'region',
    operation: 'IN',
    values: ['North America', 'Europe']
  }
]);
```

---

## 13. Complete Embedding Examples

### 13.1 Full Symphony Embed (Current Approach)

```html
<!DOCTYPE html>
<html>
<head>
  <title>Embedded Dashboard</title>
  <style>
    #dashboard-container {
      width: 100%;
      height: 90vh;
    }
  </style>
</head>
<body>
  <div id="dashboard-container"></div>

  <script data-name="composer-embed-manager"
          src="https://YOUR_SERVER/discovery/embed/embed.js"></script>
  <script>
    const getToken = async () => {
      const response = await fetch('/api/token', {
        method: 'GET',
        credentials: 'same-origin'
      });
      return response.json().then((result) => ({
        access_token: result.dataDiscoveryToken || result.access_token,
        expires_in: result.expiresIn || result.expires_in
      }));
    };

    async function init() {
      const em = await window.initComposerEmbedManager({ getToken });

      const dashboard = await em.createComponent('dashboard', {
        dashboardId: 'YOUR_DASHBOARD_ID',
        originId: 'YOUR_DASHBOARD_ID',
        interactivityProfileName: 'interactive',
        theme: '__platform__',
        editor: { placement: 'modals' },
        header: {
          showActions: false,
          showTitle: true,
          visible: true
        },
        interactivityOverrides: {
          FILTER: true,
          EXPORT: true,
          DELETE: false,
          SHARE: false
        },
        initialFilters: [
          {
            sourceId: 'YOUR_SOURCE_ID',
            applyFiltersStrategy: 'overrideSamePath',
            filters: [
              {
                type: 'ATTRIBUTE',
                path: 'region',
                operation: 'IN',
                values: ['North America']
              }
            ]
          }
        ]
      });

      dashboard.render(
        document.getElementById('dashboard-container'),
        { width: '100%', height: '100%' }
      );

      // Event listeners
      dashboard.addEventListener('composer-dashboard-loaded', (e) => {
        console.log('Dashboard loaded:', e.detail.dashboard);
      });

      dashboard.addEventListener('composer-visual-series-clicked', (e) => {
        console.log('Clicked:', e.detail);
      });
    }

    init();
  </script>
</body>
</html>
```

### 13.2 Legacy Composer Embed

```html
<!DOCTYPE html>
<html>
<head>
  <title>Embedded Dashboard (Legacy)</title>
</head>
<body>
  <div id="dashboard-container" style="width:100%; height:90vh;"></div>

  <script data-name="composer-embed-manager"
          src="https://YOUR_SERVER/discovery/embed/embed.js"></script>
  <script>
    var embedManager, visuals = [], dashboards = [];

    const initEmbedManager = () => new Promise((resolve) => {
      window.initLogiEmbedManager({
        getToken: () => getToken()
      }).then((em) => {
        embedManager = em;
        setTimeout(resolve, 150);
      });
    });

    window.composerGetToken = () => getToken();

    const getToken = async () => {
      const response = await fetch('/token');
      return response.json();
    };

    const addViz = async (target, id, theme, canEdit = false, type = 'dashboard') => {
      if (typeof embedManager === 'undefined' || embedManager == null) {
        await initEmbedManager();
      }

      const dashboard = await embedManager.createComponent(type, {
        dashboardId: id,
        root: target,
        theme: theme,
        header: {
          visible: canEdit,
          showTitle: canEdit,
          showActions: canEdit
        }
      });

      dashboard.render(document.getElementById(target), {
        width: '100%',
        height: '100%'
      });

      dashboard.addEventListener('composer-visual-loaded', (e) => {
        visuals.push(e.detail.visualization);
      });

      dashboard.addEventListener('composer-dashboard-loaded', (e) => {
        dashboards.push(e.detail.dashboard);
      });

      return dashboard;
    };

    // Usage
    addViz('dashboard-container', 'DASHBOARD_ID', 'light', false);
  </script>
</body>
</html>
```

### 13.3 Multiple Dashboards with Context Menus

```javascript
const dashboards = [];

const AddComponent = async (em, target, id) => {
  document.getElementById(target).innerHTML = "";

  const dashboard = await em.createComponent('dashboard', {
    dashboardId: id,
    theme: 'light',
    editor: { placement: 'dockRight' },
    header: { showActions: false, visible: true, showTitle: false },
    menuEventsConfig: {
      click: 'openMenu',
      customActions: [
        {
          icon: { src: 'https://example.com/icon.png' },
          name: "Google It",
          action: (data) => {
            window.open(
              'https://www.google.com/search?q=' + data.data.group[0],
              '_blank'
            ).focus();
          }
        },
        {
          name: "View Record",
          action: (data) => {
            // Navigate to detail page with clicked value
            window.location.href = `/detail/${encodeURIComponent(data.data.group[0])}`;
          }
        }
      ]
    }
  });

  dashboard.render(document.getElementById(target), {
    width: "100%",
    height: "100%"
  });

  dashboard.addEventListener('composer-dashboard-loaded', (e) => {
    dashboards.push(e.detail.dashboard);
  });

  return dashboard;
};
```

---

## 14. Quick Reference Tables

### Initialization Methods

| Method | API | Notes |
|--------|-----|-------|
| `window.initComposerEmbedManager({ getToken })` | Symphony (current) | Returns Promise<EmbedManager> |
| `window.initLogiEmbedManager({ getToken })` | Composer (legacy) | Returns Promise<EmbedManager> |

### getToken Response Format

```javascript
{
  access_token: "string",   // JWT or bearer token
  expires_in: 3600          // Seconds until expiry
}
```

### Trusted Access Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/trusted-access/sessions` | POST | Create session (username, account) |
| `/api/trusted-access/sessions/{session}` | DELETE | Delete session |
| `/api/trusted-access/push/tokens` | POST | Create push token (username, account, fullname, email, groups, attributes) |
| `/api/trusted-access/pull/tokens` | POST | Create pull token (username, account) |
| `/api/trusted-access/tokens/{tokenId}` | DELETE | Delete token |

### Filter Type Quick Reference

| Filter Type | Key Properties | Use Case |
|-------------|---------------|----------|
| `ATTRIBUTE` | path, operation (IN/NOT_IN/EQUALS/NOT_EQUALS), values | Discrete value filtering |
| `COMPARISON` | path, operation (GT/GTE/LT/LTE/EQ/NE), value | Numeric comparison |
| `RANGE` | path, from, to | Numeric range |
| `TIME` | path, timeWindow (from/to or relative) | Date/time filtering |
| `TEXT_SEARCH` | path, value, operation (CONTAINS/STARTS_WITH/ENDS_WITH) | Text search |
| `WILDCARD` | path, value | Pattern matching |
| `HIERARCHY` | path, values, operation | Hierarchical data |
| `BOOLEAN` | path, value | True/false filtering |
| `KEYSET` | path, keys, operation | Key-based filtering |

### Event Prefixes

| Component | Event Prefix | Example |
|-----------|-------------|---------|
| Dashboard | `composer-dashboard-` | `composer-dashboard-loaded` |
| Visual | `composer-visual-` | `composer-visual-series-clicked` |

---

## 15. Managed API Authentication Flow (LogOn + DataDiscoveryToken)

In addition to the Trusted Access push/pull token endpoints (Section 3), Symphony provides a **Managed API** authentication path that uses session-based login followed by a discovery token exchange. This is the flow used in the official Postman collection and is common for internal tools, demos, and service accounts.

### 15.1 Step 1 — LogOn to Get a Session ID

```
POST {{baseUrl}}/managed/API/LogOn
Content-Type: application/json

{
  "accountName": "service",
  "password": "Password01!",
  "isWindowsLogOn": false,
  "deleteOtherSessions": false,
  "performDataDiscoveryLogon": true
}
```

**Response:**

```json
{
  "sessionId": "abc123-session-id-string",
  ...
}
```

The `performDataDiscoveryLogon: true` flag is **required** — it ensures the session is valid for obtaining a Data Discovery token in the next step.

#### Tenant Impersonation (effectiveAccountName)

To log on as a specific tenant administrator, add the `effectiveAccountName` field:

```json
{
  "effectiveAccountName": "Common Admin",
  "accountName": "service",
  "password": "Password01!",
  "isWindowsLogOn": false,
  "deleteOtherSessions": false,
  "performDataDiscoveryLogon": true
}
```

This allows a super-admin or service account to act on behalf of a tenant admin without knowing the tenant admin's credentials.

### 15.2 Step 2 — Exchange Session for Data Discovery Token

```
GET {{baseUrl}}/managed/API/Session/DataDiscoveryToken/
Authorization: Bearer {{sessionId}}
```

**Response:** A plain JSON string containing the discovery token (JWT).

This discovery token is what gets passed as the `access_token` to the embed manager's `getToken` function.

### 15.3 Step 3 — Wire Into Embed Manager

```javascript
const getToken = async () => {
  // Step 1: LogOn
  const logonRes = await fetch(`${SERVER_URL}/managed/API/LogOn`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      accountName: USERNAME,
      password: PASSWORD,
      isWindowsLogOn: false,
      deleteOtherSessions: false,
      performDataDiscoveryLogon: true
    })
  });
  const { sessionId } = await logonRes.json();

  // Step 2: Get Discovery Token
  const tokenRes = await fetch(`${SERVER_URL}/managed/API/Session/DataDiscoveryToken/`, {
    headers: { 'Authorization': `Bearer ${sessionId}` }
  });
  const discoveryToken = await tokenRes.json();

  return {
    access_token: discoveryToken,
    expires_in: 3600
  };
};

// Step 3: Initialize embed manager
const em = await window.initComposerEmbedManager({ getToken });
```

### 15.4 Session Cleanup

Sessions should be cleaned up when no longer needed:

```
POST {{baseUrl}}/managed/api/session/delete/?sessionId={{apiSessionId}}
Content-Type: application/json

{
  "sessionIds": ["{{sessionId1}}", "{{sessionId2}}"]
}
```

### 15.5 Managed API Endpoints Quick Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/managed/API/LogOn` | POST | Authenticate and get a session ID |
| `/managed/API/Session/DataDiscoveryToken/` | GET | Exchange session for a discovery token (Bearer auth) |
| `/managed/api/session/delete/` | POST | Delete one or more sessions |
| `/managed/api/tenant` | POST | Create a new tenant |
| `/managed/api/account` | POST | Create a user account |
| `/managed/api/group` | POST | Create a group |
| `/managed/api/group/addmembertogroups/{accountId}` | POST | Add a user to groups |
| `/discovery/api/groups` | PUT | Update group roles/privileges for Discovery (requires `application/vnd.composer.v3+json` content type and a discovery token) |

---

## 16. Standalone Embed Page (Self-Contained HTML)

When you need a quick, portable way to embed a dashboard without a backend proxy, you can use a self-contained HTML page that handles the full auth + embed flow client-side. This is useful for demos, internal tools, and rapid prototyping.

### 16.1 How It Works

1. User enters server URL, credentials, and dashboard ID in a login form
2. Page calls **LogOn** → gets `sessionId`
3. Page calls **DataDiscoveryToken** → gets discovery token
4. Page dynamically loads `embed.js` from the server
5. Initializes `initComposerEmbedManager` with the token
6. Renders the dashboard component

### 16.2 Key Implementation Details

**Dynamic embed.js loading** — The script is loaded at runtime rather than hardcoded, so the same HTML works against any Symphony server:

```javascript
function loadEmbedScript(serverUrl) {
  return new Promise((resolve, reject) => {
    if (window.initComposerEmbedManager) { resolve(); return; }
    const script = document.createElement('script');
    script.setAttribute('data-name', 'composer-embed-manager');
    script.src = `${serverUrl}/discovery/embed/embed.js`;
    script.onload = () => setTimeout(resolve, 200);
    script.onerror = () => reject(new Error('Failed to load embed.js'));
    document.head.appendChild(script);
  });
}
```

**Token caching with refresh** — Avoids re-authenticating on every embed manager token request:

```javascript
let cachedToken = null;
let tokenExpiry = 0;

async function getToken() {
  const now = Date.now();
  if (cachedToken && now < tokenExpiry - 60000) {
    return cachedToken;
  }
  cachedToken = await getDiscoveryToken();
  tokenExpiry = now + (cachedToken.expires_in * 1000);
  return cachedToken;
}
```

### 16.3 CORS Considerations

Since the standalone page makes cross-origin requests to the Symphony server, CORS must be configured. Options:

- **Same-origin deployment**: Serve the HTML from the same domain as the Symphony server
- **Reverse proxy**: Place the HTML behind a proxy that routes `/managed/` and `/discovery/` to the Symphony server
- **CORS headers**: Configure the Symphony server to allow requests from the embed page's origin

### 16.4 Dashboard ID Format

Dashboard IDs in Symphony URLs follow this pattern:

```
/discovery/visualization/{dashboardId}
```

For example, the URL:
```
https://preview.logi-symphony.com/discovery/visualization/6597b290b953476212e25f2e_69d6328a819b936d08b88bae
```

Contains the dashboard ID: `6597b290b953476212e25f2e_69d6328a819b936d08b88bae`

This ID is used as both `dashboardId` and `originId` in the component configuration.

### 16.5 Embedding Limitations in Sandboxed Environments

Composer embeds require loading `embed.js` from the Symphony server and making authenticated API calls. This means they **cannot** be embedded inside:

- **Sandboxed iframes** that block external network requests
- **Cowork artifacts** (which only allow Chart.js, Grid.js, and Mermaid from CDN)
- **Environments with strict CSP** that block the Symphony server domain

In these cases, use a standalone HTML page opened directly in the browser, or serve it from a location with network access to the Symphony server.

---

## 17. Tenant, Group & User Provisioning via Managed API

The Managed API supports programmatic provisioning of tenants, groups, and users. This is the workflow used in the official Postman collection for setting up multi-tenant environments.

### 17.1 Provisioning Workflow

1. **LogOn** as a super-admin/service account
2. **Create a tenant** → returns `tenantId`, `administratorsGroupId`, `membersGroupId`
3. **Create a tenant admin user** → assign to the tenant
4. **Add user to administrators group**
5. **Create custom groups** (Content Authors, Data Authors, Read-Only)
6. **LogOn as tenant admin** (using `effectiveAccountName`)
7. **Get discovery token** for the tenant context
8. **Update group roles** via the Discovery API

### 17.2 Create a Tenant

```
POST {{baseUrl}}/managed/api/tenant
Authorization: Bearer {{sessionId}}
Content-Type: application/json

{
  "name": "TenantName",
  "isEnabled": true,
  "__classType": "dundas.account.Tenant"
}
```

**Response:**

```json
{
  "id": "tenant-id",
  "administratorsGroupId": "admin-group-id",
  "membersGroupId": "members-group-id"
}
```

### 17.3 Create a User Account

```
POST {{baseUrl}}/managed/api/account
Authorization: Bearer {{sessionId}}
Content-Type: application/json

{
  "__classType": "dundas.account.Account",
  "accountType": "LocalUser",
  "canChangePassword": true,
  "displayName": "Tenant Administrator",
  "emailAddress": "admin@example.com",
  "isEnabled": true,
  "isSeatReserved": true,
  "name": "tenant-admin",
  "password": "Password01!",
  "seatKind": "Developer",
  "tenantIds": ["{{tenantId}}"]
}
```

### 17.4 Add User to Group

```
POST {{baseUrl}}/managed/api/group/addmembertogroups/{{userId}}
Authorization: Bearer {{sessionId}}
Content-Type: application/json

{
  "accountIds": ["{{userId}}"],
  "groupIds": ["{{groupId}}"]
}
```

### 17.5 Create a Custom Group

```
POST {{baseUrl}}/managed/api/group
Authorization: Bearer {{sessionId}}
Content-Type: application/json

{
  "__classType": "dundas.account.Group",
  "name": "Content Authors",
  "description": "Can view, create, edit and delete all dashboards and visuals",
  "groupKind": "Standard",
  "seatKind": "PowerUser",
  "tenantId": "{{tenantId}}",
  "deniedApplicationPrivilegeIds": [],
  "grantedApplicationPrivilegeIds": []
}
```

### 17.6 Update Group Roles for Discovery

This call requires a **discovery token** (not a session ID) and the special content type header:

```
PUT {{baseUrl}}/discovery/api/groups
Authorization: Bearer {{discoveryToken}}
Content-Type: application/vnd.composer.v3+json

{
  "group": {
    "accountId": "{{tenantId}}",
    "id": "{{groupId}}",
    "label": "Content Authors",
    "roles": [
      "ROLE_ADMINISTER_VISUALS",
      "ROLE_EXPORT_VISUALS",
      "ROLE_CREATE_VISUALS",
      "ROLE_PERMISSION_VISUALS",
      "ROLE_ADMINISTER_DASHBOARDS",
      "ROLE_EXPORT_DASHBOARDS",
      "ROLE_CREATE_DASHBOARDS",
      "ROLE_PERMISSION_DASHBOARDS",
      "ROLE_ADMINISTER_DASHBOARD_REPORTS",
      "ROLE_CREATE_DASHBOARD_REPORTS",
      "ROLE_ADMINISTER_TAGS",
      "ROLE_CREATE_TAGS",
      "ROLE_EDIT_FORMULAS",
      "ROLE_ADMINISTER_ALERTS",
      "ROLE_CREATE_ALERTS",
      "ROLE_SAVE_FILTERS",
      "ROLE_GENERATE_EMBED_CODE",
      "ROLE_ADMINISTER_INITIAL_VISUALS"
    ],
    "system": false
  },
  "sources": [],
  "userIds": []
}
```

### 17.7 Common Discovery Role Sets

**Content Authors:**
`ROLE_ADMINISTER_VISUALS`, `ROLE_EXPORT_VISUALS`, `ROLE_CREATE_VISUALS`, `ROLE_PERMISSION_VISUALS`, `ROLE_ADMINISTER_DASHBOARDS`, `ROLE_EXPORT_DASHBOARDS`, `ROLE_CREATE_DASHBOARDS`, `ROLE_PERMISSION_DASHBOARDS`, `ROLE_ADMINISTER_DASHBOARD_REPORTS`, `ROLE_CREATE_DASHBOARD_REPORTS`, `ROLE_ADMINISTER_TAGS`, `ROLE_CREATE_TAGS`, `ROLE_EDIT_FORMULAS`, `ROLE_ADMINISTER_ALERTS`, `ROLE_CREATE_ALERTS`, `ROLE_SAVE_FILTERS`, `ROLE_GENERATE_EMBED_CODE`, `ROLE_ADMINISTER_INITIAL_VISUALS`

**Data Authors:**
`ROLE_ADMINISTER_SOURCES`, `ROLE_CREATE_SOURCES`, `ROLE_EDIT_FORMULAS`, `ROLE_PERMISSION_SOURCES`, `ROLE_MANAGE_CONNECTIONS`, `ROLE_MANAGE_FILE_UPLOADS`, `ROLE_ADMINISTER_VISUAL_TYPES`, `ROLE_ADMINISTER_CALENDARS`, `ROLE_GENERATE_EMBED_CODE`, `ROLE_SAVE_FILTERS`

---

## Notes

- **Dashboard IDs and Source IDs** are MongoDB ObjectId strings (24 hex characters). These are found in the Composer admin UI or via the API. Some dashboard IDs use a compound format with an underscore (e.g., `6597b290b953476212e25f2e_69d6328a819b936d08b88bae`).
- **Theme names** are case-sensitive. Use `"__platform__"` for the server default.
- **The embed.js script** must be loaded before calling any initialization functions. Use the `data-name="composer-embed-manager"` attribute on the script tag. It can be loaded dynamically at runtime.
- **Token refresh** is handled automatically by the embed manager — it will call your `getToken` function again when the token expires. Implement token caching in your `getToken` function to avoid unnecessary re-authentication.
- **Cross-origin** embedding requires the Composer/Symphony server to be configured with appropriate CORS headers for your host domain.
- **`originId`** should typically match `dashboardId`. It represents the original/source dashboard from which a copy may have been derived.
- **The `performDataDiscoveryLogon: true` flag** must be set in the LogOn request body to enable the DataDiscoveryToken endpoint.
- **Discovery API calls** (e.g., updating group roles) require the content type `application/vnd.composer.v3+json` and a discovery token, not a session ID.
- **The preview server** at `preview.logi-symphony.com` is an insightsoftware-hosted instance used for demos and testing.

---

## 18. Parameterization & Dynamic Data Control

This section covers how to achieve parameter-like behavior in the **Composer Discovery / Visual Data Discovery (VDD) embed layer** — passing values from the host application into embedded dashboards so they influence the underlying data queries.

### 18.1 The Problem

A common embedding requirement is: the host application has a value (e.g., a tenant ID, a selected product line, a date threshold, a user-chosen multiplier) and needs to push that value into an embedded dashboard such that it affects how data is queried or computed — not just filtered.

True "view parameters" would flow into formulas or expressions defined in a Composer data source, influencing calculated fields, derived metrics, or SQL template arguments. The Composer Discovery embed API does not expose a dedicated `parameters` or `variables` key in its component configuration or query configuration objects. However, several Composer-native mechanisms can achieve equivalent results depending on the use case.

### 18.2 Mechanism 1: Initial Filters + EMBED/PUBLISH (Runtime Filter Injection)

**Best for:** Restricting the data a dashboard shows based on a host-app value (e.g., tenant scoping, region selection, date range).

Filters are the primary way the embed API passes values into dashboards. They restrict which rows are returned from the data source but do not alter computed expressions.

**At embed time (static):**

```javascript
const dashboard = await em.createComponent('dashboard', {
  dashboardId: 'abc123',
  initialFilters: [
    {
      sourceId: 'source-id',
      applyFiltersStrategy: 'overrideSamePath',
      filters: [
        {
          type: 'ATTRIBUTE',
          path: 'tenant_id',
          operation: 'IN',
          values: [hostApp.currentTenantId]  // Value from host app
        }
      ]
    }
  ]
});
```

**At runtime (dynamic):**

```javascript
// User selects a new value in the host app → push it into the dashboard
dashboard.trigger('EMBED/PUBLISH', {
  sourceId: 'source-id',
  filter: {
    type: 'ATTRIBUTE',
    path: 'product_line',
    operation: 'IN',
    values: [selectedProductLine]
  }
});
```

**Limitations:** Filters restrict rows returned. They cannot change a formula, pass a scalar into a calculation, or alter how a derived field is computed.

### 18.3 Mechanism 2: Admin-Defined Functions (Connector-Level Custom SQL)

**Best for:** Creating reusable SQL expressions with field-based arguments that can be used in derived fields and custom metrics. Useful when the "parameter" is actually a column value that needs to be transformed by a custom formula.

Admin-Defined Functions allow you to define custom SQL functions at the **connector level**. They are defined in JSON files and become available in the Composer Derived Field Editor for any data source using that connector.

#### 18.3.1 Overview

- Available only for **SQL-based connectors** that support row-level expressions
- Perform **row-level operations only** (not aggregation)
- Arguments are **field references** (columns), not arbitrary user-supplied scalars
- Defined per connector via JSON files stored on the server
- Once activated, they appear in the Derived Field Editor UI

#### 18.3.2 Supported Connectors

PostgreSQL, MySQL, MariaDB, SQL Server, Oracle, Snowflake, BigQuery, Redshift, Impala, Hive, Spark SQL, Databricks, SAP HANA, Vertica, Teradata, Greenplum, ClickHouse, Dremio, and other SQL-based EDC connectors.

#### 18.3.3 JSON File Structure

Function definition files are stored at:
- **Linux:** `/etc/zoomdata/edc-<connector>-functions.json`
- **Windows:** `<install-path>/conf-modify/edc-<connector>-functions.json`

```json
{
  "<FUNCTION_NAME>": {
    "template": "<SQL template with {arg_key} placeholders>",
    "returnType": {
      "type": "simple|generic",
      "name": "NUMBER|INTEGER|STRING|DATE|BOOLEAN or generic name"
    },
    "arguments": {
      "<arg_key>": {
        "name": "Display Name",
        "returnType": {
          "type": "simple|generic|array",
          "name": "NUMBER|INTEGER|STRING|DATE|BOOLEAN or generic name"
        },
        "description": "What this argument represents"
      }
    },
    "description": "What this function does"
  }
}
```

#### 18.3.4 Template Syntax

The `template` string is raw SQL. Argument placeholders use `{arg_key}` syntax and are replaced at runtime with the SQL representation of the referenced field. Escape braces with backslash: `\{`, `\}`, `\\`.

```json
{
  "REVENUE_WITH_TAX": {
    "template": "({revenue}) * (1 + {tax_rate})",
    "returnType": { "type": "simple", "name": "NUMBER" },
    "arguments": {
      "revenue": {
        "name": "Revenue",
        "returnType": { "type": "simple", "name": "NUMBER" },
        "description": "Revenue amount field"
      },
      "tax_rate": {
        "name": "Tax Rate",
        "returnType": { "type": "simple", "name": "NUMBER" },
        "description": "Tax rate field (e.g., 0.08 for 8%)"
      }
    },
    "description": "Calculate revenue including tax"
  }
}
```

#### 18.3.5 Return Types

| Type | Usage | Example |
|------|-------|---------|
| `simple` | Concrete type | `{ "type": "simple", "name": "NUMBER" }` |
| `generic` | Inferred from argument | `{ "type": "generic", "name": "T" }` — must match an argument's generic name |
| `array` | Variadic last argument only | `{ "type": "array", "baseType": { "type": "simple", "name": "STRING" } }` |

#### 18.3.6 Complete Example — Two Functions

```json
{
  "TEST_ADD": {
    "template": "{summand_1} + {summand_2}",
    "returnType": { "type": "simple", "name": "NUMBER" },
    "arguments": {
      "summand_1": {
        "name": "Summand 1",
        "returnType": { "type": "simple", "name": "NUMBER" },
        "description": "An expression evaluated to a numeric value."
      },
      "summand_2": {
        "name": "Summand 2",
        "returnType": { "type": "simple", "name": "NUMBER" },
        "description": "An expression evaluated to a numeric value."
      }
    },
    "description": "Addition: add two numbers."
  },
  "ADD_YEARS": {
    "template": "({0}) + ({1}) * interval '1 year'",
    "returnType": { "type": "simple", "name": "DATE" },
    "arguments": {
      "0": {
        "name": "Date",
        "returnType": { "type": "simple", "name": "DATE" },
        "description": "A date expression"
      },
      "1": {
        "name": "Years",
        "returnType": { "type": "simple", "name": "INTEGER" },
        "description": "Number of years to add"
      }
    },
    "description": "Add years to a date."
  }
}
```

#### 18.3.7 Validation

Composer provides a JSON schema file for each connector at:
- **Linux:** `/opt/zoomdata/docs/edc-<connector>/functions-schema.json`
- **Windows:** `<install-path>/docs/edc-<connector>/functions-schema.json`

Use a JSON Schema Validator (e.g., jsonschemavalidator.net) to validate your function definitions before deploying.

#### 18.3.8 Limitations for Parameterization

Admin-Defined Functions are powerful for custom SQL expressions, but they have key constraints when considered as a "view parameter" mechanism:

- **Arguments are field references, not user-supplied scalars.** When a user applies `REVENUE_WITH_TAX` in a derived field, they map `revenue` → a column and `tax_rate` → another column. They cannot type in an arbitrary number like `0.08`.
- **Row-level only.** Cannot be used for aggregation operations.
- **Static deployment.** JSON files must be placed on the server filesystem and the connector restarted. They cannot be created or modified at runtime via the API.

**Workaround for scalar parameters:** Create a lookup table or a single-column "parameter" table in your database containing the parameter value. The Admin-Defined Function references this column. To change the parameter value, update the row in the parameter table. This is a database-level pattern, not a Composer-level one.

### 18.4 Mechanism 3: ZoomdataSDK Data Queries with Dynamic Configuration

**Best for:** Custom applications that query Composer data sources programmatically and build their own visualizations. Full control over the query, but no rendered dashboard.

When using the ZoomdataSDK (`zoomdata-client.js`) to create data query objects, the host application constructs the entire query configuration — fields, metrics, filters, time ranges — programmatically. This gives you complete control over what is queried, effectively making every part of the configuration a "parameter."

```javascript
// Host app controls all query parameters
const userThreshold = getUserSelectedThreshold();  // e.g., 1000
const userRegion = getUserSelectedRegion();         // e.g., 'EMEA'

const query = client.createQuery({
  sourceId: 'source-id',
  fields: [
    { name: 'product', limit: 50, sort: { dir: 'desc', name: 'count' } },
    { name: 'revenue', func: 'sum' }
  ],
  filters: [
    {
      type: 'ATTRIBUTE',
      path: 'region',
      operation: 'IN',
      values: [userRegion]
    },
    {
      type: 'COMPARISON',
      path: 'order_value',
      operation: 'GT',
      value: userThreshold
    }
  ]
});

const result = await query.run();
// Render with your own charting library
```

**Limitations:** You are not embedding a Composer dashboard — you are building a custom app that uses Composer as a data engine. The user does not see Composer's dashboard UI, filters, or interactivity.

### 18.5 Mechanism 4: Multiple Data Sources with Pre-Filtered Views

**Best for:** When different parameter values should show fundamentally different data slices and you can define them ahead of time.

Create multiple Composer data sources (or database views) — one per parameter value combination — and switch which data source or dashboard the embed renders based on the host app's context.

```javascript
const DASHBOARDS_BY_REGION = {
  'EMEA':  'dashboard-id-emea',
  'APAC':  'dashboard-id-apac',
  'AMER':  'dashboard-id-amer'
};

const selectedRegion = getHostAppRegion();
const dashboardId = DASHBOARDS_BY_REGION[selectedRegion];

const dashboard = await em.createComponent('dashboard', {
  dashboardId: dashboardId,
  originId: dashboardId,
  theme: '__platform__'
});

dashboard.render(container, { width: '100%', height: '100%' });
```

**Limitations:** Does not scale for many parameter values. Requires maintaining multiple dashboards or data sources. Best suited for a small, fixed set of parameter values.

### 18.6 Strategy Summary

| Mechanism | Passes Values Into | Affects Formulas | Runtime Dynamic | Requires Server Config |
|-----------|-------------------|-----------------|----------------|----------------------|
| Initial Filters | Row filtering | No | No (set at embed time) | No |
| EMBED/PUBLISH | Row filtering | No | Yes | No |
| Admin-Defined Functions | SQL template expressions | Yes (via field references) | No (static JSON) | Yes |
| ZoomdataSDK Queries | Full query config | N/A (custom app) | Yes | No |
| Multiple Dashboards | Dashboard selection | Indirect | Yes | No (but more dashboards) |
| Custom Chart Constant Variables | Custom chart rendering logic | Yes (chart-level) | Configurable per visual instance | No (custom chart dev) |
| Keysets | Cross-source filtering by value sets | No | Yes (API-updatable) | No |
| Action Templates | Outbound to external apps | No (outbound only) | Yes | Admin privilege |
| Python Connector | Data source logic (arbitrary Python) | Yes (Python scripts) | Yes (script changes) | Yes (connector setup) |
| File Upload API | Data source content (CSV/JSON rows) | No (raw data) | Yes (REST API append/replace) | No (built-in) |
| Data Writer Microservice | Persistent data storage | Yes (landing data) | Yes (REST API streaming) | Yes (microservice) |

### 18.7 Recommended Approach for Common Scenarios

**"Filter the dashboard to show only this tenant's data"**
→ Use `initialFilters` at embed time (Section 18.2)

**"Let the user pick a region and update the dashboard live"**
→ Use `EMBED/PUBLISH` filter injection (Section 18.2)

**"Apply a custom calculation that references multiple columns"**
→ Use Admin-Defined Functions (Section 18.3) — define the SQL formula once, users apply it in derived fields

**"Pass a named constant (e.g., API key, label, threshold) into a custom visualization"**
→ Use Custom Chart Constant Variables (Section 19) — define string/boolean/text constants in the chart definition, access via `controller.variables`

**"Filter across data sources using a saved set of values"**
→ Use Keysets (Section 21) — create a named collection of values, apply as a filter to any visual with a matching field, update via API

**"Trigger an external action with data context from a visual"**
→ Use Action Templates (Section 20) — push selected field data to an external URL with user context variables

**"Provide a fully dynamic data source driven by custom logic"**
→ Use the Python Connector (Section 22) — each Python function becomes a data source, with full control over data generation and transformation

**"Push parameter values or reference data into Composer at runtime via API"**
→ Use the File Upload REST API (Section 24) — POST JSON to append/replace rows in an uploaded data source. Combine with Fusion (cross-source joins) or Keysets for parameter-table patterns

**"Land streaming or real-time data into Composer for analysis"**
→ Use the Data Writer Microservice (Section 23) — receive data via REST API, queue it, and persist to a relational database as a standard data source

**"Pass an arbitrary scalar (like a discount rate) into a formula at runtime"**
→ Multiple approaches: (a) write the scalar to a file-upload data source via the Upload API and reference it via a Fusion join or Admin-Defined Function, (b) use a Python Connector function that reads the parameter from an external source, (c) use ZoomdataSDK to build a fully custom query experience, or (d) build a custom chart that reads the scalar from `controller.variables`

**"Build a completely custom UI with Composer as the data engine"**
→ Use ZoomdataSDK data query objects (Section 18.4)

---

## 19. Custom Chart Controller API

The Composer Custom Chart API exposes a global `controller` object that provides the interface between Composer and custom-built visualizations. Custom charts are developed using the Custom Chart CLI and can be deployed to any Composer instance.

### 19.1 Controller Properties

| Property | Type | Description |
|----------|------|-------------|
| `controller.element` | HTMLElement | The `<div>` container Composer provides for the chart to render into |
| `controller.dataAccessors` | Object | Configuration for each query variable (group-by fields, metrics). Properties map to the data accessor definitions in the chart's variable config |
| `controller.source` | Object | Information about the current Composer data source the visual is connected to |
| `controller.variables` | Object | Named constant variables defined in the chart's variable configuration. Each property corresponds to a constant variable name |

### 19.2 Constant Variables

Constant variables are named values (string, boolean, or text) defined in a custom chart's variable configuration. They allow chart authors to expose configurable parameters that dashboard designers can set per visual instance — without modifying the chart code.

**Accessing constant variables:**

```javascript
// In your custom chart's controller handler
var apiKey = controller.variables['API Key'];
var showLegend = controller.variables['Show Legend'];
var threshold = controller.variables['Threshold Value'];

// Use these values in your chart rendering logic
if (showLegend) {
  renderLegend(controller.element);
}
```

Each constant variable is defined in the chart's variable definition with a name, type, and optional default value. When a dashboard designer places the custom chart on a dashboard, they can configure these constant values in the visual's settings panel.

### 19.3 Data Accessors (Query Variables)

Data accessors define how the chart maps query results to visual elements. They are configured via `controller.dataAccessors` and represent the group-by dimensions and metrics the chart expects.

```javascript
// Access group-by field configuration
var groupAccessor = controller.dataAccessors['Group By'];

// Access metric configuration  
var metricAccessor = controller.dataAccessors['Size'];
```

### 19.4 Controller Event Handlers

Custom charts override controller methods to react to lifecycle events:

- **Data updates** — new query results arrive
- **Chart resizing** — the container dimensions change (use `controller.resize`)
- **Query errors** — a data query fails

### 19.5 Relevance to Parameterization

Constant variables are the closest Composer-native mechanism to "view parameters" for custom visualizations. A custom chart can define named constants like "Threshold", "Multiplier", or "Display Mode" that:

- Are configured per visual instance by the dashboard designer
- Are accessible in the chart's JavaScript at render time
- Can influence how the chart processes and displays data

**Limitation:** Constant variables are set at design time in the dashboard editor — they are not currently exposed for dynamic override via the embed API's component configuration. The values are baked into the dashboard definition. To change them, the dashboard designer must edit the visual's settings in the Composer UI.

---

## 20. Action Templates

Action templates define integrations that push data from Composer visuals to external applications. They are configured by administrators and become available to users on visuals connected to the specified data source.

### 20.1 Action Template Properties

| Property | Description |
|----------|-------------|
| **Name** | Unique identifier for the action template |
| **Target URL** | URL of the external application to receive the data |
| **Data Source** | The Composer data source configuration the action is linked to |
| **Fields** | Selected fields from the data source whose values are collected when the action is invoked |
| **Row Limit** | Maximum number of rows submitted (1–999,999,999) |
| **Enable Action** | Toggle to enable or disable the action |

### 20.2 Context Variables

Action template Target URLs support context variable substitution:

| Variable | Description |
|----------|-------------|
| `${User.composerUserName}` | The username of the user invoking the action |
| `${User.accountId}` | The account ID of the user invoking the action |

**Example Target URL:**

```
https://myapp.example.com/api/action?user=${User.composerUserName}&account=${User.accountId}
```

### 20.3 Requirements

- Must be logged in as an administrator or a user with the **Manage Action Templates** privilege
- Configured via the **Actions** page in the Composer UI menu

### 20.4 Relevance to Parameterization

Action templates are an **outbound** mechanism — they push data from Composer to external apps, not the other way around. However, they are relevant in parameterization workflows where:

- A user action in Composer should trigger a process in an external system (e.g., creating a ticket, sending an alert, initiating a workflow)
- The external system needs to know which user triggered the action and what data context they were viewing
- The context variables (`${User.composerUserName}`, `${User.accountId}`) provide user identity for the external system to look up additional context

Action templates do not pass values *into* Composer queries or formulas.

---

## 21. Keysets

Keysets are named collections of unique data values that can be saved, managed, and applied as filters across visuals and data sources. They enable multipass and cross-source filtering workflows.

### 21.1 Overview

A keyset is created by selecting a single field (the **key field**) from a visual's data. The keyset captures the unique values of that field, optionally filtered by any visual-level filters already applied. For example, from a visual filtered to show only Virginia airports, creating a keyset on the "airport code" field produces a collection of only Virginia airport codes.

### 21.2 Creating Keysets

Keysets can be created from three sources:

- **From the visual result set** — select a field, keyset captures all unique values currently visible
- **From a data point** — select specific data point(s) in a visual
- **From a CSV file** — upload values directly

### 21.3 Applying Keysets as Filters

Once created, a keyset can be applied as a filter to any visual — including visuals from **different data sources** — as long as the target visual's data source contains a field storing the same kind of data as the keyset's key field.

**Filter execution order** when multiple filter types are combined on a visual:

1. **Row-level filters** (including wildcard filters) — applied first
2. **Keyset filters** — applied second
3. **Group filters** — applied last, on the aggregated result set

### 21.4 Updating Keysets via API

Keyset values can be updated programmatically using the API by uploading new values from a CSV file. This makes keysets a viable mechanism for host-application-driven filtering:

- **Upload Keyset Data From a CSV File Using the API** — create/replace keyset values
- **Update Keyset Values From a CSV File Using the API** — modify existing keyset values

### 21.5 Managing Keysets

- Keysets can be updated at any time with new values
- Keysets can be deleted when no longer needed
- The interactivity sidebar controls whether keyset creation and management is available on a visual (see Section 11)

### 21.6 Relevance to Parameterization

Keysets offer a unique parameterization capability that other mechanisms do not:

- **Cross-source filtering** — a keyset created from one data source can filter visuals from a completely different data source, as long as both share a compatible field
- **API-updatable** — the host application can programmatically update keyset values via CSV upload, making them a dynamic filtering mechanism controlled from outside Composer
- **Multipass analysis** — use the results of one query to filter another, enabling drill-down and linked analysis workflows

**Example workflow:** A host application maintains a list of "active customer IDs" in a keyset. When the customer list changes, the host app updates the keyset via the API. All visuals filtered by that keyset automatically reflect the updated customer list on their next query.

**Limitation:** Keysets filter by discrete value sets, not by scalar parameters or formula inputs. They are best suited for scenarios where the parameter is a list of values to include/exclude.

---

## 22. Python Connector

The Python connector allows arbitrary Python scripts to serve as Composer data sources. Each public function in the script becomes a separate data entity, giving developers full programmatic control over the data returned to Composer.

### 22.1 How It Works

- Provide a Python script as the connection parameter
- Each **public function** definition becomes a separate data source entity
- Private functions (prefixed with `_`) are not exposed as data sources
- The connector operates in **raw data mode only** — no push-down of aggregations
- Python is executed via JEP (Java Embedded Python) in the same process as the Java connector

### 22.2 Return Value Conventions

Python functions can return data in several formats:

| Return Type | Description |
|-------------|-------------|
| Pandas DataFrame | Full DataFrame support |
| Dictionary | Key = column name (string), value = list of values: `{"col1": [1, 2], "col2": ["a", "b"]}` |
| List of dictionaries | Each dict is a row: `[{"col1": 1, "col2": "a"}, {"col1": 2, "col2": "b"}]` |
| List of lists | Each inner list is a row: `[[1, 2], [3, 4]]` |
| List | Single column with index: `[1, 2, 3, 4]` |
| Single value | Single value of any supported type: `return 1` or `return decimal.Decimal("3.14")` |

### 22.3 Type Conversion

| Python Type | Composer Field Type |
|-------------|-------------------|
| `str` | STRING |
| `int` | INTEGER |
| `float` | DOUBLE |
| `decimal.Decimal` | DOUBLE |
| `datetime.date` | DATE |
| `datetime.datetime` | DATE |
| arbitrary object | STRING |

### 22.4 Important Constraints

**No top-level state:** Function invocation happens in a subprocess (forked from the Java process). Global variables set at the top level are not available inside functions.

```python
# This will NOT work — x is not available in the subprocess
x = 40
def side_effect():
    x = x + 1  # UnboundLocalError
    return {"result": [x]}

# This WILL work — self-contained function
def get_data():
    x = 40
    return {"result": [x + 1]}
```

**Limited filesystem access:** The container runs as non-root. Write access is available only to: `/opt/zoomdata/logs`, `/opt/zoomdata/temp`, `/opt/zoomdata/lib`, `/opt/zoomdata/wrappers`.

**No stdout/stderr:** `print()` output is not preserved.

**Reserved names to avoid:** `__convert`, `__convert_list_of_dicts_to_dict_of_lists`, `f`, `__fork`, `__emulate`, `all_functions`, and imported modules: `pandas`, `numbers`, `datetime`, `multiprocessing`, `queue`, `inspect`, `types`.

**Performance:** Use filter operations to minimize data returned. The raw data mode means all aggregation happens in Composer, not at the source.

### 22.5 Relevance to Parameterization

The Python connector is the most flexible data source mechanism in Composer for parameterization scenarios:

- **Dynamic data generation:** A Python function can read parameters from an external source (file, environment variable, API call, database) and return computed data
- **Custom transformations:** Apply any Python logic — mathematical formulas, statistical models, lookups — before returning data to Composer
- **External integration:** Functions can call external APIs, read from message queues, or query other databases to assemble data

**Example — parameter-driven data source:**

```python
import json

def revenue_with_adjustment():
    # Read parameter from a config file or external API
    with open('/opt/zoomdata/temp/params.json') as f:
        params = json.load(f)
    
    adjustment_factor = params.get('adjustment_factor', 1.0)
    
    # Query base data and apply the parameter
    # (in practice, connect to your actual data source here)
    return {
        "product": ["Widget A", "Widget B", "Widget C"],
        "base_revenue": [100000, 250000, 175000],
        "adjusted_revenue": [
            100000 * adjustment_factor,
            250000 * adjustment_factor,
            175000 * adjustment_factor
        ]
    }
```

**Limitation:** The script itself is static (deployed as a connection parameter). To change the parameter values, you update an external resource the script reads from — not the script itself. This introduces a dependency on an external parameter store.

---

## 23. Data Writer Microservice

The Data Writer microservice is a Composer component that writes data to a relational database, providing persistent storage for several key workflows.

### 23.1 Architecture

The Data Writer consists of three components:

1. **REST API** — receives data write requests
2. **Message queue** — manages backflow and ordering
3. **Writable data connectors** — persist data to the target database

### 23.2 Use Cases

**User-uploaded files:** When users upload CSV/TSV files via the Composer UI, the Data Writer persists the file contents to a PostgreSQL database. The uploaded data then behaves like any other data source, supporting push-down processing and derived fields.

**Landing streaming data:** Any streaming engine (Kafka, Spark Streaming, Storm, Apex, NiFi, Kinesis, etc.) can push data to the Data Writer via the REST API. Data is queued and written to persistent storage, making it available for both live mode and historical analysis. This approach provides greater functionality than connecting directly to a live stream and requires less infrastructure than a full lambda architecture.

**Keyset storage:** The Data Writer stores keyset data (ordered, filtered sets of key values) in a relational database for reuse in cross-source filtering (see Section 21).

### 23.3 Relevance to Parameterization

The Data Writer is the underlying infrastructure that makes several parameterization patterns possible:

- File Upload API (Section 24) writes through the Data Writer
- Keysets are stored via the Data Writer
- Streaming data landing enables near-real-time parameter updates — push new parameter values via the REST API and they become available as data source rows

---

## 24. File Upload Data Sources (CSV/JSON/TSV via REST API)

Composer can create data sources from uploaded flat files (CSV, JSON, TSV) with a maximum size of 500 MB. Uploaded data is stored in a PostgreSQL database and is accessible as a standard data source with full feature support.

### 24.1 Supported Formats and Storage

- **Formats:** CSV, JSON, TSV
- **Max file size:** 500 MB
- **Storage:** PostgreSQL database (via the Data Writer microservice)
- **Type inference:** First 1,000 records determine field types (NUMBER vs INTEGER). Sort data to ensure decimal values appear in the first 1,000 rows.

### 24.2 Feature Support

File upload data sources support a rich set of Composer features:

| Feature | Supported |
|---------|-----------|
| Admin-Defined Functions | Yes |
| Derived Fields (Row-Level Expressions) | Yes |
| Custom SQL Queries | Yes |
| Pushdown Joins for Fusion Data Sources | Yes |
| Group By Multiple Fields / Time / UNIX Time | Yes |
| Histograms | Yes |
| Distinct Counts | Yes |
| Live Mode and Playback | Yes |
| Wildcard Filters (case-sensitive and insensitive) | Yes |
| Box Plots | Yes |
| Schemas | Yes |
| TLS | Yes |
| Last Value | Yes |

Notably, file upload sources support **Admin-Defined Functions**, **Derived Fields**, **Custom SQL**, and **Fusion joins** — making them a capable foundation for parameter-table patterns.

### 24.3 Upload API

The Upload API allows programmatic management of file upload data source content. It supports two operations:

**Append data:**

```bash
curl -v --user <username>:<password> \
  'https://<Your_Composer_Server>/composer/api/upload/<YourDataSourceId>' \
  -X POST \
  -H "Content-Type: application/vnd.composer.v3+json" \
  -d '[{"price":100.5,"venue_id":"V678","venue_name":"Pizza Barn"}]' \
  --insecure
```

The API accepts an array of JSON objects. Field types must match those used when the source was originally created.

**Clear all previously uploaded data:**

```bash
curl -v --user <username>:<password> \
  'https://<Your_Composer_Server>/api/upload/<YourDataSourceId>' \
  -X DELETE \
  --insecure
```

**Replace data** (clear + append): Call DELETE first, then POST with new data.

### 24.4 UI Workflow

- **Upload:** Create a data source → Files tab → Upload New File → set display name, delimiter, column headers → Save
- **Edit/Replace:** Edit data source → select entity → Edit File → browse for new file → enable/disable Replace checkbox → Preview → Save
- **API Endpoints dialog:** Edit data source → select entity → API Endpoints → copy example cURL commands with pre-filled source ID

### 24.5 Relevance to Parameterization

The File Upload API is one of the most practical mechanisms for runtime parameterization in Composer:

**Parameter table pattern:**
1. Create a file upload data source with a simple schema (e.g., `param_name`, `param_value`)
2. Upload initial parameter values via CSV or the API
3. Use Fusion (cross-source joins) to join the parameter table with your main data source
4. Derived fields or Admin-Defined Functions can reference the parameter columns
5. To change a parameter value at runtime, call the Upload API: DELETE to clear, POST to write the new value
6. Dashboards referencing this data source reflect the updated parameter on their next query

**Example — runtime discount rate parameter:**

```bash
# Step 1: Clear existing parameter
curl -v --user service:Password01! \
  'https://your-server.com/composer/api/upload/param-source-id' \
  -X DELETE --insecure

# Step 2: Write new parameter value
curl -v --user service:Password01! \
  'https://your-server.com/composer/api/upload/param-source-id' \
  -X POST \
  -H "Content-Type: application/vnd.composer.v3+json" \
  -d '[{"param_name":"discount_rate","param_value":0.15}]' \
  --insecure
```

A dashboard with a Fusion data source joining the main sales data with this parameter source can now use the `param_value` field in derived fields or Admin-Defined Functions to compute `revenue * (1 - param_value)`.

**Advantages over other mechanisms:**
- No server-side file deployment (unlike Admin-Defined Functions)
- Works with standard Composer features (derived fields, Fusion, SQL)
- Fully API-driven — the host application controls parameter values programmatically
- Parameter changes are persistent (stored in PostgreSQL)

**Limitations:**
- Not instantaneous — data goes through the Data Writer queue
- Requires Administer Sources or Create New Data Sources privilege
- Parameter changes affect all users viewing the dashboard (not per-user unless combined with row-level security or user-specific parameter sources)
