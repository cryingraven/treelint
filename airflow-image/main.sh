#!/bin/bash
airflow scheduler -D &
airflow webserver -D -p 8080 &
python run.py