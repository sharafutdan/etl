#!/bin/bash
set -e

echo "Running ruff linter..."
ruff check --exit-non-zero-on-fix

echo "Running ruff formatter..."
ruff format
