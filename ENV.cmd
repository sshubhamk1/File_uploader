@echo off
set FLASK_APP=webapp
set FLASK_ENV=development

python3 -m flask run --host=0.0.0.0 --port 80 