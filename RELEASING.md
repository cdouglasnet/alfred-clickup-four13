# Release Process

This document describes how to create a new release of the ClickUp Alfred Workflow.

## Automated Release Process

The workflow uses GitHub Actions to automatically build and release new versions when you create a tag.

### Steps to Create a Release

1. **Update Version Number**
   ```bash
   # Update version in info.plist
   plutil -replace version -string "1.0.2" info.plist
   
   # Verify the change
   plutil -extract version raw info.plist
   ```

2. **Update README Badge**
   - Edit README.md and update the version badge to match

3. **Commit Version Changes**
   ```bash
   git add info.plist README.md
   git commit -m "Bump version to 1.0.2"
   git push origin master
   ```

4. **Create and Push Tag**
   ```bash
   # Create tag matching the version in info.plist
   git tag -a v1.0.2 -m "Release version 1.0.2"
   
   # Push tag to trigger release
   git push origin v1.0.2
   ```

5. **Monitor Release**
   - Go to [Actions tab](https://github.com/four13co/alfred-clickup-four13/actions)
   - Watch the "Build and Release Alfred Workflow" workflow
   - Once complete, check [Releases page](https://github.com/four13co/alfred-clickup-four13/releases)

## Manual Release Process (if needed)

If the automated process fails, you can create a release manually:

1. **Build Locally**
   ```bash
   ./build.sh
   ```

2. **Create Release on GitHub**
   - Go to [Releases page](https://github.com/four13co/alfred-clickup-four13/releases)
   - Click "Draft a new release"
   - Choose your tag (e.g., v1.0.2)
   - Title: "ClickUp Alfred Workflow v1.0.2"
   - Upload the `ClickUp.alfredworkflow` file
   - Add release notes
   - Publish release

## Version Numbering

We follow semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking changes (e.g., 2.0.0)
- **MINOR**: New features, backwards compatible (e.g., 1.1.0)
- **PATCH**: Bug fixes (e.g., 1.0.1)

## Pre-release Checklist

Before creating a release:

- [ ] All tests pass locally
- [ ] No hardcoded credentials in code
- [ ] info.plist version updated
- [ ] README.md version badge updated
- [ ] CHANGELOG updated (if maintaining one)
- [ ] All changes committed and pushed
- [ ] PR merged to master (if applicable)

## Post-release Tasks

After releasing:

1. **Announce the Release**
   - Update any documentation sites
   - Post in relevant forums/communities
   - Tweet about major releases

2. **Monitor Issues**
   - Watch for bug reports
   - Be ready to hotfix if needed

## Troubleshooting

### Version Mismatch Error
If you get a version mismatch error, ensure:
- Tag version matches info.plist version exactly
- Format: tag `v1.0.2` should match info.plist `1.0.2`

### Build Failures
- Check GitHub Actions logs
- Ensure all Python files have valid syntax
- Verify info.plist is valid XML

### Missing Artifact
- Ensure build.sh has execute permissions
- Check that all required files are present
- Verify workflow directory structure