# Installation Guide

## Quick Install

1. **Download** `ClickUp.alfredworkflow` from this repository
2. **Double-click** the file to install in Alfred
3. **Configure** your ClickUp API credentials

## Step-by-Step Setup

### 1. Get Your ClickUp API Key
1. Open [ClickUp](https://app.clickup.com) → Profile Icon → **Apps**
2. Click **Generate API Key**  
3. Copy the key (starts with `pk_`)

### 2. Configure the Workflow
Type `cu:config` in Alfred and enter:
- **API Key**: Your ClickUp API token
- **Workspace ID**: Found in ClickUp URLs (7 digits)
- **Space ID**: Found in ClickUp URLs (7 digits)  
- **List ID**: Your default list for new tasks (7 digits)

### 3. Find Your IDs
**Workspace**: `https://app.clickup.com/2181159/...` → Use `2181159`
**Space**: `https://app.clickup.com/.../s/2288348` → Use `2288348`  
**List**: Hover over list → ⋯ → 🔗 → `https://app.clickup.com/.../li/4646883` → Use `4646883`

### 4. Test the Workflow
```
cu Test task #workflow @h1 !3
```

## Requirements
- macOS 10.15+
- Alfred 4+ with Powerpack
- ClickUp 2.0 account
- Python 3.9+ (included with macOS)

## Troubleshooting
- Run `cu:config validate` to test your settings
- Check Alfred's debug console for errors
- See [README.md](README.md) for detailed documentation

---
**Made with ❤️ by [Four13 Digital](https://four13.digital)**