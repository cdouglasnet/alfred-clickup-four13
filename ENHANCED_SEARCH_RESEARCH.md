# Enhanced Search Research for ClickUp Alfred Workflow

## Overview

This document outlines research into extending the `cus` (ClickUp search) command to search not just tasks, but also folders, spaces, and potentially chat spaces.

## Current State

The workflow currently searches only tasks using the ClickUp API v2 endpoint:
- `GET /api/v2/team/{team_id}/task`

## Research Findings

### 1. ClickUp API Entity Hierarchy

ClickUp has a clear hierarchy:
```
Workspace (Team)
  └── Spaces
      └── Folders
          └── Lists
              └── Tasks
```

### 2. Available Search/List Endpoints

#### Spaces
- **Endpoint**: `GET /api/v2/team/{team_id}/space`
- **Description**: Lists all spaces in a workspace
- **Search params**: None documented
- **Returns**: Array of space objects with id, name, etc.

#### Folders
- **Endpoint**: `GET /api/v2/space/{space_id}/folder`
- **Description**: Lists all folders in a space
- **Search params**: None documented
- **Returns**: Array of folder objects with id, name, lists, etc.

#### Lists
- **Endpoint**: `GET /api/v2/folder/{folder_id}/list` or `GET /api/v2/space/{space_id}/list`
- **Description**: Lists all lists in a folder or space
- **Search params**: None documented
- **Returns**: Array of list objects

#### Chat Spaces
- **Finding**: No dedicated chat space search API found
- **Note**: Chat appears to be integrated within tasks/comments rather than as separate searchable entities

### 3. Search Limitations

1. **No Universal Search**: ClickUp API v2 doesn't provide a universal search endpoint that searches across all entity types
2. **No Query Parameters**: The folder/space/list endpoints don't accept search/query parameters
3. **Client-Side Filtering Required**: To search folders/spaces by name, we'd need to:
   - Fetch all entities
   - Filter client-side using fuzzy matching

### 4. API v3 Status

- **Current State**: ClickUp is transitioning to API v3 but most endpoints remain v2
- **v3 Endpoints**: Limited to specific features (e.g., Docs search)
- **Migration Timeline**: No official timeline for full v3 release
- **Key Change**: v3 uses "Workspace" terminology instead of "Team"

## Proposed Implementation

### Phase 1: Enhanced Entity Search
1. Add configuration option: `searchEntities` with options:
   - `tasks` (default, current behavior)
   - `all` (tasks + folders + spaces)
   
2. Modify `getTasks.py` to:
   - Fetch tasks (existing functionality)
   - If `searchEntities=all`, also fetch:
     - All spaces from workspace
     - All folders from configured space
   - Combine results with type indicators

3. Update result display:
   - Prefix items with type: `[Task]`, `[Folder]`, `[Space]`
   - Use different icons for each type
   - Folders/Spaces open in ClickUp web when selected

### Phase 2: Performance Optimization
1. Cache folder/space data longer (they change less frequently)
2. Parallel API calls for different entity types
3. Progressive loading (show tasks first, then folders/spaces)

### Phase 3: API v3 Migration
1. Monitor ClickUp's v3 documentation
2. Create compatibility layer for v2→v3 transition
3. Update endpoints as v3 equivalents become available

## Technical Considerations

### 1. API Rate Limits
- Multiple API calls needed (tasks + spaces + folders)
- Consider caching strategy to minimize requests

### 2. Result Mixing
- How to sort mixed entity types?
- Fuzzy scoring might differ between task names and folder/space names

### 3. User Experience
- Clear visual distinction between entity types
- Keyboard shortcuts to filter by type?
- Different actions for different types (open vs create vs navigate)

## Implementation Priority

1. **High Priority**:
   - Add folder/space search to `cus`
   - Clear type indicators in results
   - Configuration toggle for feature

2. **Medium Priority**:
   - Performance optimizations
   - Advanced filtering options
   - Chat integration (if API becomes available)

3. **Low Priority**:
   - Full API v3 migration (wait for stable release)

## Example API Calls

### Get All Spaces
```python
url = f'https://api.clickup.com/api/v2/team/{team_id}/space'
headers = {'Authorization': api_key}
response = requests.get(url, headers=headers)
spaces = response.json()['spaces']
```

### Get All Folders in Space
```python
url = f'https://api.clickup.com/api/v2/space/{space_id}/folder'
headers = {'Authorization': api_key}
response = requests.get(url, headers=headers)
folders = response.json()['folders']
```

### Filter Results Client-Side
```python
# Fuzzy match against space/folder names
for space in spaces:
    if fuzzy_match(query, space['name']):
        results.append({
            'type': 'space',
            'name': space['name'],
            'id': space['id'],
            'url': f'https://app.clickup.com/{team_id}/v/s/{space["id"]}'
        })
```

## Next Steps

1. Implement basic folder/space search as experimental feature
2. Gather user feedback on UX preferences
3. Monitor ClickUp API v3 development
4. Consider creating ClickUp feature request for universal search endpoint