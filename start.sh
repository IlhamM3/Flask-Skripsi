#!/bin/bash
pip install -r requirements.txt
gunicorn api.withProba:app
