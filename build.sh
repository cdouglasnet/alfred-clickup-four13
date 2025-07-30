#!/bin/bash
# Build script for ClickUp Alfred Workflow

WORKFLOW_NAME="ClickUp"
BUNDLE_ID="com.four13digital.clickup"
VERSION="1.0.1"

echo "Building $WORKFLOW_NAME v$VERSION..."

# Create temp directory
TEMP_DIR=$(mktemp -d)
BUILD_DIR="$TEMP_DIR/$WORKFLOW_NAME"

# Copy all necessary files
mkdir -p "$BUILD_DIR"

# Copy Python files and images
cp *.py "$BUILD_DIR/" 2>/dev/null || true
cp *.png "$BUILD_DIR/" 2>/dev/null || true
cp info.plist "$BUILD_DIR/"

# Copy directories with all subdirectories preserved, excluding __pycache__
rsync -a --exclude='__pycache__' --exclude='*.pyc' --exclude='.DS_Store' workflow/ "$BUILD_DIR/workflow/"
rsync -a --exclude='__pycache__' --exclude='*.pyc' --exclude='.DS_Store' emoji/ "$BUILD_DIR/emoji/"
rsync -a --exclude='__pycache__' --exclude='*.pyc' --exclude='.DS_Store' requests/ "$BUILD_DIR/requests/"
rsync -a --exclude='__pycache__' --exclude='*.pyc' --exclude='.DS_Store' urllib3/ "$BUILD_DIR/urllib3/"
rsync -a --exclude='__pycache__' --exclude='*.pyc' --exclude='.DS_Store' certifi/ "$BUILD_DIR/certifi/"
rsync -a --exclude='__pycache__' --exclude='*.pyc' --exclude='.DS_Store' chardet/ "$BUILD_DIR/chardet/"
rsync -a --exclude='__pycache__' --exclude='*.pyc' --exclude='.DS_Store' idna/ "$BUILD_DIR/idna/"

# Update version in info.plist if needed
sed -i '' "s/<string>1.0.0<\/string>/<string>$VERSION<\/string>/g" "$BUILD_DIR/info.plist"

# Create the .alfredworkflow file (just a zip)
cd "$BUILD_DIR"
zip -r "$OLDPWD/$WORKFLOW_NAME.alfredworkflow" .

# Cleanup
rm -rf "$TEMP_DIR"

echo "✓ Built $WORKFLOW_NAME.alfredworkflow"
echo "  Version: $VERSION"
echo "  Location: $OLDPWD/$WORKFLOW_NAME.alfredworkflow"