# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an Alfred workflow for ClickUp 2.0 integration, allowing users to quickly create and search tasks within ClickUp using Alfred. The workflow is written in Python 2.7 and uses the Alfred-Workflow library.

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

### Python 2.7 Compatibility
This project uses Python 2.7 (legacy). Key considerations:
- Use `from __future__ import unicode_literals` 
- Handle encoding with `sys.setdefaultencoding('utf-8')`
- Use `reload(sys)` for encoding setup