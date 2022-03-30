# In-memory File-system Problem

This is an implementation of an in-memory file-system + Web Service.

> Problem asked during interviews with Coinbase

# Setup

pip install -r requirements.txt

# Framework

* mkdir: creates dir
* write_file: creates file
* read_file: read contents

# API

Run ws.py and go to `localhost:8000/docs`

<img width="1459" alt="Screen Shot 2022-03-29 at 9 33 50 PM" src="https://user-images.githubusercontent.com/131457/160752045-64b5fab7-1c68-48ed-882f-9c072cd2a3c7.png">

## HTTP POST /fs/{path}

> creates new dir or file

## HTTP GET /fs/{path}

> retrieves info about dir or file

## HTTP HEAD /fs/{path}

> verifies if the given path exists

## HTTP DELETE: /fs/{path}

> deletes the given path if it's file or empty dir

