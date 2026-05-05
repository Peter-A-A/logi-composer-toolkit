# Logi Composer MCP Server

An MCP (Model Context Protocol) server that exposes the Logi Composer REST API as 133 tools (132 auto-generated endpoints + 1 generic passthrough).

## Quick Start

### 1. Install dependencies

```bash
cd logi-composer-mcp
pip install -r requirements.txt
```

Or with a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

### 2. Configure

Copy the example config and add your credentials:

```bash
cp .env.example .env
```

Edit `.env` and set:
- `COMPOSER_USERNAME` — your Composer username (required)
- `COMPOSER_PASSWORD` — your Composer password (required)
- `COMPOSER_HOST` — your server hostname, e.g. `http://localhost:8008` or `https://uat.logi-symphony.com`
- `COMPOSER_BASE_PATH` — `/composer` for local installs, `/discovery` for cloud/UAT

### 3. Run the server

```bash
python server.py
```

The server communicates over stdio, which is the standard MCP transport.

## Connecting to Claude

### Claude Desktop / Cowork

Add this to your Claude Desktop config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "logi-composer": {
      "command": "python",
      "args": ["/full/path/to/logi-composer-mcp/server.py"],
      "env": {
        "COMPOSER_USERNAME": "admin",
        "COMPOSER_PASSWORD": "password",
        "COMPOSER_HOST": "http://localhost:8008",
        "COMPOSER_BASE_PATH": "/composer"
      }
    }
  }
}
```

### Claude Code

```bash
claude mcp add logi-composer python /full/path/to/logi-composer-mcp/server.py
```

## Available Tools

The server exposes 133 tools covering:

- **Accounts** — load, create, update, delete accounts and members
- **Users** — manage users and user segregation permissions
- **Groups** — list and update groups
- **Connections** — manage connections, connection types, schema configuration
- **Connectors** — retrieve and update connectors
- **Data Sources** — full CRUD on sources, fields, custom metrics, dictionaries, cache settings, global settings, visual types, unique keys
- **Source Security** — row-level filters, field-level security, custom metric security, attribute settings
- **Dashboards** — manage dashboards, reports, interactivity, comments
- **Visuals** — retrieve and update visuals
- **Visual Types** — manage visual type definitions
- **Permissions (ACLs)** — bulk permission assignment on dashboards, visuals, sources
- **Filter Sets** — manage saved filters
- **Uploads** — manage data uploads
- **Customization** — themes, branding, branding extensions
- **Alerts & Actions** — manage alerts and action templates
- **Calendars, Snippets, Keysets, Quota** — additional management endpoints
- **System** — activity logging, toggles, global security config
- **Generic Passthrough** — `composer_api_request` for any endpoint not covered above

## Authentication

The server uses HTTP Basic authentication. Set your username and password in `.env` or pass them as environment variables.

## Notes

- The spec was generated from the OpenAPI 3.1.0 definition at `/discovery/api-docs`
- The original spec was truncated at ~109K chars; the generic `composer_api_request` tool covers any missing endpoints
- For PUT/POST endpoints, pass the request body as a `body` dict parameter
