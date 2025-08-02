# Title-Only Search Feature

## Problem Statement
Currently, the ClickUp API's `query` parameter searches across multiple fields including:
- Task titles/names
- Task descriptions
- Comments
- Custom fields

This can lead to false positives where users search for a specific task by name but get results where the search term only appears deep in descriptions or comments.

## Proposed Solution: Search Modifiers

Implement search modifiers that allow users to control search scope on a per-query basis.

### Syntax Options
```bash
# Default behavior - full search (current)
cus integration

# Title-only search with short modifier
cus t:integration

# Title-only search with full modifier  
cus title:integration

# Future expansion possibilities
cus d:integration     # Description only
cus c:integration     # Comments only
```

### Why This Approach?
1. **Discoverable** - Users can learn about it through documentation
2. **Flexible** - Choose search scope per query without config changes
3. **Familiar** - Follows patterns from GitHub (`in:title`), Gmail, etc.
4. **Extensible** - Can add more modifiers in the future
5. **Backward Compatible** - Existing searches work unchanged

## Implementation Details

### 1. Query Parser
```python
def parse_search_query(query):
    """
    Parse query for search modifiers.
    Returns: (search_mode, clean_query)
    """
    if query.startswith('t:') or query.startswith('title:'):
        mode = 'title'
        clean_query = query.split(':', 1)[1].strip()
    elif query.startswith('d:') or query.startswith('desc:'):
        mode = 'description'
        clean_query = query.split(':', 1)[1].strip()
    else:
        mode = 'all'
        clean_query = query
    
    return mode, clean_query
```

### 2. Result Filtering
Since ClickUp API doesn't support title-only search, we need client-side filtering:

```python
# In getTasks.py, after receiving API results
if search_mode == 'title':
    # Filter tasks where query appears in title
    filtered_tasks = []
    for task in result['tasks']:
        task_name = task.get('name', '').lower()
        if clean_query.lower() in task_name:
            filtered_tasks.append(task)
    result['tasks'] = filtered_tasks

# Similar filtering for docs
if search_mode == 'title' and docs_results:
    filtered_docs = []
    for doc in docs_results:
        doc_title = doc.get('title', '').lower()
        if clean_query.lower() in doc_title:
            filtered_docs.append(doc)
    docs_results = filtered_docs
```

### 3. User Interface Updates
- Update empty search message to mention modifiers
- Add help text in configuration
- Update README with examples

## Alternative Approaches Considered

### 1. Configuration Toggle
- Pro: Set once and forget
- Con: Less flexible, requires config change for different search types

### 2. Separate Commands (cus vs cust)
- Pro: Very clear separation
- Con: More commands to remember, clutters Alfred

### 3. Smart Default (title-only by default)
- Pro: Reduces false positives for most users
- Con: Breaking change, might confuse existing users

## Testing Plan
1. Test with queries containing special characters
2. Test with empty modifiers (e.g., `t:`)
3. Test case sensitivity
4. Test with very long queries
5. Performance test with 100+ results

## Future Enhancements
1. Multiple modifiers: `cus t:shopify d:integration`
2. Negative modifiers: `cus -t:draft` (exclude drafts)
3. Regex support: `cus t:/^SHOP-\d+/`
4. Save common searches as Alfred snippets

## User Documentation
Add to README.md:
```markdown
### Search Modifiers
Control what fields are searched:
- `cus t:shopify` - Search only in task/doc titles
- `cus shopify` - Search everywhere (default)

Coming soon: `d:` for descriptions, `c:` for comments
```