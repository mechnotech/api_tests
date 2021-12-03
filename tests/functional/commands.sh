#!/bin/bash
cd tests
cd functional
python3 wait_for_backend.py
pytest

