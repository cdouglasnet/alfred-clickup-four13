# ClickUp API v2 to v3 Migration Plan

## Current API v2 Usage

The workflow currently uses ClickUp API v2 extensively. Here's an inventory of all v2 endpoints:

### Task Operations
- `GET /api/v2/team/{team_id}/task` - Search/list tasks (getTasks.py:42)
- `POST /api/v2/list/{list_id}/task` - Create task (createTask.py:88)
- `PUT /api/v2/task/{task_id}` - Update task status/close (closeTask.py:33)

### Organization Structure
- `GET /api/v2/team` - Get workspaces (config.py:266)
- `GET /api/v2/team/{workspace_id}/space` - Get spaces (config.py:197)
- `GET /api/v2/space/{space_id}/folder` - Get folders (config.py:346)
- `GET /api/v2/folder/{folder_id}/list` - Get lists from folder (config.py:108)
- `GET /api/v2/space/{space_id}/list` - Get lists from space (config.py:111)
- `GET /api/v2/team/{team_id}/list` - Get all lists (main.py:141)

### Metadata
- `GET /api/v2/space/{space_id}/tag` - Get available tags (main.py:40)
- `GET /api/v2/user` - Get current user info (createTask.py:36)

### Validation
- `GET /api/v2/{type}/{id}` - Generic validation endpoint (config.py:535)

## API v3 Changes

### 1. Terminology Updates
- **v2**: "Team" → **v3**: "Workspace"
- More consistent naming conventions
- Clearer resource relationships

### 2. Endpoint Structure
Based on current ClickUp documentation:
- v3 endpoints follow pattern: `/api/v3/workspaces/{workspaceId}/...`
- Not all endpoints have v3 equivalents yet
- Some v3 endpoints have different response structures

### 3. Known v3 Endpoints
Currently documented v3 endpoints:
- Docs operations
- Some workspace operations
- Limited task operations

## Migration Strategy

### Phase 1: Compatibility Layer (Immediate)
1. Create `api_client.py` wrapper module
2. Abstract all API calls through this module
3. Support both v2 and v3 endpoints
4. Example:
```python
class ClickUpAPI:
    def __init__(self, api_key, api_version='v2'):
        self.api_key = api_key
        self.api_version = api_version
        self.base_url = f'https://api.clickup.com/api/{api_version}'
    
    def get_tasks(self, workspace_id, **params):
        if self.api_version == 'v2':
            url = f'{self.base_url}/team/{workspace_id}/task'
        else:  # v3
            url = f'{self.base_url}/workspaces/{workspace_id}/tasks'
        return self._make_request('GET', url, params=params)
```

### Phase 2: Gradual Migration (As v3 Endpoints Available)
1. Monitor ClickUp API changelog
2. Update individual endpoints as v3 equivalents released
3. Maintain backward compatibility
4. Test thoroughly with both versions

### Phase 3: Full v3 Migration (Future)
1. Once all used endpoints have v3 equivalents
2. Deprecate v2 support
3. Update documentation
4. Major version bump (2.0)

## Implementation Checklist

### Immediate Actions
- [ ] Create API compatibility layer
- [ ] Add configuration for API version preference
- [ ] Update error handling for v3 responses
- [ ] Add logging for API version usage

### Per-Endpoint Migration
- [ ] Tasks search/list
- [ ] Task creation
- [ ] Task updates
- [ ] Workspace listing
- [ ] Space operations
- [ ] Folder operations
- [ ] List operations
- [ ] Tag retrieval
- [ ] User info

### Testing Requirements
- [ ] Unit tests for both v2 and v3 endpoints
- [ ] Integration tests with real API
- [ ] Performance comparison v2 vs v3
- [ ] Error handling for missing v3 endpoints

## Risk Mitigation

1. **Gradual Rollout**: Use feature flags to enable v3 per endpoint
2. **Fallback Logic**: Automatically fall back to v2 if v3 fails
3. **Version Detection**: Check which API versions are available
4. **User Communication**: Clear messages about API version in use

## Benefits of v3

1. **Better Performance**: Potentially optimized endpoints
2. **Clearer Structure**: More intuitive resource paths
3. **Enhanced Features**: New capabilities not in v2
4. **Future-Proof**: v2 will eventually be deprecated

## Timeline Estimate

- **Phase 1**: 1-2 weeks (compatibility layer)
- **Phase 2**: Ongoing as v3 endpoints released
- **Phase 3**: 6-12 months (depends on ClickUp)

## Notes

1. ClickUp hasn't announced v2 deprecation timeline
2. v3 is still in active development
3. Some v3 endpoints may have breaking changes
4. Need to monitor ClickUp developer announcements

## Resources

- [ClickUp API Changelog](https://developer.clickup.com/changelog)
- [API v2 vs v3 Terminology](https://developer.clickup.com/docs/general-v2-v3-api)
- [ClickUp Developer Portal](https://developer.clickup.com)