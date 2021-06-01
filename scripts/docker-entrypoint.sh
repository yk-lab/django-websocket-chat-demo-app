#!/usr/bin/env bash

pipenv install --dev --ignore-pipfile
source .venv/bin/activate

exec "$@"
