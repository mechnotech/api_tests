#!/bin/bash
python3 /tests/functional/utils/wait_for_backend.py
cd /tests/functional/src/
pytest
