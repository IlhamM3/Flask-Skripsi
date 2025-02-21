#!/bin/bash

# pyenv install 3.10.12 -s
# pyenv global 3.10.12

# Install dependencies
pip install -r requirements.txt

# Jalankan aplikasi dengan Gunicorn
exec gunicorn api/withProba:app
