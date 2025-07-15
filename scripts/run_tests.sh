#!/bin/bash
set -e

pytest --cov-report=html --cov=app tests/

