#!/bin/bash

pipenv run gunicorn -w 4 -b 127.0.0.1:4000 biggerbot:app
