# MCP Inspector Tools Reference

## Overview
This document provides a comprehensive reference of tools available from 5 major MCP (Model Context Protocol) servers. Each section lists the tools available from that MCP with their descriptions.

**Note:** To view the actual MCP inspector UI with live tool details, use:
```bash
npx @modelcontextprotocol/inspector <server-command>
```

---

## 1. Playwright MCP

**Purpose:** Automate browser interactions, web testing, and cross-browser automation  
**Server Package:** `@playwright/mcp`

**How to Launch Inspector:**
```bash
npx @modelcontextprotocol/inspector npx playwright-mcp
```

### Available Tools

| Tool Name | Description |
|-----------|-------------|
| `browser_navigate` | Navigate to a URL in the browser |
| `browser_click` | Click on an element using CSS/XPath selector |
| `browser_type` | Type text into a focused input field |
| `browser_fill` | Fill an input field with text |
| `browser_press` | Press a keyboard key |
| `browser_take_screenshot` | Capture a screenshot of the current page |
| `browser_get_page_content` | Get HTML/text content of the current page |
| `browser_find_element` | Find elements on page by selector |
| `browser_wait_for_navigation` | Wait for page navigation to complete |
| `browser_wait_for_selector` | Wait for element to appear |
| `browser_go_back` | Navigate back in browser history |
| `browser_go_forward` | Navigate forward in browser history |
| `browser_reload` | Reload the current page |
| `browser_close` | Close the browser session |

---

## 2. Selenium MCP

**Purpose:** Web browser automation for testing and interaction  
**Server Package:** Community Selenium MCP

**How to Launch Inspector:**
```bash
npx @modelcontextprotocol/inspector npx selenium-mcp
```

### Available Tools

| Tool Name | Description |
|-----------|-------------|
| `start_browser` | Start a new browser session (Chrome/Firefox/Safari) |
| `navigate` | Navigate to a specified URL |
| `find_element` | Locate element using ID, name, CSS selector, or XPath |
| `find_elements` | Find multiple elements matching criteria |
| `click_element` | Click on a located element |
| `send_keys` | Type text into an element |
| `clear_element` | Clear text from an input field |
| `get_attribute` | Get HTML attribute value from element |
| `get_text` | Get visible text of an element |
| `take_screenshot` | Capture a screenshot of the page/element |
| `wait_for_element` | Wait for element to be present/clickable |
| `switch_to_frame` | Switch focus to an iframe |
| `switch_to_default_content` | Return to main page content |
| `execute_script` | Execute JavaScript code |
| `get_current_url` | Get the current page URL |
| `get_page_title` | Get the page title |
| `close_browser` | Close the browser session |
| `accept_alert` | Accept JavaScript alert |
| `dismiss_alert` | Dismiss JavaScript alert |

---

## 3. GitHub MCP

**Purpose:** Access GitHub repositories, issues, pull requests, and code search  
**Server Package:** `@modelcontextprotocol/github`

**How to Launch Inspector:**
```bash
npx @modelcontextprotocol/inspector github-mcp
```

**Authentication:** Requires GitHub token (GITHUB_TOKEN environment variable)

### Available Tools

| Tool Name | Description |
|-----------|-------------|
| `search_repositories` | Search for repositories by keywords/filters |
| `get_repository` | Get detailed info about a specific repository |
| `list_issues` | List issues in a repository |
| `get_issue` | Get detailed information about a specific issue |
| `create_issue` | Create a new issue in a repository |
| `update_issue` | Update issue title, body, or state |
| `add_issue_comment` | Add a comment to an issue |
| `list_pull_requests` | List pull requests in a repository |
| `get_pull_request` | Get details about a specific PR |
| `create_pull_request` | Create a new pull request |
| `update_pull_request` | Update PR title, body, or state |
| `merge_pull_request` | Merge a pull request |
| `list_pull_request_files` | List files changed in a PR |
| `add_pull_request_comment` | Add comment to a PR |
| `search_code` | Search for code across repositories |
| `get_file_contents` | Get contents of a file in a repository |
| `list_files_in_repository` | List files in a directory |
| `create_file` | Create a new file in a repository |
| `update_file` | Update contents of a file |
| `delete_file` | Delete a file from a repository |
| `get_commit` | Get details about a specific commit |
| `list_commits` | List commits in a repository |
| `get_branch_info` | Get information about a branch |
| `list_branches` | List all branches in a repository |

---

## 4. Jira MCP

**Purpose:** Interact with Jira projects, issues, and workflows  
**Server Package:** Community Jira MCP (Atlassian-compatible)

**How to Launch Inspector:**
```bash
npx @modelcontextprotocol/inspector jira-mcp
```

**Authentication:** Requires Jira URL, email, and API token (set as environment variables)

### Available Tools

| Tool Name | Description |
|-----------|-------------|
| `search_issues` | Search issues using JQL (Jira Query Language) |
| `get_issue` | Get detailed information about a specific issue |
| `create_issue` | Create a new issue in a project |
| `update_issue` | Update issue fields (assignee, priority, description, etc.) |
| `add_comment` | Add a comment to an issue |
| `get_comments` | Get all comments on an issue |
| `transition_issue` | Move issue to different workflow state |
| `list_transitions` | List available transitions for an issue |
| `get_issue_types` | Get available issue types in a project |
| `list_projects` | List all projects in Jira instance |
| `get_project` | Get detailed info about a specific project |
| `list_sprints` | List sprints in a project |
| `get_sprint` | Get sprint details |
| `add_issue_to_sprint` | Add issue to a sprint |
| `remove_issue_from_sprint` | Remove issue from sprint |
| `get_issue_changelog` | Get change history of an issue |
| `link_issue` | Create a link between two issues |
| `get_custom_fields` | Get available custom fields |
| `assign_issue` | Assign issue to a user |
| `watch_issue` | Watch/follow an issue |
| `unwatch_issue` | Stop watching an issue |

---

## 5. Slack MCP

**Purpose:** Send messages, manage channels, and interact with Slack workspace  
**Server Package:** `@modelcontextprotocol/slack`

**How to Launch Inspector:**
```bash
npx @modelcontextprotocol/inspector slack-mcp
```

**Authentication:** Requires Slack bot token (SLACK_BOT_TOKEN environment variable)

### Available Tools

| Tool Name | Description |
|-----------|-------------|
| `list_channels` | List all channels in the Slack workspace |
| `get_channel_info` | Get details about a specific channel |
| `create_channel` | Create a new channel |
| `archive_channel` | Archive a channel |
| `post_message` | Send a message to a channel |
| `send_direct_message` | Send a direct message to a user |
| `send_ephemeral_message` | Send a message visible only to one user |
| `update_message` | Edit a previously sent message |
| `delete_message` | Delete a message |
| `add_reaction` | Add an emoji reaction to a message |
| `remove_reaction` | Remove an emoji reaction |
| `get_message_replies` | Get thread replies to a message |
| `reply_in_thread` | Post a reply in a message thread |
| `get_channel_history` | Get message history for a channel |
| `search_messages` | Search messages across channels |
| `list_users` | List users in the workspace |
| `get_user_info` | Get details about a user |
| `set_user_status` | Set user status and emoji |
| `list_user_groups` | List user groups (teams) |
| `get_file_info` | Get information about an uploaded file |
| `download_file` | Download a file from Slack |
| `upload_file` | Upload a file to a channel |
| `invite_users_to_channel` | Add users to a channel |
| `remove_user_from_channel` | Remove user from a channel |
| `create_user_group` | Create a user group |
| `update_user_group` | Update user group members |

---

## How to Screenshot Each MCP Inspector

1. **Open Terminal/Command Prompt** in your project directory

2. **For each MCP**, run the inspector command:
   ```bash
   npx @modelcontextprotocol/inspector <server-command>
   ```

3. **Copy the localhost URL** printed to console (typically `http://localhost:3000`)

4. **Open in browser** and you'll see:
   - Tool name and description
   - Input schema (parameters)
   - Usage examples

5. **Take screenshots** of each MCP's tool list and save them

---

## Alternative: Using Claude Desktop MCP Inspector

If you have Claude Desktop configured with these MCPs:

1. Open Claude Desktop → Settings → Model Options
2. You should see configured MCPs
3. Click **"Inspect"** button next to each MCP to see tools
4. Screenshot the tool list

---

## Summary Table

| MCP | Use Case | Key Tools Count |
|-----|----------|-----------------|
| **Playwright** | Browser automation & testing | 14+ tools |
| **Selenium** | Web testing & interaction | 19+ tools |
| **GitHub** | Repository & code management | 24+ tools |
| **Jira** | Issue tracking & workflow | 21+ tools |
| **Slack** | Team communication & messaging | 26+ tools |

---

**Last Updated:** 2026-10-10  
**Generated for:** MCP Inspector Reference Task
