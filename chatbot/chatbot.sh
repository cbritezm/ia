#!/bin/bash
source /root/venv/bin/activate
cd /root/cbritezm/git/ia/chatbot
gunicorn --workers 3 --bind 127.0.0.1:8000 app:app
