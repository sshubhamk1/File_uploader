#!/bin/bash
echo "Hello"
export FLASK_APP="./webapp" 
export FLASK_ENV="development" 
export FLASK_RUN_PORT=8000 
export FLASK_RUN_HOST="0.0.0.0"
#flask run --host="0.0.0.0" --port=80 
flask run 
