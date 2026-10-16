# MCP Inspector - Sequential Access (One at a Time)

**Access URL for all MCPs:** `http://127.0.0.1:6274`

---

## 📋 Instructions

Run each command below one at a time in PowerShell. After each starts:
1. Open browser to `http://127.0.0.1:6274`
2. Screenshot the tools panel
3. Close with **Ctrl+C** when done
4. Move to next MCP

---

## MCP #1: Playwright

```powershell
npx @modelcontextprotocol/inspector npx @playwright/mcp@latest
```

**Browser:** `http://127.0.0.1:6274`

**Tools to capture:**
- browser_navigate
- browser_click
- browser_take_screenshot
- browser_get_page_content
- browser_wait_for_selector

**Close:** Press `Ctrl+C` in terminal when done

---

## MCP #2: Selenium

```powershell
npx @modelcontextprotocol/inspector npx selenium-mcp@latest
```

**Browser:** `http://127.0.0.1:6274`

**Tools to capture:**
- start_browser
- navigate
- find_element
- click_element
- take_screenshot

**Close:** Press `Ctrl+C` in terminal when done

---

## MCP #3: GitHub

Set token first, then run:

```powershell
$env:GITHUB_TOKEN = "<YOUR_GITHUB_TOKEN>"
npx @modelcontextprotocol/inspector github-mcp@latest
```

**Browser:** `http://127.0.0.1:6274`

**Tools to capture:**
- search_repositories
- create_issue
- create_pull_request
- search_code
- get_file_contents

**Close:** Press `Ctrl+C` in terminal when done

---

## MCP #4: Jira

Set credentials first, then run:

```powershell
$env:JIRA_URL = "https://vandysengar.atlassian.net"
$env:JIRA_EMAIL = "vandy.sengar@gmail.com"
$env:JIRA_API_TOKEN = "ATATT3xFfGF0X4VkJdDLuiqEkM9r2qXtbbNwnix6WXAWIq3PEL4PcpIukeEwFSsZeJARyYZTvKpxDZ2I4ZvAOxWhIf6OnLfH5gXx8Vg8AvO1G_OIkRExRnDhFzoF5Al7ZRnNfXGhWnPjiAB0vXQgBLAICbRkn5pkP678knPECZEw8AOTUTGnVkA=7315E455"
npx @modelcontextprotocol/inspector jira-mcp@latest
```

**Browser:** `http://127.0.0.1:6274`

**Tools to capture:**
- search_issues
- get_issue
- create_issue
- transition_issue
- add_comment

**Close:** Press `Ctrl+C` in terminal when done

---

## MCP #5: Slack

Set token first, then run:

```powershell
$env:SLACK_BOT_TOKEN = "xoxb-your-bot-token-here"
npx @modelcontextprotocol/inspector slack-mcp@latest
```

**Note:** You need a Slack bot token. Do you have one?

**Browser:** `http://127.0.0.1:6274`

**Tools to capture:**
- list_channels
- post_message
- send_direct_message
- add_reaction
- upload_file

**Close:** Press `Ctrl+C` in terminal when done

---

## ✅ Summary

| MCP | Status | Port | Browser URL |
|-----|--------|------|-------------|
| Playwright | Ready | 6274 | http://127.0.0.1:6274 |
| Selenium | Ready | 6274 | http://127.0.0.1:6274 |
| GitHub | Ready | 6274 | http://127.0.0.1:6274 |
| Jira | Ready | 6274 | http://127.0.0.1:6274 |
| Slack | Needs Token | 6274 | http://127.0.0.1:6274 |

Run each sequentially and screenshot the tools panel from each MCP!

