#!/usr/bin/env bash

set -ex

gunicorn --timeout 3000000 -w 2 --bind=0.0.0.0 server:app
