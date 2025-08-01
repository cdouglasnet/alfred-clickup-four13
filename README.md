# ClickUp Alfred Workflow

**Streamline your ClickUp task management directly from Alfred**

[![Build Status](https://github.com/four13co/alfred-clickup-four13/actions/workflows/build-release.yml/badge.svg)](https://github.com/four13co/alfred-clickup-four13/actions)
[![Version](https://img.shields.io/badge/version-1.12-blue.svg)](https://github.com/four13co/alfred-clickup-four13/releases)
[![Python](https://img.shields.io/badge/python-3.9+-green.svg)](https://python.org)
[![Alfred](https://img.shields.io/badge/alfred-5%2B-purple.svg)](https://alfredapp.com)
[![License](https://img.shields.io/badge/license-GPL%20v2.0-red.svg)](LICENSE)

*Created by [Greg Flint](https://github.com/gregflint) • [Four13 Digital](https://github.com/four13co)*

## Overview

This Alfred workflow integrates seamlessly with ClickUp 2.0, allowing you to create tasks, search existing tasks, and manage your ClickUp workspace without leaving your keyboard. Built with Python 3.9+ for maximum compatibility with modern macOS systems.

![ClickUp Workflow Demo](docs/ClickUp.gif)

## ✨ Features

### 🎯 **Quick Task Creation** (`cu`)
Create ClickUp tasks with natural language parsing:
```
cu Clean the kitchen :Before my wife gets angry #Housework @h4 !1 +Personal
```
- **Title**: `Clean the kitchen`
- **Description**: `:Before my wife gets angry` 
- **Tags**: `#Housework` (with autocomplete)
- **Due Date**: `@h4` (4 hours from now)
- **Priority**: `!1` (Urgent: 1=Urgent, 2=High, 3=Normal, 4=Low)
- **List**: `+Personal` (with autocomplete)

### 🔍 **Powerful Task Search**
- **`cus <search>`** - Search all tasks with fuzzy matching
- **`cuo [search]`** - Show tasks due today or overdue
- **`cul [search]`** - Show tasks created via Alfred (filtered by default tag)

### ⚙️ **Smart Configuration** (`cu:config`)
- Secure API key storage in macOS Keychain
- Workspace, Space, Folder, and List configuration
- Default settings for due dates, tags, and notifications
- Configuration validation with real-time API testing

### 🛡️ **Security & Privacy**
- API keys stored securely in macOS Keychain
- No sensitive data stored in plain text
- Full control over your ClickUp access

## 🚀 Installation

### Requirements
- **macOS 10.15+** (Catalina or later)
- **Alfred 4+** with [Powerpack](https://www.alfredapp.com/powerpack/)
- **ClickUp 2.0** account
- **Python 3.9+** (included with macOS)

### Quick Install
1. **Download** the [latest release](https://github.com/four13co/alfred-clickup-four13/releases/latest)
2. **Double-click** the `.alfredworkflow` file to install
3. **Configure** your ClickUp credentials (see setup below)

## ⚡ Quick Start

### 1. Get Your ClickUp API Key
1. Open ClickUp → Profile Icon (bottom left) → **Apps**
2. Click **Generate API Key**
3. Copy your API key (treat it like a password!)

### 2. Configure the Workflow
Type `cu:config` in Alfred and set up:

| Setting | Description | Example |
|---------|-------------|---------|
| **API Key** | Your ClickUp API token | `pk_12345_abc...` |
| **Workspace ID** | ClickUp Workspace ID | `2181159` |
| **Space ID** | Space for tags/priorities | `2288348` |
| **List ID** | Default list for new tasks | `4696187` |
| **Default Tag** | Auto-added to all tasks | `alfred-created` |

### 3. Find Your IDs
**Workspace ID**: Go to any task → URL shows `https://app.clickup.com/2181159/...` → Use `2181159`

**Space ID**: Click Space icon → URL shows `https://app.clickup.com/.../s/2288348` → Use `2288348`

**List ID**: Hover over a List → Click ⋯ → Click 🔗 → URL shows `https://app.clickup.com/.../li/4646883` → Use `4646883`

### 4. Start Creating Tasks!
```
cu Review Q4 budget :Need to finish by Friday #finance @fri !2
```

## 📚 Usage Guide

### Task Creation (`cu`)

**Basic Syntax:**
```
cu <Title> [:<Description>] [#<Tag>] [@<Due Date>] [!<Priority>] [+<List>]
```

**Due Date Options:**
- `@m30` - 30 minutes from now
- `@h2` - 2 hours from now  
- `@d3` - 3 days from now
- `@w1` - 1 week from now
- `@today` or `@tod` - Today
- `@tomorrow` or `@tom` - Tomorrow
- `@monday` or `@mon` - Next Monday
- `@2024-12-31` - Specific date
- `@2024-12-31 14.00` - Specific date and time
- `@14.00` - Today at 2 PM

**Priority Levels:**
- `!1` - 🔴 Urgent
- `!2` - 🟡 High  
- `!3` - 🟢 Normal (default)
- `!4` - 🔵 Low

**Examples:**
```bash
# Simple task
cu Call mom

# Task with description and tag
cu Review proposal :Check the new client requirements #work

# Complex task with all options
cu Deploy website :Final review and testing #dev @fri !1 +Projects

# Multiple tags
cu Plan vacation #personal #travel @w2 !3
```

### Task Search

**Search All Tasks (`cus`)**
```bash
cus budget          # Find tasks containing "budget"
cus [Open]          # Filter by status
```

**Open Tasks (`cuo`)**
```bash
cuo                 # Show all due/overdue tasks
cuo urgent          # Filter overdue tasks
```

**Alfred-Created Tasks (`cul`)**
```bash
cul                 # Show all tasks created via Alfred
cul review          # Filter Alfred tasks
```

### Keyboard Shortcuts
- **Enter** → Open task in ClickUp (web)
- **⌥ + Enter** → Close/complete task
- **⌥ + Enter** (creation) → Create task and open in ClickUp

## 🔧 Advanced Configuration

### Hierarchy Limits
Limit search results by organizational level:
- `space` - Limit to configured Space
- `folder` - Limit to configured Folder  
- `list` - Limit to configured List
- `space,folder` - Combine multiple levels

### Default Settings
- **Default Due Date**: Set automatic due date (e.g., `h2` for 2 hours)
- **Default Tag**: Auto-added to every task for easy filtering
- **Notifications**: Toggle desktop notifications on task creation

### API Rate Limits
- Tags cached for 10 minutes
- Lists cached for 2 hours
- Automatic cache invalidation on errors

## 🛠️ Technical Details

### Architecture
- **Python 3.9+** for modern macOS compatibility
- **alfred-pyworkflow** library for Alfred integration
- **ClickUp API v2** for full feature support
- **Secure keychain storage** for credentials

### File Structure
```
alfred-clickup-four13/
├── main.py              # Main workflow entry point
├── createTask.py        # Task creation logic
├── getTasks.py          # Task search and retrieval
├── closeTask.py         # Task completion
├── config.py            # Configuration interface
├── configStore.py       # Settings storage
├── fuzzy.py             # Fuzzy search functionality
├── workflow/            # Alfred workflow library
├── info.plist           # Alfred workflow configuration
└── *.png               # UI icons
```

### Customization
All workflow behavior can be customized through:
- Alfred workflow variables
- ClickUp configuration settings
- Python script modifications

## 🐛 Troubleshooting

### Common Issues

**"We are missing some settings"**
- Run `cu:config` and set up all required fields
- Use `cu:config validate` to test your configuration

**"Error connecting to ClickUp"**
- Check your internet connection
- Verify your API key is correct
- Ensure your Workspace/Space/List IDs are valid

**Tasks not appearing in search**
- Check your hierarchy limit settings
- Verify you have access to the configured Workspace
- Clear cache with `cu:config cache`

### Debug Mode
Enable debug logging by editing Python files:
```python
DEBUG = 2  # 0=Off, 1=Some, 2=All
```

View logs in Alfred's debug console (Alfred → Workflows → ClickUp → Debug).

## 🤝 Contributing

We welcome contributions! Here's how to help:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'Add amazing feature'`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### Development Setup
```bash
git clone https://github.com/four13co/alfred-clickup-four13.git
cd alfred-clickup-four13
# Edit Python files with your favorite editor
# Test with: /usr/bin/python3 main.py "test input"
```

## 📝 Changelog

### v1.0.0 (2025-07-30)
- **🚀 Python 3.9+ Migration**: Complete upgrade from Python 2.7
- **⚡ Modern Compatibility**: Works with latest macOS versions  
- **🔧 Library Updates**: Migrated to alfred-pyworkflow
- **🛡️ Enhanced Security**: Improved keychain integration
- **📚 Documentation**: Comprehensive setup and usage guides
- **🎨 UI Improvements**: Refined user experience

### Previous Versions
See [releases](https://github.com/four13co/alfred-clickup-four13/releases) for complete history.

## 📄 License

This project is licensed under the GNU General Public License v2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Original Concept**: Based on alfred-clickup-msk by Michael Schmidt-Korth
- **Alfred Workflow Library**: Built with alfred-pyworkflow by Thomas Harr
- **ClickUp Team**: For providing an excellent API
- **Alfred Team**: For creating the amazing Alfred app

## 📞 Support

**Need Help?**
- 📖 Check the [Wiki](https://github.com/four13co/alfred-clickup-four13/wiki)
- 🐛 Report issues: [GitHub Issues](https://github.com/four13co/alfred-clickup-four13/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/four13co/alfred-clickup-four13/discussions)

**Four13 Digital**
- 🌐 Website: [four13.digital](https://four13.digital)
- 💼 GitHub: [@four13co](https://github.com/four13co)
- 👨‍💻 Author: [Greg Flint](https://github.com/gregflint)

---

**⚡ Made with ❤️ by Four13 Digital**

*Streamline your workflow. Amplify your productivity.*