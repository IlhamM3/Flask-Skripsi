#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Jalankan gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 api.withProba:app
