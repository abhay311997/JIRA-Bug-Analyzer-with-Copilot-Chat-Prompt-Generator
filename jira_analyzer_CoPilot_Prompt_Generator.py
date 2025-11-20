#!/usr/bin/env python3
"""
JIRA Bug Analyzer with GitHub Copilot Integration
This script provides a GUI to analyze JIRA bugs and get AI-powered bug fix suggestions.

All configurations are hardcoded - no external config files needed!
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests
from requests.auth import HTTPBasicAuth
from pathlib import Path
import webbrowser
from io import BytesIO
from PIL import Image, ImageTk
import os
import json

class JiraAnalyzerGUI:
    # ========== HARDCODED CONFIGURATION ==========
    # Configure your tokens and project details here
    JIRA_BASE_URL = "https://abc.atlassian.net/"  # Replace with your JIRA Base URL
    JIRA_EMAIL = "name@org.comf"  # Replace with your JIRA email
    JIRA_API_TOKEN = ""  # Replace with your JIRA API token
    WORKSPACE_PATH = str(Path.cwd())  # Current directory
    
    # Project-specific configuration (customize for your project)
    PROJECT_NAME = "Project-name"  # Your project name
    PROJECT_TECHNOLOGIES = [ "Java", "C++" ]  
    # List technologies used in your project like ["Python", "Java", "C++", "JavaScript", "React", "Node.js", "Django", "Spring Boot", "Docker", "Kubernetes"]
    PROJECT_COMPONENTS = [ "Frontend", "Backend", "Database", "API", "Cache" ]  
    # List main components of your project like ["Frontend", "Backend", "Database", "API", "Authentication", "Cache", "Message Queue", "File Processing"]
    
    # =============================================
    
    def __init__(self, root):
        self.root = root
        self.root.title("JIRA Bug Analyzer - Copilot Chat Prompt Generator")
        self.root.geometry("1000x800")
        
        # Use hardcoded configuration
        self.config = {
            "jira_base_url": self.JIRA_BASE_URL,
            "jira_email": self.JIRA_EMAIL,
            "jira_api_token": self.JIRA_API_TOKEN,
            "workspace_path": self.WORKSPACE_PATH
        }
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the GUI components"""
        # Main Analysis Frame (no tabs needed)
        analysis_frame = ttk.Frame(self.root)
        analysis_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Add logo at the top
        self.add_logo(analysis_frame)
        
        self.setup_analysis_tab(analysis_frame)
    
    def add_logo(self, parent):
        """Add company logo at the top of the GUI"""
        try:
            # Download logo symbol from URL
            logo_url = "https://blog.org.com/hubfs/logo.png"
            response = requests.get(logo_url, timeout=10)
            response.raise_for_status()
            
            # Load image
            image_data = BytesIO(response.content)
            symbol_img = Image.open(image_data)
            
            # Resize logo symbol (smaller size)
            symbol_width = 350
            ratio = symbol_width / symbol_img.width
            symbol_height = int(symbol_img.height * ratio)
            symbol_img = symbol_img.resize((symbol_width, symbol_height), Image.Resampling.LANCZOS)
            
            # Crop to show only M symbol from logo
            crop_width = symbol_width // 7
            symbol_img = symbol_img.crop((0, 0, crop_width, symbol_height))
            
            # Convert to PhotoImage
            self.logo_image = ImageTk.PhotoImage(symbol_img)
            
            # Create logo frame with white background - centered with minimal height
            logo_frame = tk.Frame(parent, bg='white')
            logo_frame.pack(pady=(0, 5), fill='x')
            
            # Container for horizontal layout - centered
            logo_container = tk.Frame(logo_frame, bg='white')
            logo_container.pack(anchor='center', pady=(2, 2))
            
            # Left side: M symbol with minimal padding
            logo_label = tk.Label(logo_container, image=self.logo_image, bg='white')
            logo_label.pack(side='left', padx=(0, 2), pady=(5, 0))
            
            # Right side: Text frame (Company_name + tagline)
            text_frame = tk.Frame(logo_container, bg='white')
            text_frame.pack(side='left')
            
            # "XYZ Organisation" text in larger font
            company_name = tk.Label(text_frame, text="XYZ Organisation", 
                                   font=('Arial', 40, 'normal'), 
                                   fg='black', bg='white')
            company_name.pack(anchor='w', pady=(0, 0))
            
            # Tagline in smaller font below - shifted right and closer to top
            tagline = tk.Label(text_frame, text="Organisation Tag Line", 
                             font=('Arial', 10), 
                             fg='black', bg='white')
            tagline.pack(anchor='w', padx=(20, 0), pady=(0, 5))
            
        except Exception as e:
            # If logo fails to load, just continue without it
            print(f"Could not load logo: {e}")
    
    def setup_analysis_tab(self, parent):
        """Setup the main analysis tab"""
        # JIRA Bug ID Input Section
        input_frame = ttk.LabelFrame(parent, text="JIRA Bug Details", padding=10)
        input_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(input_frame, text="JIRA Bug ID:").grid(row=0, column=0, sticky='w', pady=5)
        self.bug_id_entry = ttk.Entry(input_frame, width=30, font=('Arial', 11))
        self.bug_id_entry.grid(row=0, column=1, sticky='ew', padx=10, pady=5)
        self.bug_id_entry.insert(0, "")  # Placeholder example
        
        # View in Browser Button
        view_button = ttk.Button(input_frame, text="View in Browser", 
                                 command=self.view_in_browser)
        view_button.grid(row=0, column=2, padx=5)
        
        input_frame.columnconfigure(1, weight=1)
        
        # Analyze Button
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill='x', padx=10, pady=5)
        
        self.analyze_button = ttk.Button(button_frame, text="📋 Generate Copilot Chat Prompt", 
                                         command=self.analyze_bug,
                                         style='Accent.TButton')
        self.analyze_button.pack(pady=10)
        
        # Progress Bar
        self.progress = ttk.Progressbar(button_frame, mode='indeterminate')
        self.progress.pack(fill='x', pady=5)
        
        # Results Section
        results_frame = ttk.LabelFrame(parent, text="Analysis Results", padding=10)
        results_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Bug Details Section
        ttk.Label(results_frame, text="Bug Details:", font=('Arial', 10, 'bold')).pack(anchor='w')
        self.bug_details_text = scrolledtext.ScrolledText(results_frame, height=8, 
                                                          wrap=tk.WORD, font=('Courier', 9))
        self.bug_details_text.pack(fill='both', expand=True, pady=5)
        
        # Copilot Chat Prompt Section with Copy Button
        prompt_header_frame = ttk.Frame(results_frame)
        prompt_header_frame.pack(fill='x', pady=(10, 0))
        
        ttk.Label(prompt_header_frame, text="🤖 Copilot Chat Prompt (Copy & Paste):", 
                 font=('Arial', 10, 'bold')).pack(side='left')
        
        self.copy_button = ttk.Button(prompt_header_frame, text="📋 Copy Prompt", 
                                      command=self.copy_prompt_to_clipboard)
        self.copy_button.pack(side='right', padx=5)
        
        # Instructions label
        instructions = ttk.Label(results_frame, 
                                text="📌 Copy this prompt and paste it into GitHub Copilot Chat in VS Code",
                                font=('Arial', 9, 'italic'),
                                foreground='blue')
        instructions.pack(anchor='w', pady=(2, 5))
        
        self.bug_fix_text = scrolledtext.ScrolledText(results_frame, height=20, 
                                                      wrap=tk.WORD, font=('Courier', 9))
        self.bug_fix_text.pack(fill='both', expand=True, pady=5)
        
        # Status Bar
        self.status_label = ttk.Label(parent, text="Ready", relief=tk.SUNKEN, anchor='w')
        self.status_label.pack(fill='x', side='bottom', padx=10, pady=5)
    
    def copy_prompt_to_clipboard(self):
        """Copy the Copilot prompt to clipboard"""
        try:
            prompt_text = self.bug_fix_text.get(1.0, tk.END).strip()
            if prompt_text:
                self.root.clipboard_clear()
                self.root.clipboard_append(prompt_text)
                self.root.update()
                messagebox.showinfo("Success", "Prompt copied to clipboard!\n\nNow:\n1. Open VS Code\n2. Open Copilot Chat (Ctrl+Alt+I or Cmd+Shift+I)\n3. Paste the prompt\n4. Press Enter")
            else:
                messagebox.showwarning("Warning", "No prompt to copy. Please analyze a bug first.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy to clipboard: {str(e)}")
    
    def view_in_browser(self):
        """Open JIRA bug in browser"""
        bug_id = self.bug_id_entry.get().strip()
        if bug_id:
            url = f"{self.config['jira_base_url']}/browse/{bug_id}"
            webbrowser.open(url)
        else:
            messagebox.showwarning("Warning", "Please enter a JIRA Bug ID")
    
    def fetch_jira_bug(self, bug_id):
        """Fetch bug details from JIRA"""
        try:
            url = f"{self.config['jira_base_url']}/rest/api/3/issue/{bug_id}"
            
            auth = HTTPBasicAuth(self.config['jira_email'], self.config['jira_api_token'])
            headers = {"Accept": "application/json"}
            
            response = requests.get(url, headers=headers, auth=auth, timeout=30)
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch JIRA bug: {str(e)}")
    
    def format_bug_details(self, bug_data):
        """Format bug details for display"""
        try:
            fields = bug_data.get('fields', {})
            
            # Handle description - it can be a string or a dict (ADF format)
            description_raw = fields.get('description', 'No description available')
            if isinstance(description_raw, dict):
                description = self.extract_text_from_adf(description_raw)
            else:
                description = str(description_raw) if description_raw else 'No description available'
            
            # Handle environment field
            environment_raw = fields.get('environment')
            if isinstance(environment_raw, dict):
                environment = self.extract_text_from_adf(environment_raw)
            else:
                environment = str(environment_raw) if environment_raw else 'Not specified'
            
            details = f"""
Bug ID: {bug_data.get('key', 'N/A')}
Summary: {fields.get('summary', 'N/A')}
Status: {fields.get('status', {}).get('name', 'N/A')}
Priority: {fields.get('priority', {}).get('name', 'N/A')}
Reporter: {fields.get('reporter', {}).get('displayName', 'N/A')}
Assignee: {fields.get('assignee', {}).get('displayName', 'Unassigned')}
Created: {fields.get('created', 'N/A')[:10]}
Updated: {fields.get('updated', 'N/A')[:10]}

Description:
{description}

Environment:
{environment}

Components:
{', '.join([c.get('name', '') for c in fields.get('components', [])]) or 'None'}

Labels:
{', '.join(fields.get('labels', [])) or 'None'}
            """.strip()
            
            return details
        except Exception as e:
            return f"Error formatting bug details: {str(e)}"
    
    def generate_copilot_analysis(self, bug_data):
        """Generate Copilot Chat prompt that users can copy and paste"""
        try:
            fields = bug_data.get('fields', {})
            bug_id = bug_data.get('key', 'Unknown')
            summary = fields.get('summary', '')
            
            # Handle description - it can be a string or a dict (ADF format)
            description_raw = fields.get('description', '')
            if isinstance(description_raw, dict):
                description = self.extract_text_from_adf(description_raw)
            else:
                description = str(description_raw) if description_raw else ''
            
            # Scan workspace for relevant code files
            self.status_label.config(text="Scanning workspace for code context...")
            self.root.update()
            workspace_context = self.scan_workspace_files()
            
            # Generate comprehensive prompt for Copilot Chat
            self.status_label.config(text="Generating Copilot Chat prompt...")
            self.root.update()
            prompt = self.generate_copilot_chat_prompt(
                bug_id, summary, description, workspace_context
            )
            
            return prompt
            
        except Exception as e:
            return f"Error generating Copilot prompt: {str(e)}"
    
    def scan_workspace_files(self):
        """Scan workspace and collect relevant code files"""
        workspace_path = Path(self.config['workspace_path'])
        code_extensions = {'.java', '.cpp', '.h', '.py', '.js', '.ts', '.jsx', '.tsx', '.c', '.cc'}
        
        relevant_files = []
        file_count = 0
        max_files = 100  # Limit to avoid token overflow
        max_lines_per_file = 2000  # Limit lines per file
        
        try:
            for ext in code_extensions:
                if file_count >= max_files:
                    break
                    
                for file_path in workspace_path.rglob(f'*{ext}'):
                    if file_count >= max_files:
                        break
                    
                    # Skip common directories to ignore
                    if any(skip in file_path.parts for skip in ['node_modules', '.git', 'build', 'dist', 'target', '__pycache__']):
                        continue
                    
                    try:
                        # Read file content
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = f.readlines()[:max_lines_per_file]
                            content = ''.join(lines)
                            
                        relative_path = file_path.relative_to(workspace_path)
                        relevant_files.append({
                            'path': str(relative_path),
                            'content': content,
                            'lines': len(lines)
                        })
                        file_count += 1
                    except Exception as e:
                        continue
            
            return {
                'total_files': file_count,
                'files': relevant_files,
                'workspace_structure': self.get_workspace_structure()
            }
        except Exception as e:
            return {
                'total_files': 0,
                'files': [],
                'error': str(e)
            }
    
    def get_workspace_structure(self):
        """Get high-level workspace structure"""
        workspace_path = Path(self.config['workspace_path'])
        structure = []
        
        try:
            for item in workspace_path.iterdir():
                if item.name.startswith('.'):
                    continue
                if item.is_dir():
                    structure.append(f"[DIR] {item.name}/")
                else:
                    structure.append(f"[FILE] {item.name}")
        except Exception:
            pass
        
        return structure[:30]  # Limit to first 30 items
    
    def generate_copilot_chat_prompt(self, bug_id, summary, description, workspace_context):
        """Generate a comprehensive prompt for GitHub Copilot Chat"""
        
        # Get workspace files summary
        workspace_files = workspace_context.get('files', [])
        total_files = workspace_context.get('total_files', 0)
        
        # Build workspace structure
        workspace_structure = "\n".join(workspace_context.get('workspace_structure', []))
        
        # Get relevant files list
        relevant_files_list = "\n".join([
            f"   {idx}. {f['path']} ({f['lines']} lines)" 
            for idx, f in enumerate(workspace_files[:15], 1)
        ])
        
        # Get code samples from top files
        code_samples = ""
        for idx, file_info in enumerate(workspace_files[:8], 1):
            code_samples += f"\n### File {idx}: {file_info['path']} ({file_info['lines']} lines)\n"
            code_samples += "```\n"
            code_samples += file_info['content'][:1500]  # First 1500 chars
            code_samples += "\n```\n"
        
        # Generate comprehensive prompt
        prompt = f"""# 🐛 JIRA Bug Analysis Request

I need help analyzing and fixing a JIRA bug in my project. Please provide detailed analysis and fix recommendations.

---

## 📋 JIRA Bug Details

**Bug ID:** {bug_id}
**Summary:** {summary}

**Description:**
{description}

---

## 🏗️ Project Context

**Project Name:** {self.PROJECT_NAME}
**Workspace:** {self.config['workspace_path']}
**Technologies:** {', '.join(self.PROJECT_TECHNOLOGIES)}
**Components:** {', '.join(self.PROJECT_COMPONENTS)}

---

## 📁 Workspace Analysis

**Total Code Files Scanned:** {total_files}

### Workspace Structure:
```
{workspace_structure}
```

### Relevant Code Files in Workspace:
{relevant_files_list if relevant_files_list else "   No code files found"}

---

## 💻 Code Samples from Workspace

{code_samples if code_samples else "No code samples available"}

---

## 🎯 What I Need From You

Please analyze this bug and provide:

1. **Root Cause Analysis**
   - What is likely causing this bug based on the description and code?
   - Which specific files or components are most likely affected?
   - Are there any patterns in the code that might contribute to this issue?

2. **Detailed Fix Recommendations**
   - What specific code changes are needed?
   - Which files should I modify? (from the workspace files listed above)
   - Provide code examples showing the fix
   - Consider the project's technology stack: {', '.join(self.PROJECT_TECHNOLOGIES)}

3. **Implementation Steps**
   - Step-by-step guide to implement the fix
   - What to change in each affected file
   - Any configuration or dependency updates needed

4. **Testing Strategy**
   - What unit tests should I write?
   - How to test the fix thoroughly?
   - Edge cases to consider

5. **Potential Side Effects**
   - What other parts of the codebase might be affected?
   - Any performance implications?
   - Backward compatibility concerns?

6. **Code Review Checklist**
   - What should reviewers pay attention to?
   - Security considerations
   - Best practices to follow

---

## 📝 Additional Context

- This is a **{self.PROJECT_NAME}** project
- Main technologies: {', '.join(self.PROJECT_TECHNOLOGIES)}
- Focus on providing actionable, code-specific suggestions
- Reference the actual files from my workspace (listed above)
- Consider the project structure and components

---

**Please provide a comprehensive analysis with specific file references and code examples!** 🚀
"""
        
        return prompt
    
    def extract_text_from_adf(self, adf_content):
        """Extract plain text from Atlassian Document Format (ADF)"""
        try:
            text_parts = []
            
            def extract_text(node, depth=0):
                if isinstance(node, dict):
                    node_type = node.get('type', '')
                    
                    # Handle paragraph breaks
                    if node_type == 'paragraph' and depth > 0:
                        text_parts.append('\n')
                    
                    # Handle text nodes
                    if node_type == 'text':
                        text_parts.append(node.get('text', ''))
                    
                    # Handle hard breaks
                    if node_type == 'hardBreak':
                        text_parts.append('\n')
                    
                    # Handle list items
                    if node_type in ['bulletList', 'orderedList']:
                        text_parts.append('\n')
                    
                    if node_type == 'listItem':
                        text_parts.append('\n• ')
                    
                    # Recursively process content
                    if 'content' in node:
                        for child in node['content']:
                            extract_text(child, depth + 1)
                    
                    # Add paragraph break after paragraph
                    if node_type == 'paragraph':
                        text_parts.append('\n')
                        
                elif isinstance(node, list):
                    for item in node:
                        extract_text(item, depth)
            
            extract_text(adf_content)
            result = ''.join(text_parts).strip()
            # Clean up multiple consecutive newlines
            import re
            result = re.sub(r'\n{3,}', '\n\n', result)
            return result
        except Exception as e:
            return f"[Could not parse description: {str(e)}]"
    
    def analyze_bug(self):
        """Main analysis function"""
        bug_id = self.bug_id_entry.get().strip()
        
        if not bug_id:
            messagebox.showwarning("Warning", "Please enter a JIRA Bug ID")
            return
        
        # Validate configuration
        if not self.config.get('jira_email') or not self.config.get('jira_api_token'):
            messagebox.showerror("Error", 
                               "Please configure JIRA credentials in the Configuration tab")
            return
        
        # Clear previous results
        self.bug_details_text.delete(1.0, tk.END)
        self.bug_fix_text.delete(1.0, tk.END)
        
        # Disable button and show progress
        self.analyze_button.config(state='disabled')
        self.progress.start()
        self.status_label.config(text=f"Fetching JIRA bug {bug_id}...")
        self.root.update()
        
        try:
            # Fetch JIRA bug
            self.status_label.config(text=f"Analyzing {bug_id} with JIRA API...")
            self.root.update()
            bug_data = self.fetch_jira_bug(bug_id)
            
            # Format and display bug details
            bug_details = self.format_bug_details(bug_data)
            self.bug_details_text.insert(1.0, bug_details)
            
            # Generate AI analysis
            self.status_label.config(text="Generating Copilot Chat prompt...")
            self.root.update()
            analysis = self.generate_copilot_analysis(bug_data)
            self.bug_fix_text.insert(1.0, analysis)
            
            self.status_label.config(text=f"✓ Copilot prompt generated for {bug_id} - Click 'Copy Prompt' button!")
            messagebox.showinfo("Success", 
                              f"Copilot Chat prompt generated for {bug_id}!\n\n"
                              "Next steps:\n"
                              "1. Click 'Copy Prompt' button\n"
                              "2. Open VS Code\n"
                              "3. Open Copilot Chat (Ctrl+Alt+I or Cmd+Shift+I)\n"
                              "4. Paste and press Enter")
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.status_label.config(text="Error occurred during analysis")
            self.bug_fix_text.insert(1.0, error_msg)
            messagebox.showerror("Error", error_msg)
        
        finally:
            # Re-enable button and stop progress
            self.analyze_button.config(state='normal')
            self.progress.stop()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = JiraAnalyzerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
