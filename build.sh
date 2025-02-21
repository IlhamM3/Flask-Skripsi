#!/bin/bash

# Pastikan menggunakan Python 3.10 jika tersedia
if command -v pyenv 1>/dev/null 2>&1; then
    pyenv install 3.10.12 -s
    pyenv global 3.10.12
fi

# Install dependencies
pip install -r requirements.txt

# Jalankan aplikasi dengan Gunicorn
exec gunicorn api/withProba:app
