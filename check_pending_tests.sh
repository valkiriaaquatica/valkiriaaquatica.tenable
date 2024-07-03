#!/usr/bin/env bash

### this script outputs the pending unit and integration tests that remain of the actual modules ###

COLLECTION_ROOT="$(pwd)"
MODULES_DIR="$COLLECTION_ROOT/plugins/modules"
UNIT_TESTS_DIR="$COLLECTION_ROOT/tests/unit/plugins/modules"
INTEGRATION_TESTS_DIR="$COLLECTION_ROOT/tests/integration/targets"

if [[ ! -d "$MODULES_DIR" || ! -d "$UNIT_TESTS_DIR" || ! -d "$INTEGRATION_TESTS_DIR" ]]; then
  echo "Not a valid directory. Please be on the root collection directory."
  exit 1
fi
for module_file in "$MODULES_DIR"/*.py; do
  module_name=$(basename "$module_file" .py)
  # unit
  unit_test_file="$UNIT_TESTS_DIR/test_${module_name}.py"
  if [[ -f "$unit_test_file" ]]; then
    unit_test_status="present"
  else
    unit_test_status="not present"
  fi

  # integration
  integration_test_dir="$INTEGRATION_TESTS_DIR/$module_name"
  if [[ -d "$integration_test_dir" ]]; then
    integration_test_status="present"
  else
    integration_test_status="not present"
  fi
    # prints
  echo "Module: $module_name"
  echo "  Unit test: $unit_test_status"
  echo "  Integration test: $integration_test_status"
done
