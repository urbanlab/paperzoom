#!/bin/bash
#
# Description :
# -------------
# Very specific script executed at the launch of the system
# 2019:11:23 Sébastien Albert (Updates) : Changement de chemins, suppression etape 3

# 0. Init paramaters
export DISPLAY=:0
source ~/.bash_profile

# 1. Handle innoportune screensaver
config_screensaver.sh &&

# 2. Launch program
echo -e "Start Paperzoom -> \n"
cd /home/paperzoom/Bureau/PaperZoom
#(python paperzoom_2016.py -a &)
(/home/paperzoom/Bureau/PaperZoom/start.sh &) &&

# 3. scenario Change
# Obsolete depuis l'ajout de l'affichage d'un script de test
# C'est start.sh qui lance le scenario
#echo -e "Wait 10s before changing scenario -> \c"
#sleep 10 &&
#xdotool key 3

# 4. End
echo -e "Launch end"

