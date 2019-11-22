#!/bin/sh

sleep 10

# 1. Start Test script
#cd /home/paperzoom/Bureau/PaperZoom
echo "Script de test. Kinect OK ?"
python testKinect01.py &
sleep 5

# 2. Kill old instances (and test script)
killall python &
sleep 1

# 3. Launch the real app
echo "Démarrage Paper zoom."
python paperzoom.py -a &
# 3.b Do a keyboard shortcut to switch on scenario
echo "Changement de scenario dans 5 sec."
sleep 5
xdotool key 2



