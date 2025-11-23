# JIRA Bug Analyzer - Copilot Chat Prompt Generator

A Python GUI application that analyzes JIRA bugs and **generates comprehensive prompts for GitHub Copilot Chat** by scanning your actual workspace codebase.
**Works with GitHub Copilot without API limitations!**

## 🎯 Features

- 🔍 **JIRA Integration**: Fetches bug details directly from JIRA REST API v3
- 📁 **Workspace Code Scanning**: Automatically scans your project files (.java, .cpp, .h, .py, .js, .ts)
- 📋 **Copilot Prompt Generator**: Creates ready-to-use prompts for GitHub Copilot Chat
- 🎯 **Workspace-Aware Context**: Includes actual code snippets and file structure in prompts
- 📋 **One-Click Copy**: Copy button to instantly copy prompt to clipboard
- 🎨 **Beautiful GUI**: <Organisation>-branded interface with logo and professional layout
- 🌐 **Browser Integration**: Quick access to view bugs in JIRA web interface
- 🔧 **Customizable**: Works with any technology stack and project type

## Prerequisites

### Required Software:
- Python 3.8 or higher
- pip (Python package manager)

### Required Python Libraries:
```bash
pip install requests pillow
```

Note: `tkinter` usually comes pre-installed with Python. If not, install it:
- **Ubuntu/Debian**: `sudo apt-get install python3-tk`
- **Fedora**: `sudo dnf install python3-tkinter`
- **macOS**: Should be included with Python installation

### Required Credentials:

#### 1. JIRA API Token (Required)
- Go to: https://id.atlassian.com/manage-profile/security/api-tokens
- Click **"Create API token"**
- Give it a name (e.g., "JIRA Analyzer")
- Copy the generated token

#### 2. GitHub Copilot Subscription (Required)
- Verify at: https://github.com/settings/copilot
- You need either:
  - **GitHub Copilot Individual** (~$10/month)
  - **GitHub Copilot Business** (via organization)
- This tool generates prompts that you paste into Copilot Chat in VS Code
- **No API token needed** - works directly with Copilot Chat UI!

## Setup Instructions

### 1. Install Dependencies

```bash
pip install requests
pip install Pillow
```

### 2. Configure for Your Project

Edit the `jira_analyzer_CoPilotChat_Manual.py` file and update the hardcoded configuration section at the top of the `JiraAnalyzerGUI` class:

```python
class JiraAnalyzerGUI:
    # ========== HARDCODED CONFIGURATION ==========
    # Configure your tokens and project details here
    JIRA_BASE_URL = "https://your-company.atlassian.net"  # ← Your JIRA URL
    JIRA_EMAIL = "your.email@company.com"                 # ← Your email
    JIRA_API_TOKEN = "your_jira_api_token_here"          # ← Your JIRA token
    WORKSPACE_PATH = str(Path.cwd())                      # ← Workspace path
    
    # Project-specific configuration (customize for your project)
    PROJECT_NAME = "My Project"                           # ← Your project name
    PROJECT_TECHNOLOGIES = [ "Java", "C++" ]              # ← Your tech stack
    PROJECT_COMPONENTS = [ "Frontend", "Backend", ... ]   # ← Your components
    # =============================================
```

#### Configure JIRA Access:
1. Go to: https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Give it a name (e.g., "JIRA Analyzer")
4. Copy the token and paste it into `JIRA_API_TOKEN`
5. Update `JIRA_BASE_URL` with your company's JIRA URL
6. Update `JIRA_EMAIL` with your JIRA login email

#### Customize Project Information (Optional):
1. **PROJECT_NAME**: Set your project name (e.g., "RNS-SrsInternational")
2. **PROJECT_TECHNOLOGIES**: List main technologies (e.g., ["Java", "C++", "Python"])
3. **PROJECT_COMPONENTS**: List main components (e.g., ["Frontend", "Backend", "Database"])

This information is included in the generated prompts to help Copilot provide more relevant analysis!

---

## ✅ **How This Solves the Copilot API Limitation**

### **The Problem:**
- GitHub Copilot Chat API **does NOT accept** Personal Access Tokens (PATs)
- Even PATs with `copilot` scope cannot access the API endpoint
- Direct API integration is impossible from standalone applications

### **The Solution:**
This tool generates **comprehensive, ready-to-use prompts** that you can paste directly into GitHub Copilot Chat in VS Code:

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Fetch JIRA Bug                                          │
│    └─> JIRA REST API v3                                    │
│    └─> Parse bug details and description                   │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. Scan Workspace (Deep Analysis)                          │
│    └─> Scan up to 100 code files                           │
│    └─> Read up to 1000 lines per file                      │
│    └─> Build workspace structure (30 items)                │
│    └─> Prepare file list (15 files)                        │
│    └─> Extract code samples (8 files, 1500 chars each)     │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. Generate Comprehensive Copilot Prompt                    │
│    └─> Bug details (ID, summary, description)              │
│    └─> Project context (name, technologies, components)    │
│    └─> Workspace structure                                 │
│    └─> Relevant file list (15 files)                       │
│    └─> Code samples (8 files with 1500 chars each)         │
│    └─> Clear instructions for Copilot                      │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. Copy & Paste into Copilot Chat                          │
│    └─> Click "Copy Prompt" button                          │
│    └─> Open VS Code                                        │
│    └─> Open Copilot Chat (Ctrl+Alt+I)                      │
│    └─> Paste and press Enter                               │
│    └─> Get AI-powered analysis!                            │
└─────────────────────────────────────────────────────────────┘
```

### **Benefits:**
✅ **Works with GitHub Copilot** - No API limitations!
✅ **Rich Context** - Includes actual code from your workspace
✅ **One-Click Copy** - Instant clipboard copy functionality
✅ **Comprehensive Prompts** - All information Copilot needs
✅ **No Configuration Hassle** - No tokens or API keys needed
✅ **Better Results** - More context = better AI analysis

---

### 3. Run the Application

```bash
python3 jira_analyzer_CoPilotChat_Manual.py
```

## Usage

### Step-by-Step Workflow

1. **Launch Application**
   ```bash
   python3 jira_analyzer_CoPilotChat_Manual.py
   ```

2. **Enter JIRA Bug ID**
   - Example: `PROJ-123`, `DEV-456`, etc.
   - Format depends on your JIRA project key
   
3. **Optional: View in Browser**
   - Click "View in Browser" to open JIRA in your web browser
   
4. **Generate Copilot Prompt**
   - Click "📋 Generate Copilot Chat Prompt"
   - Wait for workspace scanning and prompt generation (5-15 seconds)
   
5. **Copy the Prompt**
   - Click "📋 Copy Prompt" button
   - Prompt is now in your clipboard
   
6. **Open Copilot Chat in VS Code**
   - Windows/Linux: Press `Ctrl+Alt+I`
   - Mac: Press `Cmd+Shift+I`
   - Or: Click Copilot Chat icon in VS Code sidebar
   
7. **Paste and Analyze**
   - Paste the prompt into Copilot Chat
   - Press Enter
   - Wait for Copilot's AI-powered analysis
   
8. **Review Copilot's Response**
   - Root cause analysis
   - Specific file recommendations
   - Code-level fix suggestions
   - Testing approach
   - Implementation steps

---

## 📊 **Example Generated Prompt**

The tool generates comprehensive, well-formatted prompts like this:

```markdown
# 🐛 JIRA Bug Analysis Request

I need help analyzing and fixing a JIRA bug in my project. Please provide detailed analysis and fix recommendations.

---

## 📋 JIRA Bug Details

**Bug ID:** RNS-123
**Summary:** Performance degradation in message processing

**Description:**
The system experiences significant slowdown when processing messages...

---

## 🏗️ Project Context

**Project Name:** RNS-SrsInternational
**Workspace:** /home/user/project/SrsInternational
**Technologies:** Java, C++
**Components:** Frontend, Backend, Database, API, Cache

---

## 📁 Workspace Analysis

**Total Code Files Scanned:** 42

### Workspace Structure:
```
[DIR] cpp/
[DIR] java/
[DIR] database/
[FILE] build.xml
...
```

### Relevant Code Files in Workspace:
   1. cpp/SrsOCMain.cpp (245 lines)
   2. cpp/SrsMessageQueue.cpp (156 lines)
   3. java/src/ServiceHandler.java (189 lines)
   4. cpp/SrsOCServiceHandler.cpp (198 lines)
   ...

---

## � Code Samples from Workspace

### File 1: cpp/SrsMessageQueue.cpp (156 lines)
\```
// Message queue implementation
class SrsMessageQueue {
    void processMessage(Message& msg) {
        // ... code ...
    }
};
\```

### File 2: java/src/ServiceHandler.java (189 lines)
\```
public class ServiceHandler {
    public void handleRequest(Request req) {
        // ... code ...
    }
}
\```

---

## 🎯 What I Need From You

Please analyze this bug and provide:

1. **Root Cause Analysis**
   - What is likely causing this bug based on the description and code?
   - Which specific files or components are most likely affected?

2. **Detailed Fix Recommendations**
   - What specific code changes are needed?
   - Which files should I modify?
   - Provide code examples showing the fix

3. **Implementation Steps**
   - Step-by-step guide to implement the fix

4. **Testing Strategy**
   - What unit tests should I write?
   - How to test the fix thoroughly?

... (more sections)
```

This prompt is then pasted into Copilot Chat for AI analysis!

---

## Features Explained

### Copilot Prompt Generation

The tool creates comprehensive prompts that include:
- **JIRA Bug Details**: ID, summary, full description
- **Project Context**: Name, technologies, components
- **Workspace Structure**: Directory and file layout
- **Code Files List**: Up to 15 relevant files with line counts
- **Code Samples**: Up to 8 files with 1500 characters each
- **Clear Instructions**: Tells Copilot exactly what analysis you need

### One-Click Workflow

1. **Click "Generate Copilot Chat Prompt"** - Tool scans workspace and creates prompt
2. **Click "Copy Prompt"** - Instant clipboard copy
3. **Paste in Copilot Chat** - Open in VS Code and paste
4. **Get AI Analysis** - Copilot provides detailed, code-specific recommendations

### Customizable for Any Project

The analyzer is fully customizable for any type of application:
- **Web Applications**: React, Angular, Vue, Django, Flask, Spring Boot, .NET, etc.
- **Mobile Apps**: React Native, Flutter, iOS, Android
- **Desktop Applications**: Electron, Qt, JavaFX, WPF
- **Backend Services**: Node.js, Python, Java, C#, Go, Ruby
- **Data Systems**: Databases, Data Pipelines, ETL, Analytics
- **DevOps/Infrastructure**: Docker, Kubernetes, CI/CD, Cloud platforms
- **Embedded Systems**: IoT, Firmware, Real-time systems

### What Copilot Provides

When you paste the generated prompt into Copilot Chat, you get:

1. **Deep Root Cause Analysis**
   - AI analyzes bug in context of your actual code
   - Identifies specific problematic patterns
   - Explains why the bug occurs at code level

2. **Specific File References**
   - Points to exact files from your workspace
   - Often includes line numbers or function names
   - Prioritizes files by importance

3. **Code-Level Fix Recommendations**
   - Actual code snippets showing the fix
   - Multiple solution approaches when applicable
   - Considers your technology stack

4. **Comprehensive Testing Strategy**
   - Unit tests specific to your bug
   - Integration test scenarios
   - Edge cases to consider

5. **Implementation Guidance**
   - Step-by-step fix instructions
   - Deployment considerations
   - Side effect warnings

## Troubleshooting

### "Failed to fetch JIRA bug"
- Verify JIRA credentials are properly set in the script
- Check internet connectivity
- Ensure JIRA bug ID is valid
- Verify you have access to the JIRA project

### "Please configure JIRA credentials"
- Edit the `jira_analyzer_CoPilotChat_Manual.py` file
- Update `JIRA_EMAIL` and `JIRA_API_TOKEN` in the hardcoded configuration section
- Save the file and restart the application

### "No prompt to copy"
- Make sure you've clicked "Generate Copilot Chat Prompt" first
- Wait for the generation to complete
- The prompt will appear in the text area before you can copy it

### Copilot Chat not opening in VS Code
- Verify you have GitHub Copilot subscription active
- Check VS Code has Copilot extension installed
- Try keyboard shortcut: `Ctrl+Alt+I` (Windows/Linux) or `Cmd+Shift+I` (Mac)
- Alternative: Click Copilot icon in VS Code sidebar

### Prompt too long / Copilot not responding
- The tool limits workspace scan to 100 files and 1000 lines each
- If still too long, edit the script to reduce `max_files` or `max_lines_per_file`
- Copilot has context limits (~8K tokens for input)

### No workspace files found in analysis
- Verify you're running from the project root directory
- Check `WORKSPACE_PATH` configuration in the script
- Ensure project has .java, .cpp, .py, .js, or .ts files
- Files in node_modules, .git, build, dist, target are automatically excluded

### GUI doesn't open
- Ensure `tkinter` is installed
- Check Python version (3.8+ required)
- Run: `python3 -m tkinter` to test tkinter installation

### Copy to clipboard not working
- On Linux, you may need `xclip` or `xsel` installed
- Try: `sudo apt-get install xclip` (Ubuntu/Debian)
- On Mac/Windows, clipboard should work out of the box

## Example Workflow

1. Edit `jira_analyzer_CoPilotChat_Manual.py` and configure for your project (first time only)
2. Launch application: `python3 jira_analyzer_CoPilotChat_Manual.py`
3. Enter bug ID: `PROJ-123`
4. Click "📋 Generate Copilot Chat Prompt"
5. Click "📋 Copy Prompt"
6. Open VS Code → Open Copilot Chat (`Ctrl+Alt+I`)
7. Paste prompt and press Enter
8. Review Copilot's AI-powered analysis
9. Apply recommended fixes to your code
10. Test and validate changes

**Time saved**: 2-3 minutes vs manually typing context into Copilot!

## Support

For issues or questions:
1. Verify all prerequisites are installed
2. Check JIRA API token is valid
3. Ensure GitHub Copilot subscription is active
4. Verify Copilot extension is installed in VS Code
5. Ensure JIRA URL is correct
6. Review project configuration matches your tech stack
7. Check Python and library versions

## Use Cases

This tool is perfect for:
- **Developers**: Get AI-powered bug analysis with your actual code context
- **Team Leads**: Understand bug impact with detailed AI insights
- **QA Engineers**: Better understand bugs through AI analysis
- **New Team Members**: Learn codebase through AI-explained bugs
- **Code Reviews**: Get AI insights during bug fix reviews
- **Complex Bugs**: Leverage Copilot AI for hard-to-diagnose issues

## Advantages Over Manual Copilot Usage

| **Aspect** | **Manual Copilot Chat** | **With This Tool** |
|------------|------------------------|-------------------|
| Context gathering | Manual file copying | Automatic (100 files scanned) |
| Bug details | Manual typing | Automatic from JIRA API |
| Code samples | Copy-paste 1-2 files | 8 files (1500 chars each) |
| Workspace structure | Not included | Full directory tree |
| Time required | 10-15 minutes | 30 seconds |
| File discovery | Manual search | Automatic scanning |
| Consistent quality | Varies | Always comprehensive |

## License

Open source - use and modify as needed for your projects!

## Security Notes

- All API tokens are hardcoded in the script
- Keep `jira_analyzer_CoPilotChat_Manual.py` secure and private
- Don't commit the script with real tokens to public repositories
- Consider creating a template version with placeholder tokens for sharing
- Use read-only JIRA tokens when possible
- Regularly rotate API tokens
- **Your code is included in prompts** - ensure compliance with your organization's policies regarding code sharing with AI services

## Quick Start Guide

```bash
# 1. Install dependencies
pip install requests Pillow

# 2. Verify GitHub Copilot subscription
# Go to: https://github.com/settings/copilot
# Ensure Copilot is active

# 3. Edit the script and configure your JIRA credentials
nano jira_analyzer_CoPilotChat_Manual.py  # or use your preferred editor

# 4. Update these settings in the script:
#    JIRA_BASE_URL = "https://your-company.atlassian.net"
#    JIRA_EMAIL = "your.email@company.com"
#    JIRA_API_TOKEN = "your_actual_token"
#    
#    # Optional: Customize project info
#    PROJECT_NAME = "Your Project Name"
#    PROJECT_TECHNOLOGIES = ["Java", "C++", ...]
#    PROJECT_COMPONENTS = ["Frontend", "Backend", ...]

# 5. Run the application
python3 jira_analyzer_CoPilotChat_Manual.py

# 6. Generate prompt for your bug
#    - Enter JIRA bug ID
#    - Click "Generate Copilot Chat Prompt"
#    - Click "Copy Prompt"

# 7. Use in Copilot Chat
#    - Open VS Code
#    - Press Ctrl+Alt+I (or Cmd+Shift+I on Mac)
#    - Paste and press Enter
```

## Example Configurations

### Web Application (React + Node.js + PostgreSQL)
```python
PROJECT_NAME = "E-Commerce Platform"
PROJECT_TECHNOLOGIES = [
    "React", "Node.js", "Express", "PostgreSQL", "Redis",
    "Docker", "Kubernetes", "AWS", "TypeScript"
]
PROJECT_COMPONENTS = [
    "Frontend UI", "Backend API", "Database", "Authentication",
    "Payment Gateway", "Order Processing", "Inventory Management",
    "Notification Service", "Admin Dashboard"
]
```

### Mobile Application (React Native)
```python
PROJECT_NAME = "Social Media App"
PROJECT_TECHNOLOGIES = [
    "React Native", "Node.js", "MongoDB", "Firebase",
    "Redux", "GraphQL", "AWS S3", "Push Notifications"
]
PROJECT_COMPONENTS = [
    "Mobile App", "Backend API", "Database", "Authentication",
    "Media Storage", "Real-time Chat", "User Profiles",
## Support

For issues or questions:
1. Verify all prerequisites are installed
2. Check JIRA API token is valid
3. Ensure JIRA URL is correct
4. Review project configuration matches your tech stack
5. Check Python and library versions

## Use Cases

This tool is perfect for:
- **Developers**: Quick bug analysis and fix suggestions
- **Team Leads**: Understand bug impact and estimate effort
- **QA Engineers**: Better understand bug context for testing
- **New Team Members**: Learn about codebase through bug analysis
- **Code Reviews**: Get additional insights during bug fix reviews

## License

Open source - use and modify as needed for your projects!
