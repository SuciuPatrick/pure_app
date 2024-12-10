#!/bin/bash
set -e

echo "Running tests..."
pytest -v --no-migrations "$@"
