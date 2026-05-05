# Logi Composer Toolkit

Reference documentation, MCP server, and examples for working with Logi Composer (Logi Symphony) — insightsoftware's embedded analytics platform.

## What's included

### Documentation (`docs/`)
- **Embedding Reference** — comprehensive guide to embedding dashboards and visuals using `initComposerEmbedManager`, Trusted Access, filtering, pub/sub, data queries, and more
- **REST API Reference** — structured reference for all 175 API endpoints, organized by category
- **OpenAPI Spec** — raw OpenAPI 3.1.0 JSON specification

### MCP Server (`mcp-server/`)
A Python MCP server that lets Claude call the Composer REST API directly. Exposes 133 tools covering accounts, users, groups, connections, sources, dashboards, visuals, permissions, and more.

See `mcp-server/USER_GUIDE.md` for setup instructions.

### Examples (`examples/`)
- **Dashboard Embed** — working HTML page demonstrating a Composer dashboard embed with Trusted Access authentication

## Using with Claude

This repo is designed to be used as project knowledge in Claude projects. Add the repo (or specific files) to give Claude the context it needs to:

- Answer questions about the Composer embedding API
- Answer questions about the REST API
- Generate embedded dashboard/visual code
- Call API endpoints via the MCP server

The `CLAUDE.md` file at the root acts as an index — it tells Claude what's in each folder and when to reference which file.

## Quick links

| I want to... | Read this |
|---|---|
| Embed a dashboard | `docs/Logi-Composer-Symphony-Embedding-Reference.md` |
| See a working embed example | `examples/composer-dashboard-embed.html` |
| Look up an API endpoint | `docs/Logi Composer REST API Reference.md` |
| Set up the MCP server | `mcp-server/USER_GUIDE.md` |
| Understand the MCP server code | `mcp-server/README.md` |
