#!/bin/bash

# baseurl = "http://127.0.0.1:5000"

chmod +x app.py
python app.py &

chmod +x api.py
python api.py
