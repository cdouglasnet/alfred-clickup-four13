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
cp -R *.py *.png icon.png info.plist "$BUILD_DIR/"
cp -R workflow/ emoji/ fuzzy.py "$BUILD_DIR/"
cp -R requests/ urllib3/ certifi/ chardet/ idna/ "$BUILD_DIR/"

# Update version in info.plist if needed
sed -i '' "s/<string>1.0.0<\/string>/<string>$VERSION<\/string>/g" "$BUILD_DIR/info.plist"

# Create the .alfredworkflow file (just a zip)
cd "$TEMP_DIR"
zip -r "$WORKFLOW_NAME.alfredworkflow" "$WORKFLOW_NAME"

# Move to original directory
mv "$WORKFLOW_NAME.alfredworkflow" "$OLDPWD/"

# Cleanup
rm -rf "$TEMP_DIR"

echo "✓ Built $WORKFLOW_NAME.alfredworkflow"
echo "  Version: $VERSION"
echo "  Location: $(pwd)/$WORKFLOW_NAME.alfredworkflow"