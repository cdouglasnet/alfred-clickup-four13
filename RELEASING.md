# Release Process

This document describes how to create a new release of the ClickUp Alfred Workflow.

## Automated Release Process

The workflow automatically creates releases when changes are merged to the main/master branch.

### Steps to Create a Release

1. **Update Version Number in Your Branch**
   ```bash
   # Update version in info.plist
   plutil -replace version -string "1.13" info.plist
   
   # Verify the change
   plutil -extract version raw info.plist
   ```

2. **Update README Badge**
   - Edit README.md and update the version badge to match

3. **Commit Version Changes**
   ```bash
   git add info.plist README.md
   git commit -m "Bump version to 1.13"
   git push origin your-feature-branch
   ```

4. **Create Pull Request and Merge**
   - Create a PR to main/master
   - Once approved and merged, the release will be created automatically

5. **Automatic Release Process**
   When your PR is merged to main/master:
   - GitHub Actions will automatically build the workflow
   - If the version in info.plist is new, it will create a release
   - If the version already exists, it will skip the release
   - The workflow file will be attached to the release

6. **Monitor Release**
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

We use a simple two-digit versioning system (MAJOR.MINOR):

- **MAJOR**: Major rewrites or breaking changes (e.g., 2.0)
- **MINOR**: All other updates including features and fixes (e.g., 1.12, 1.13)

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

### Version Already Released
If the version was already released:
- The workflow will skip creating a duplicate release
- You need to increment the version number (e.g., 1.12 → 1.13)

### Build Failures
- Check GitHub Actions logs
- Ensure all Python files have valid syntax
- Verify info.plist is valid XML

### Missing Artifact
- Ensure build.sh has execute permissions
- Check that all required files are present
- Verify workflow directory structure