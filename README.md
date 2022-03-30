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

* HTTP POST /fs/{path}: creates new dir or file
* HTTP GET /fs/{path}: retrieves info about dir or file
* HTTP HEAD /fs/{path}: verifies if the given path exists
* HTTP DELETE: /fs/{path}: deletes the given path if it's file or empty dir 
