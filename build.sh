#!/bin/bash
pyenv install 3.10.12 -s
pyenv global 3.10.12
pip install -r requirements.txt
gunicorn api/withProba:app