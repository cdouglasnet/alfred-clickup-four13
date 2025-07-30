# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an Alfred workflow for ClickUp 2.0 integration by Four13 Digital, allowing users to quickly create and search tasks within ClickUp using Alfred. The workflow is written in Python 3.9+ and uses the alfred-pyworkflow library.

## Key Architecture Components

### Main Entry Points
- `main.py` - Primary script for creating tasks with the `cu` command
- `getTasks.py` - Script for searching tasks (`cus`, `cuo`, `cul` commands)
- `createTask.py` - Handles the actual task creation via ClickUp API
- `closeTask.py` - Handles closing tasks via the API
- `config.py` - Configuration management interface
- `configStore.py` - Stores configuration values in macOS Keychain or workflow settings

### Core Dependencies
- `workflow/` - Alfred-Workflow library for Alfred integration
- `requests/` - HTTP library for API calls
- `emoji/` - Emoji support for task formatting
- `fuzzy.py` - Fuzzy matching for search functionality

### Configuration Storage
- API keys are stored in macOS Keychain for security
- Other settings stored in Alfred workflow settings
- Configuration accessed via `getConfigValue()` function

## Common Development Tasks

### Testing the Workflow
There are no automated tests. To test:
1. Install the workflow in Alfred by opening the `.alfredworkflow` file
2. Configure via `cu:config` command
3. Test task creation with `cu <task title>`
4. Test search with `cus <search term>`

### Debugging
- Set `DEBUG = 2` in Python files for verbose logging
- Logs available in Alfred's debug console
- Use `log.debug()` for debug output

### API Integration
- ClickUp API v2 endpoints used throughout
- Authentication via API token in headers
- Key endpoints:
  - `/api/v2/task` - Create tasks
  - `/api/v2/team/{team_id}/task` - Search tasks
  - `/api/v2/space/{space_id}/tag` - Get tags
  - `/api/v2/team/{team_id}/list` - Get lists

### Python 3.9+ Modern Implementation
This project uses Python 3.9+ for modern macOS compatibility. Key features:
- Native Unicode string handling (no encoding setup needed)
- Modern exception handling and syntax
- Compatible with macOS system Python 3.9.6+
- Uses alfred-pyworkflow for Alfred 5+ compatibility

## Project Information
- **Author**: Greg Flint - Four13 Digital  
- **Bundle ID**: com.four13digital.clickup
- **Version**: 1.0.0
- **Repository**: https://github.com/four13co/alfred-clickup-four13
- **Website**: https://four13.digital