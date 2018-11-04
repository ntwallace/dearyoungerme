#!bin/bash

# start ngrok if not running
if [ “$(ps -ef | grep -v grep | grep ngrok | wc -l)” -le 0 ]
then
 ./ngrok http 5000
 echo "Ngrok started, update SMS HTTP POST api"
else
 echo "Ngrok already running"

 # start python script if not running
 if [ “$(ps -ef | grep -v grep | grep popup | wc -l)” -le 0 ]
 then
  python3 popup.py
  echo "Python script started"
 else
  echo "Python script already running"

fi
