#!/bin/bash
screen_name="web"
screen -dmS $screen_name
screen -x -S $screen_name -p 0 -X stuff "python ./main.py"
screen -x -S $screen_name -p 0 -X stuff "\n"