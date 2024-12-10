#!/bin/bash
set -e

echo "Running tests..."
pytest -s -v --no-migrations
