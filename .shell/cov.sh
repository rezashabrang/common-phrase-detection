#!/bin/bash
find . -name 'coverage.txt' -delete
poetry run pytest --cov-report term --cov phrase_counter tests/ >>.logs/coverage.txt
