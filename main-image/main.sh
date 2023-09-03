#!/bin/bash
python flaskdb.py db init
python flaskdb.py db migrate
python flaskdb.py db upgrade
python -m ptvsd --port 3000 --host 0.0.0.0 run.py