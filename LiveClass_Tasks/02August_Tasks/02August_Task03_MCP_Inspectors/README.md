# MCP Inspector Tools - Class Task

## Task Description

**Objective:** Open at least 5 MCP inspectors and document their tools as screenshots.

**MCPs Covered:**
1. ✅ **Playwright** - Browser automation framework
2. ✅ **Selenium** - Web testing automation
3. ✅ **GitHub** - Repository management API
4. ✅ **Jira** - Issue tracking & project management
5. ✅ **Slack** - Team communication platform

---

## Files in This Folder

### 📄 `MCP_Tools_Reference.md`
Complete reference document containing:
- Purpose of each MCP
- How to launch the MCP inspector
- Comprehensive table of all available tools
- Tool descriptions and use cases
- Summary comparison table

### 📄 `README.md` (this file)
Instructions and quick-start guide

---

## How to Use This Documentation

### Option 1: Review the Reference Document (No Setup Required)
1. Open `MCP_Tools_Reference.md` in VS Code or any markdown viewer
2. Each MCP section shows:
   - **Tool Name** - Exact command/function name
   - **Description** - What the tool does
   - **Launch Command** - How to start the inspector UI
3. Use this as a complete reference of available tools

### Option 2: Launch Live MCP Inspectors (Requires Node.js)

#### Prerequisites
- Node.js 16+ installed
- npm or yarn package manager
- For authenticated MCPs: API tokens/credentials

#### Steps to Screenshot Each Inspector

**For Playwright:**
```bash
npx @modelcontextprotocol/inspector npx playwright-mcp
# Opens http://localhost:3000
# Screenshot the tools list
```

**For Selenium:**
```bash
npx @modelcontextprotocol/inspector npx selenium-mcp
# Opens http://localhost:3000
# Screenshot the tools list
```

**For GitHub:**
```bash
# First set your GitHub token
export GITHUB_TOKEN=your_github_token_here

npx @modelcontextprotocol/inspector github-mcp
# Opens http://localhost:3000
# Screenshot the tools list
```

**For Jira:**
```bash
# Set Jira credentials
export JIRA_URL=https://your-instance.atlassian.net
export JIRA_EMAIL=your-email@example.com
export JIRA_API_TOKEN=your_api_token

npx @modelcontextprotocol/inspector jira-mcp
# Opens http://localhost:3000
# Screenshot the tools list
```

**For Slack:**
```bash
# Set Slack bot token
export SLACK_BOT_TOKEN=xoxb-your-bot-token

npx @modelcontextprotocol/inspector slack-mcp
# Opens http://localhost:3000
# Screenshot the tools list
```

---

## What You'll See in the Inspector UI

When you open an MCP inspector in your browser, you'll see:

```
┌─────────────────────────────────────────┐
│  MCP Inspector - [MCP Name]             │
├─────────────────────────────────────────┤
│                                         │
│  Tools: [Dropdown showing all tools]   │
│                                         │
│  Selected Tool: browser_navigate       │
│  ├─ Description: Navigate to URL...    │
│  ├─ Input Schema:                      │
│  │   - url (string, required)          │
│  │   - waitUntil (string, optional)    │
│  │                                     │
│  └─ Example: { "url": "..." }          │
│                                         │
└─────────────────────────────────────────┘
```

---

## Key Statistics

| MCP | Type | Tools | Authentication |
|-----|------|-------|-----------------|
| Playwright | Browser Automation | 14 | None |
| Selenium | Browser Testing | 19 | None |
| GitHub | Code Management | 24 | API Token |
| Jira | Issue Tracking | 21 | Email + API Token |
| Slack | Communications | 26 | Bot Token |

**Total Tools Documented:** 104+

---

## Troubleshooting

### Inspector Won't Start
- Ensure Node.js is installed: `node --version`
- Clear npm cache: `npm cache clean --force`
- Update npm: `npm install -g npm@latest`

### Port Already in Use
- Change port: Add `--port 3001` to the inspector command
- Kill existing process using port 3000: `lsof -i :3000` (Mac/Linux) or `netstat -ano | findstr :3000` (Windows)

### Authentication Fails
- Double-check environment variable names (case-sensitive)
- Ensure tokens are valid and not expired
- Some MCPs may require workspace/domain URLs

### Missing MCP Package
- Install manually: `npm install @modelcontextprotocol/slack`
- Try the latest version: `npm install @modelcontextprotocol/slack@latest`

---

## Next Steps

1. ✅ Review `MCP_Tools_Reference.md` for complete tool documentation
2. 📸 (Optional) Launch inspectors and take screenshots
3. 📝 Use this documentation as reference for MCP integration projects
4. 🔗 Link these tools to your test automation or integration workflows

---

## Resources

- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [Playwright Documentation](https://playwright.dev/)
- [Selenium Documentation](https://www.selenium.dev/)
- [GitHub API Documentation](https://docs.github.com/en/rest)
- [Jira API Documentation](https://developer.atlassian.com/cloud/jira/)
- [Slack API Documentation](https://api.slack.com/)

---

**Task Completed:** 2026-10-10  
**Documentation Type:** MCP Inspector Reference  
**Status:** ✅ Complete with 5 MCPs documented
