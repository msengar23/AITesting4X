REsearch on the Commands:

 /mcp — MCP Server Management

  /mcp manages MCP (Model Context Protocol) servers — external tools and data sources that extend Command Code's capabilities. When you
  run /mcp, it opens an interactive browser to manage your connected MCP servers.

  What MCP servers do

  They let Command Code talk to external services (databases, APIs, file systems, etc.) as if they were native tools. For example, a
  GitHub MCP server lets the agent create issues, read PRs, and search repos directly.

  Adding MCP servers

  Via CLI (cmdc):

  # HTTP transport
    cmdc mcp add --transport http notion https://mcp.notion.com/mcp

    # stdio transport (local process)
    cmdc mcp add github -- npx -y @modelcontextprotocol/server-github

  Via .mcp.json (hand-written, checked into version control):

  {
      "mcpServers": {
        "github": {
          "command": "npx",
          "args": ["-y", "@modelcontextprotocol/server-github"]
        }
         }
    }

  Configuration scopes (lowest to highest precedence)

  ┌─────────┬─────────────────────────────────────────┬─────────────────────────────────────────┐
  │ Scope   │ Location                                │ Purpose                                 │
  ├─────────┼─────────────────────────────────────────┼─────────────────────────────────────────┤
  │ User    │ ~/.commandcode/mcp.json                 │ Available across all projects           │
  ├─────────┼─────────────────────────────────────────┼─────────────────────────────────────────┤
  │ Project │ <project>/.mcp.json                     │ Shared with the team, checked into git  │
  ├─────────┼─────────────────────────────────────────┼─────────────────────────────────────────┤
  │ Local   │ ~/.commandcode/projects/<slug>/mcp.json │ Private to your machine, not checked in │
  └─────────┴─────────────────────────────────────────┴─────────────────────────────────────────┘

  Local overrides project, project overrides user — so you can have team-wide servers plus your own private additions.
  Managing connections

   Run /mcp to open the interactive management panel where you can add, remove, enable/disable, and inspect connected MCP servers. No
  restart is needed when you add or remove servers — they're discovered automatically.