---
title: MCP
hidden: false
---
The Sensible Model Context Protocol (MCP) server enables AI-powered code editors like Cursor and Windsurf, plus general-purpose tools like Claude Desktop, to interact directly with your Sensible API and documentation.

## What is MCP?

Model Context Protocol (MCP) is an open standard that allows AI applications to securely access external data sources and tools. The Sensible MCP server provides AI agents with:

* **Direct API access** to Sensible functionality
* **Documentation search** capabilities
* **Real-time data** from your Sensible account
* **Code generation** assistance for Sensible integrations

## Sensible MCP Server Setup

Sensible hosts a remote MCP server at `https://docs.sensible.so/mcp`. Configure your AI development tools to connect to this server.&#x20;

If you want to search and read the Sensible docs, including the API specification, you can configure the MCP server without authorization. For example in Claude Code, add the following entry to `~/.claude.json`:

```json
{
  "mcpServers": {
    "sensible-docs": {
      "url": "https://docs.sensible.so/mcp"
    }
  }
}
```

&#x20;If you want to call the Sensible API using the MCP server, configure authorization for the server. For example, in Claude Code, add the following entry to `~/.claude.json`, and specify the `SENSIBLE_API_KEY` variable in your environment using the value of your [API key](https://app.sensible.so/account/?t=api_keys):

```json
{
  "mcpServers": {
    "sensible-docs": {
      "type": "http",
      "url": "https://docs.sensible.so/mcp",
      "headers": {
        "authorization": "Bearer ${SENSIBLE_API_KEY}"
      }
    }
}
```

## Testing Your MCP Setup

Once configured, you can test your MCP server connection:

1. **Open your AI editor** (Cursor, Windsurf, etc.)
2. **Start a new chat** with the AI assistant
3. **Ask about Sensible** - try questions like:
   * "How do I \[common use case]?"
   * "Show me an example of \[API functionality]"
   * "Create a \[integration type] using Sensible"

The AI should now have access to your Sensible account data and documentation through the MCP server.
