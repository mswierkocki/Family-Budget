#!/bin/sh
coverage
coverage run manage.py test
coverage report
