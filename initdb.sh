#!/bin/bash

# baseurl = "http://127.0.0.1:5000"

rm ./data.db
# python_id = ps | grep python | awk '{ print $1 }' | head -2
# p_ids = python_id.split(" ")
# print(ps | grep python | awk '{ print $1 }' | head -2)

for python_id in $(ps | grep python | awk '{ print $1 }' | head -1); do
  kill -9 $python_id
done



chmod +x app.py
python app.py &

echo hi

chmod +x api.py
python api.py
