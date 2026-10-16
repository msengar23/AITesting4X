# Step-by-Step Instructions: Opening MCP Inspectors & Taking Screenshots

## Overview
This guide walks you through opening each of the 5 MCP inspectors and capturing screenshots of their available tools.

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

---

## Step 7: Organize Screenshots

**7.1** Create a screenshots folder:
```
C:\Users\mamta\AITESTER4XBATCH\LiveClass_Tasks\02August_Tasks\02August_Task03_MCP_Inspectors\screenshots\
```

**7.2** Move all screenshots here:
- `01_Playwright_Tools.png`
- `02_Selenium_Tools.png`
- `03_GitHub_Tools.png`
- `04_Jira_Tools.png`
- `05_Slack_Tools.png`

---

## Step 8: Create Summary Document

**8.1** Create a file: `Screenshots_Summary.md`

**8.2** Add content:
```markdown
# MCP Inspector Screenshots Summary

## Captured MCPs

### 1. Playwright ✅
- **File**: 01_Playwright_Tools.png
- **Tools Count**: 14
- **Key Features**: Browser automation, navigation, clicking, typing
- **Captured**: [Date]

### 2. Selenium ✅
- **File**: 02_Selenium_Tools.png
- **Tools Count**: 19
- **Key Features**: Web element interaction, browser control
- **Captured**: [Date]

### 3. GitHub ✅
- **File**: 03_GitHub_Tools.png
- **Tools Count**: 24
- **Key Features**: Repo management, issue tracking, code search
- **Captured**: [Date]

### 4. Jira ✅
- **File**: 04_Jira_Tools.png
- **Tools Count**: 21
- **Key Features**: Issue management, workflow, sprint tracking
- **Captured**: [Date]

### 5. Slack ✅
- **File**: 05_Slack_Tools.png
- **Tools Count**: 26
- **Key Features**: Channel management, messaging, file uploads
- **Captured**: [Date]

## Total Tools Documented: 104+
```

---

## Step 9: Cleanup & Close Inspectors

**9.1** When done with all screenshots, close each inspector:
- Go to each terminal tab
- Press `Ctrl + C` to stop the inspector
- Close the terminal tab

**9.2** Your final folder structure should be:
```
02August_Task03_MCP_Inspectors/
├── README.md
├── MCP_Tools_Reference.md
├── Step_by_Step_Instructions.md
├── Screenshots_Summary.md
└── screenshots/
    ├── 01_Playwright_Tools.png
    ├── 02_Selenium_Tools.png
    ├── 03_GitHub_Tools.png
    ├── 04_Jira_Tools.png
    └── 05_Slack_Tools.png
```

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

## Tips & Best Practices

✅ **Open multiple terminals** - One per MCP makes it easier to manage  
✅ **Take HIGH QUALITY screenshots** - Use full page captures, not cropped  
✅ **Document the date** - Note when you captured each screenshot  
✅ **Test with a real action** - Try clicking on a tool to see its full schema  
✅ **Use browser DevTools** - Inspect elements to see complete tool definitions  
✅ **Create a checklist** - Mark off each MCP as you complete it  

---

## Verification Checklist

- [ ] Node.js and npm installed and verified
- [ ] Playwright inspector opened and screenshotted
- [ ] Selenium inspector opened and screenshotted
- [ ] GitHub token created and inspector opened
- [ ] Jira credentials configured and inspector opened
- [ ] Slack bot token created and inspector opened
- [ ] All 5 screenshots saved to `screenshots/` folder
- [ ] Summary document created
- [ ] Folder structure organized
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
