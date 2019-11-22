#!/bin/bash
#
# Description :
# -------------
# Simulate user to launch app
# We do this trick because I couldn't launch pyton in a subprocess
# without no waiting the end of it..

# 2019:11:23 Sébastien Albert (Updates) : redémarrage 2019

# 0. Init param
export DISPLAY=:0 &&
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 1. Launch gnome terminal
gnome-terminal &&


# 2. Wait for terminal to be opened and focus
echo "Wait Terminal"
sleep 30
xdotool windowfocus Terminal

# 3. Simulate user to launch process bash /home/paperzoom/Bureau/lienpaperzoom/start_app.sh
xdotool key slash h o m e slash p a p e r z o o m slash B u r e a u slash
xdotool key l i e n p a p e r z o o m slash s t a r t underscore a p p period s h Return
