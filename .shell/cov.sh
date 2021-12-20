#!/bin/bash
find . -name 'coverage.txt' -delete
poetry run pytest --cov-report term --cov stop_counter tests/ >>.logs/coverage.txt
