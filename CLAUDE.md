# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an Alfred workflow for ClickUp 2.0 integration by Four13 Digital, allowing users to quickly create and search tasks within ClickUp using Alfred. The workflow is written in Python 3.9+ and uses the alfred-pyworkflow library.

**IMPORTANT**: This workflow is designed for public distribution. It must NOT contain any hardcoded API keys, credentials, or personal data. All sensitive information must be stored securely in the macOS Keychain or user settings.

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

### Security Requirements
- **NEVER hardcode API keys or credentials in source code**
- **ALWAYS mask sensitive data when displaying in UI** (show only partial values)
- **Store all sensitive data in macOS Keychain** using `wf.save_password()`
- **This is redistributable software** - assume all code will be public

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

## Critical Lessons Learned

### Successful Workflow Build Process
1. **Use the build script**: `bash build.sh`
2. **Verify the build**: `unzip -l ClickUp.alfredworkflow | head`
3. **Install with Alfred**: `open -a "Alfred 5" ClickUp.alfredworkflow`
4. **Test configuration**: Try `cu:config` to ensure no import errors

### Workflow Packaging and Testing
**IMPORTANT**: When building/modifying the workflow, always test the actual `.alfredworkflow` file installation, not just local Python execution. Issues that work locally may fail in Alfred due to:
- Module import paths 
- Directory structure preservation
- Python environment differences

### Known Issues and Fixes

#### 1. ClickUp ID Length Validation
- **Issue**: Original code enforced 7-character limit on all ClickUp IDs
- **Fix**: Remove `len(userInput) != 7` checks from `config.py`
- **Location**: Lines ~78, 84, 90, 96 in config.py
- **Why**: Modern ClickUp IDs can be 14+ characters (e.g., `90170402244889`)

#### 2. Configuration Storage Bug
- **Issue**: `config.py` line 141 had `query.split(' ') > 1` causing TypeError
- **Fix**: Change to `len(query.split(' ')) > 1`
- **Why**: Can't compare list to int in Python

#### 3. NoneType String Concatenation
- **Issue**: Config values returning `None` cause errors when concatenated
- **Fix**: Use `getConfigValue(...) or ''` to ensure string type
- **Why**: Python 3 is stricter about type operations

### Building and Packaging

#### Build Script (`build.sh`)
```bash
#!/bin/bash
# Critical: Preserve directory structure!
rsync -a --exclude='__pycache__' --exclude='*.pyc' workflow/ "$BUILD_DIR/workflow/"
# NOT cp -R which includes cache files

# CRITICAL: Zip files at root level!
cd "$BUILD_DIR"
zip -r "$OLDPWD/$WORKFLOW_NAME.alfredworkflow" .
# NOT: zip -r name.alfredworkflow foldername/
```

#### Common Packaging Mistakes
1. **DON'T** flatten directory structures - modules won't import
2. **DON'T** include `.git`, `__pycache__`, `*.pyc`, or `.DS_Store` files
3. **DON'T** create workflow with files in a subfolder - Alfred expects files at root
4. **DO** test the packaged workflow file, not just local execution
5. **DO** use `open -a "Alfred 5" ClickUp.alfredworkflow` to install
6. **DO** verify zip structure with `unzip -l workflow.alfredworkflow | head`

### Debugging Import Errors

#### "Unable to import" in Alfred
When Alfred shows "The workflow you are trying to import is invalid or corrupted":

1. **Check zip structure** (MOST COMMON ISSUE):
   ```bash
   unzip -l ClickUp.alfredworkflow | head
   # Files should be at root: info.plist, main.py, etc.
   # NOT: ClickUp/info.plist, ClickUp/main.py
   ```

2. **Verify info.plist**:
   ```bash
   plutil -lint info.plist  # Should output "OK"
   ```

3. **Check for Python syntax errors in info.plist**:
   ```bash
   grep -n "usr/bin/python" info.plist
   # Look for malformed entries like: ./fuzzy.py /usr/bin/python3
   ```

4. **Test by unpacking and running directly**:
   ```bash
   unzip ClickUp.alfredworkflow -d test
   cd test
   /usr/bin/python3 main.py "test"
   ```

#### Other Import Errors
- Missing module directories (e.g., `emoji/` not included)
- Incorrect import statements (`from workflow.util` vs `from .util`)
- Python cache files (`__pycache__`) causing conflicts

### Configuration Testing
To verify configuration is saved correctly:
```python
from workflow import Workflow
wf = Workflow()
# Check API key in keychain
api_key = wf.get_password('clickUpAPI')
# Check settings
print(wf.settings.get('list'))
```

### Best Practices
1. **Incremental Changes**: Make one fix at a time and test
2. **Preserve Working State**: Keep a known-working `.alfredworkflow` file
3. **Test Installation**: Always test by installing the workflow, not just running locally
4. **Version Control**: Tag working versions before making changes

## Project Information
- **Author**: Greg Flint - Four13 Digital  
- **Bundle ID**: com.four13digital.clickup
- **Version**: 1.0.0
- **Repository**: https://github.com/four13co/alfred-clickup-four13
- **Website**: https://four13.digital