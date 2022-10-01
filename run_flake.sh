#!/bin/sh
flake8 . --exclude .git,.venv,*migrations* --count --show-source --statistics --max-line-length=127

