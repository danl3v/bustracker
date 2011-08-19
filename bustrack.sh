!#/bin/bash

/usr/bin/osascript -e 'tell application "Terminal"' -e "tell front window" -e "set the number of rows to 50" -e "set the number of columns to 100" -e "end tell" -e "end tell"

python ~/bustracker/app.py