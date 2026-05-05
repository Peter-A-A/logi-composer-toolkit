# Logi Composer MCP Server — User Guide

This guide walks you through setting up and using the Logi Composer MCP Server, which lets Claude call the Composer REST API on your behalf. Instead of writing curl commands or switching to Postman, you can ask Claude to query sources, inspect dashboards, manage users, and more — all through natural conversation.

## What is this?

The Logi Composer MCP Server is a lightweight Python process that runs on your machine and acts as a bridge between Claude and the Composer REST API. It exposes 133 tools (one per API endpoint, plus a generic passthrough) that Claude can call directly during a conversation.

MCP (Model Context Protocol) is the standard Claude uses to connect to external tools and services.

## Prerequisites

Before you start, make sure you have:

- **Python 3.10+** installed on your machine
- **Claude Desktop** (Mac or Windows) — download from [claude.ai/download](https://claude.ai/download)
- **Composer credentials** — a username and password that can authenticate against your Composer instance via Basic auth
- **Network access** to your Composer instance (local or cloud)

## Installation

### 1. Get the project files

Copy the `logi-composer-mcp` folder to a location on your machine. You need these files:

```
logi-composer-mcp/
├── server.py           # The MCP server (133 tools)
├── CLAUDE.md           # Context file that helps Claude use the API effectively
├── requirements.txt    # Python dependencies
├── .env.example        # Configuration template
├── README.md           # Technical reference
└── USER_GUIDE.md       # This file
```

### 2. Install Python dependencies

Open a terminal, navigate to the project folder, and run:

```bash
cd /path/to/logi-composer-mcp
pip install -r requirements.txt
```

If you prefer an isolated environment:

```bash
python3 -m venv venv
source venv/bin/activate    # Mac/Linux
# venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### 3. Create your configuration file

```bash
cp .env.example .env
```

Open `.env` in a text editor and fill in your values:

```dotenv
# Your Composer login credentials
COMPOSER_USERNAME=your-username
COMPOSER_PASSWORD=your-password

# Your Composer server (no trailing slash)
COMPOSER_HOST=https://uat.logi-symphony.com

# Base path: /discovery for cloud/UAT, /composer for local installs
COMPOSER_BASE_PATH=/discovery

# Set to false for local HTTP or self-signed certs
COMPOSER_VERIFY_SSL=true

# Request timeout in seconds
COMPOSER_TIMEOUT=30
```

**Common configurations:**

| Environment | COMPOSER_HOST | COMPOSER_BASE_PATH | COMPOSER_VERIFY_SSL |
|---|---|---|---|
| Local install | `http://localhost:8008` | `/composer` | `false` |
| UAT (cloud) | `https://uat.logi-symphony.com` | `/discovery` | `true` |

### 4. Connect to Claude Desktop

You need to tell Claude Desktop where to find the MCP server. Edit the Claude Desktop config file:

**Mac:**
```bash
open -a TextEdit ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Windows:**
Open `%APPDATA%\Claude\claude_desktop_config.json` in any text editor.

Add an `mcpServers` block. If the file already has content, merge it — don't replace existing settings:

```json
{
  "mcpServers": {
    "logi-composer": {
      "command": "python3",
      "args": ["/full/path/to/logi-composer-mcp/server.py"]
    }
  }
}
```

Replace `/full/path/to/` with the actual path on your machine. To find it, run `pwd` in terminal from the project folder.

**Note:** You can also pass credentials directly here instead of using a `.env` file:

```json
{
  "mcpServers": {
    "logi-composer": {
      "command": "python3",
      "args": ["/full/path/to/logi-composer-mcp/server.py"],
      "env": {
        "COMPOSER_USERNAME": "your-username",
        "COMPOSER_PASSWORD": "your-password",
        "COMPOSER_HOST": "https://uat.logi-symphony.com",
        "COMPOSER_BASE_PATH": "/discovery"
      }
    }
  }
}
```

Pick one approach — `.env` file or `env` block in the config — you don't need both.

### 5. Restart Claude Desktop

Quit Claude Desktop completely (Cmd+Q on Mac, not just close the window) and reopen it. The MCP server will start automatically when Claude Desktop launches.

### 6. Verify the connection

Start a new conversation in Claude and ask:

> "Use the logi-composer tools to get the branding configuration"

If everything is working, Claude will call the API and return your Composer instance's branding settings. If you see a 401 error, double-check your credentials. If you see a connection error, make sure your Composer instance is reachable.

## How to use it

Once connected, just talk to Claude naturally. Here are some examples of what you can ask:

### Exploring your environment

- "List all user groups in Composer"
- "Get the details for source ID abc123"
- "What fields are available in source xyz?"
- "Show me the branding configuration"
- "What visual types are available for this source?"

### Inspecting dashboards

- "Load dashboard ID def456 and show me its structure"
- "What reports are on this dashboard?"
- "Show the interactivity settings for this dashboard"
- "Are there any comments on this dashboard?"

### Managing security

- "Show me the security settings for source abc123"
- "What forced filters are applied to this source?"
- "What are the field-level security settings?"

### User and account management

- "Load user ID user789"
- "List the members of account xyz"
- "Show me the user segregation permissions for this SID"

### Custom API calls

If you need to call an endpoint that isn't covered by the specific tools (or if you want full control over the request), ask Claude to use the generic passthrough:

- "Call GET /api/sources with no parameters using the composer passthrough"
- "Make a POST to /api/customization/themes/activate with this body: {\"id\": \"648c48bf3f0705533ca5652a\"}"

## Tips for getting the best results

1. **Provide IDs when you have them.** Most endpoints require resource IDs. If you know the source ID or dashboard ID, include it in your request.

2. **Chain requests naturally.** You can say things like "Get the source details, then show me its fields" and Claude will make multiple API calls in sequence.

3. **Ask Claude to explain responses.** The API returns JSON. You can ask Claude to summarize, compare, or extract specific information from the results.

4. **Use the CLAUDE.md file.** If you're using this MCP server in a Claude Code project or another Claude setup, include the `CLAUDE.md` file in your project. It gives Claude context about how resources relate to each other and common workflows.

## Troubleshooting

### "All connection attempts failed"

The MCP server isn't running. Try:
- Restart Claude Desktop (Cmd+Q, then reopen)
- Check that the path to `server.py` in your config is correct
- Verify Python 3.10+ is installed: `python3 --version`
- Check that dependencies are installed: `pip list | grep mcp`

### 401 Unauthorized

Your credentials are wrong or expired. Check the `COMPOSER_USERNAME` and `COMPOSER_PASSWORD` in your `.env` file or Claude Desktop config.

### 415 Unsupported Media Type

This was a known issue in an earlier version of the server that sent unnecessary headers on GET requests. Make sure you have the latest `server.py`.

### Connection refused / timeout

- Verify your Composer instance is running and accessible
- Check `COMPOSER_HOST` is correct (no trailing slash)
- Check `COMPOSER_BASE_PATH` matches your setup (`/composer` vs `/discovery`)
- For local instances, make sure `COMPOSER_VERIFY_SSL=false`

### Server loads but tools aren't visible

- Make sure the config file path points to the correct `server.py`
- Check for JSON syntax errors in `claude_desktop_config.json`
- Restart Claude Desktop after any config changes

## API Coverage

The server covers 132 endpoints across these categories: accounts, users, groups, connections, connectors, sources (fields, security, cache, custom metrics, dictionaries), dashboards (reports, interactivity, comments), visuals, visual types, permissions/ACLs, filter sets, uploads, customization/themes/branding, alerts, actions, calendars, snippets, quota, keysets, and system settings.

The API spec was generated from the OpenAPI 3.1.0 definition at `/discovery/api-docs`. A generic passthrough tool (`composer_api_request`) is included for any endpoints not covered by the specific tools.
