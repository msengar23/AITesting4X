# MCP Inspector Tools - Complete Guide

**Task:** Open at least 5 MCP inspectors and document their tools as screenshots

**MCPs to Cover:**
1. ✅ Playwright
2. ✅ Selenium
3. ✅ GitHub
4. ✅ Jira
5. ✅ Slack

---

## Prerequisites

### System Requirements
- **Operating System**: Windows, macOS, or Linux
- **Node.js**: Version 16.0 or higher
- **npm**: Version 7.0 or higher
- **Browser**: Chrome, Firefox, Safari, or Edge
- **Terminal/Command Prompt**: PowerShell (Windows) or Terminal (Mac/Linux)

### Installation Check

**Step 1.1:** Open Command Prompt/Terminal and verify Node.js installation:
```bash
node --version
# Expected output: v16.0.0 or higher
```

**Step 1.2:** Verify npm installation:
```bash
npm --version
# Expected output: 7.0.0 or higher
```

**If not installed:**
- Download from: https://nodejs.org/
- Install the LTS (Long Term Support) version
- Restart your terminal after installation

---

## MCP Inspector #1: Playwright

### Step 2: Open Playwright MCP Inspector

**2.1** Open Terminal/Command Prompt

**2.2** Navigate to any working directory (e.g., your Documents folder):
```bash
cd Documents
# or
cd ~/Downloads
```

**2.3** Run the Playwright MCP inspector:
```bash
npx @modelcontextprotocol/inspector npx @playwright/mcp@latest
```

**2.4** Wait for output (takes 10-15 seconds on first run):
```
Starting MCP inspector...
Available on: http://localhost:3000
Open this URL in your browser
```

**2.5** Open your web browser (Chrome, Firefox, etc.)

**2.6** In the address bar, go to:
```
http://localhost:3000
```

**2.7** You'll see the Playwright MCP Inspector interface showing:
- List of available tools on the left sidebar
- Tool details on the right (description, input schema, examples)

### Step 2.8: Screenshot the Playwright Tools

**Option A: Full Page Screenshot**
- Press `Ctrl + Shift + S` (Windows/Linux) or `Cmd + Shift + 4` (Mac)
- Select the entire tools list area
- Save as: `01_Playwright_Tools.png`

**Option B: Built-in Browser Screenshot**
- Right-click on the page → "Take screenshot"
- Or press `Ctrl + Shift + I` → Console → 
  ```javascript
  document.documentElement.scrollHeight = document.documentElement.scrollHeight
  ```

**Step 2.9** Screenshot captures should show:
- ✅ Tool names (browser_navigate, browser_click, etc.)
- ✅ Description of each tool
- ✅ Input parameters/schema

**Step 2.10** Leave the terminal running, open a NEW terminal tab for the next MCP

### Playwright MCP Tools Reference

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

## MCP Inspector #2: Selenium

### Step 3: Open Selenium MCP Inspector

**3.1** Open a NEW terminal tab (don't close Playwright tab)

**3.2** Run the Selenium MCP inspector:
```bash
npx @modelcontextprotocol/inspector npx selenium-mcp@latest
```

**3.3** Wait for the output showing the URL:
```
Available on: http://localhost:3001
```

**Note:** Selenium uses port 3001 (different from Playwright's 3000)

**3.4** Open a NEW browser tab and navigate to:
```
http://localhost:3001
```

**3.5** The Selenium MCP Inspector will load, showing:
- Selenium-specific tools (start_browser, navigate, click_element, etc.)
- Full tool documentation

### Step 3.6: Screenshot the Selenium Tools

**3.6a** Take a full-page screenshot:
- Press `Ctrl + Shift + S` (Windows/Linux) or `Cmd + Shift + 4` (Mac)
- Select the tools panel
- Save as: `02_Selenium_Tools.png`

**3.6b** Scroll down if needed to capture all tools:
- Screenshot should include:
  - ✅ Tool names (start_browser, navigate, find_element, etc.)
  - ✅ Descriptions for each tool
  - ✅ Parameter requirements

**3.7** Keep this terminal running, open another NEW terminal for the next MCP

### Selenium MCP Tools Reference

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

## MCP Inspector #3: GitHub

### Step 4: Open GitHub MCP Inspector

**Important:** GitHub MCP requires authentication

**4.1** Get your GitHub Personal Access Token:
- Go to: https://github.com/settings/tokens
- Click "Generate new token"
- Select scopes: `repo`, `read:user`, `read:org`
- Copy the token (save it temporarily)

**4.2** Open a NEW terminal tab

**4.3** Set the GitHub token (Windows - PowerShell):
```powershell
$env:GITHUB_TOKEN = "your_github_token_here"
```

**Or (Windows - Command Prompt):**
```cmd
set GITHUB_TOKEN=your_github_token_here
```

**Or (Mac/Linux):**
```bash
export GITHUB_TOKEN=your_github_token_here
```

**Replace `your_github_token_here`** with your actual token

**4.4** Run the GitHub MCP inspector:
```bash
npx @modelcontextprotocol/inspector github-mcp@latest
```

**4.5** Wait for the URL (should be on a different port, e.g., 3002):
```
Available on: http://localhost:3002
```

**4.6** Open a NEW browser tab and go to:
```
http://localhost:3002
```

**4.7** GitHub MCP Inspector loads showing:
- Repository management tools
- Issue/PR tools
- Code search tools
- File management tools

### Step 4.8: Screenshot the GitHub Tools

**4.8a** Take full-page screenshots:
- Use `Ctrl + Shift + S` or browser screenshot tool
- Capture the complete tools list
- Save as: `03_GitHub_Tools.png`

**4.8b** Key tools to verify in screenshot:
- ✅ search_repositories
- ✅ create_issue
- ✅ create_pull_request
- ✅ search_code
- ✅ get_file_contents

**4.9** Keep terminal running, open another NEW terminal

### GitHub MCP Tools Reference

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

## MCP Inspector #4: Jira

### Step 5: Open Jira MCP Inspector

**Important:** Jira MCP requires authentication

**5.1** Gather your Jira credentials:
- **Jira URL**: `https://your-instance.atlassian.net`
- **Email**: Your Jira account email
- **API Token**: Create at https://id.atlassian.com/manage-profile/security/api-tokens

**5.2** Open a NEW terminal tab

**5.3** Set Jira environment variables (Windows - PowerShell):
```powershell
$env:JIRA_URL = "https://your-instance.atlassian.net"
$env:JIRA_EMAIL = "your-email@example.com"
$env:JIRA_API_TOKEN = "your_api_token_here"
```

**Or (Windows - Command Prompt):**
```cmd
set JIRA_URL=https://your-instance.atlassian.net
set JIRA_EMAIL=your-email@example.com
set JIRA_API_TOKEN=your_api_token_here
```

**Or (Mac/Linux):**
```bash
export JIRA_URL="https://your-instance.atlassian.net"
export JIRA_EMAIL="your-email@example.com"
export JIRA_API_TOKEN="your_api_token_here"
```

**5.4** Run the Jira MCP inspector:
```bash
npx @modelcontextprotocol/inspector jira-mcp@latest
```

**5.5** Wait for the localhost URL:
```
Available on: http://localhost:3003
```

**5.6** Open a NEW browser tab:
```
http://localhost:3003
```

**5.7** Jira MCP Inspector shows:
- Issue search tools
- Issue creation/update tools
- Workflow transition tools
- Project management tools

### Step 5.8: Screenshot the Jira Tools

**5.8a** Take full-page screenshot:
- Use `Ctrl + Shift + S` or browser tools
- Save as: `04_Jira_Tools.png`

**5.8b** Important tools to capture:
- ✅ search_issues
- ✅ get_issue
- ✅ create_issue
- ✅ transition_issue
- ✅ add_comment

**5.9** Keep terminal running, open another NEW terminal

### Jira MCP Tools Reference

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

## MCP Inspector #5: Slack

### Step 6: Open Slack MCP Inspector

**Important:** Slack MCP requires a bot token

**6.1** Create a Slack App and get bot token:
- Go to: https://api.slack.com/apps
- Click "Create New App" → "From scratch"
- App name: `MCP Inspector`
- Workspace: Select your workspace
- Go to "OAuth & Permissions" → "Bot Token Scopes"
- Add scopes: `channels:read`, `users:read`, `chat:write`, `files:read`
- Install the app to your workspace
- Copy the **Bot User OAuth Token** (starts with `xoxb-`)

**6.2** Open a NEW terminal tab

**6.3** Set the Slack token (Windows - PowerShell):
```powershell
$env:SLACK_BOT_TOKEN = "xoxb-your-bot-token-here"
```

**Or (Windows - Command Prompt):**
```cmd
set SLACK_BOT_TOKEN=xoxb-your-bot-token-here
```

**Or (Mac/Linux):**
```bash
export SLACK_BOT_TOKEN="xoxb-your-bot-token-here"
```

**Replace with your actual bot token**

**6.4** Run the Slack MCP inspector:
```bash
npx @modelcontextprotocol/inspector slack-mcp@latest
```

**6.5** Wait for the URL:
```
Available on: http://localhost:3004
```

**6.6** Open a NEW browser tab:
```
http://localhost:3004
```

**6.7** Slack MCP Inspector displays:
- Channel management tools
- Message posting tools
- User management tools
- File management tools
- Reaction management tools

### Step 6.8: Screenshot the Slack Tools

**6.8a** Take full-page screenshot:
- Use `Ctrl + Shift + S` or screenshot tool
- Save as: `05_Slack_Tools.png`

**6.8b** Verify screenshot includes:
- ✅ list_channels
- ✅ post_message
- ✅ send_direct_message
- ✅ add_reaction
- ✅ upload_file

**6.9** Keep this inspector running

### Slack MCP Tools Reference

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

## Step 7: Organize Screenshots

**7.1** Create a screenshots folder:
```
C:\Users\mamta\AITESTER4XBATCH\LiveClass_Tasks\04Oct_Task2\screenshots\
```

**7.2** Move all screenshots here:
- `01_Playwright_Tools.png`
- `02_Selenium_Tools.png`
- `03_GitHub_Tools.png`
- `04_Jira_Tools.png`
- `05_Slack_Tools.png`

---

## Summary of All MCP Tools

| MCP | Tool Count | Key Use Case |
|-----|-----------|--------------|
| **Playwright** | 14 | Browser automation & testing |
| **Selenium** | 19 | Web element interaction |
| **GitHub** | 24 | Repository & code management |
| **Jira** | 21 | Issue tracking & workflow |
| **Slack** | 26 | Team communication |
| **TOTAL** | **104+** | Complete automation suite |

---

## Troubleshooting

### Issue: "Command not found: npx"
**Solution:**
- Node.js not installed or PATH not updated
- Restart terminal or computer
- Run: `npm install -g npm` to update npm

### Issue: "Port 3000 already in use"
**Solution:**
- Kill the process on that port (Windows):
  ```cmd
  netstat -ano | findstr :3000
  taskkill /PID [PID] /F
  ```
- Or use a different port: `npx @modelcontextprotocol/inspector --port 3005 ...`

### Issue: "ENOENT: no such file or directory"
**Solution:**
- Wait for npm to download packages (first run takes longer)
- Try again with: `npx @modelcontextprotocol/inspector npx @playwright/mcp@latest --force`

### Issue: Authentication fails for GitHub/Jira/Slack
**Solution:**
- Verify token is correct and not expired
- Check environment variable is set: `echo $GITHUB_TOKEN` (Mac/Linux)
- Or: `echo $env:GITHUB_TOKEN` (Windows PowerShell)
- Make sure there are no extra spaces in the token

### Issue: Inspector page shows "No tools available"
**Solution:**
- Refresh the browser page (F5)
- Check terminal for error messages
- Verify authentication succeeded
- Try installing the latest version: `@playwright/mcp@latest`

---

## Verification Checklist

- [ ] Node.js and npm installed and verified
- [ ] Playwright inspector opened and screenshotted
- [ ] Selenium inspector opened and screenshotted
- [ ] GitHub token created and inspector opened
- [ ] Jira credentials configured and inspector opened
- [ ] Slack bot token created and inspector opened
- [ ] All 5 screenshots saved to `screenshots/` folder
- [ ] Screenshots show tool names and descriptions
- [ ] All terminals closed cleanly

---

## Final Notes

**Estimated Time**: 30-45 minutes total  
**Difficulty Level**: Beginner (just following commands)  
**Key Requirement**: Internet connection for npm downloads  

Once complete, you'll have:
- ✅ 5 MCP inspectors successfully opened
- ✅ Screenshots of all available tools from each MCP
- ✅ Complete documentation for reference
- ✅ Understanding of what tools each MCP provides

**Task Status**: Ready to execute! 🚀

---

**Last Updated:** 2026-10-10  
**Created for:** 04Oct_Task2
