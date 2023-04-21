#!/bin/bash

flask db upgrade
flask translate compile
exec gunicorn -b :5000 --access-logfil - --error-logfile - flasky:app