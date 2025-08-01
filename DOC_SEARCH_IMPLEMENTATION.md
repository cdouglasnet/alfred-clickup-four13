# Doc Search Implementation Plan

## Overview
Add document title search to the `cus` command using ClickUp's v3 Docs API endpoint.

## Implementation Details

### 1. Configuration
Add new option to `searchEntities` config:
- `tasks` - Current behavior (default)
- `tasks+docs` - Search tasks and doc titles
- `all` - Search tasks, folders, spaces, and doc titles

### 2. API Integration

#### Add to getTasks.py:
```python
# If searchEntities includes docs
if search_entities in ['tasks+docs', 'all']:
    # Fetch docs using v3 API
    docs_url = f'https://api.clickup.com/api/v3/workspaces/{workspace_id}/docs'
    try:
        docs_response = web.get(docs_url, headers=headers)
        docs_response.raise_for_status()
        docs_data = docs_response.json()
        
        # Add docs to results with type indicator
        for doc in docs_data.get('docs', []):
            doc_title = doc.get('name', 'Untitled Document')
            wf3.add_item(
                title = f'[Doc] {doc_title}',
                subtitle = 'ClickUp Document',
                match = doc_title,  # For fuzzy matching
                valid = True,
                arg = doc.get('url', f'https://app.clickup.com/{workspace_id}/d/{doc["id"]}'),
                icon = 'doc.png'  # Need to add doc icon
            )
    except Exception as e:
        log.debug(f'Failed to fetch docs: {e}')
        # Continue with task results even if docs fail
```

### 3. Visual Design
- Prefix: `[Doc]` in title
- Icon: Document icon (need to add `doc.png`)
- Subtitle: "ClickUp Document" or doc location if available
- Action: Open doc URL in browser

### 4. Performance Considerations
- Docs API call happens in parallel with task search
- Cache docs for longer (5-10 minutes) as they change less frequently
- If docs API fails, still show task results

### 5. Benefits
- First v3 API implementation
- Adds valuable search functionality
- Simple to implement (no content search needed)
- Low risk - additive feature

### 6. Future Enhancements
- Add folder/space info to doc subtitle
- Show last modified date
- Filter by doc owner
- Search within doc content (if API adds this)

## Testing Plan
1. Test with workspace containing 0, 1, 10, 100+ docs
2. Verify fuzzy matching works on doc titles
3. Test error handling if v3 API fails
4. Ensure performance with large doc counts
5. Verify doc URLs open correctly

## Migration Path
This creates our first v2/v3 hybrid implementation:
- Tasks use v2: `/api/v2/team/{team_id}/task`
- Docs use v3: `/api/v3/workspaces/{workspace_id}/docs`

Note: `workspace_id` in v3 is the same value as `team_id` in v2.