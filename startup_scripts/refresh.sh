#!/bin/bash
#
# Description :
# -------------
# Very specific script executed for refreshing the system

export DISPLAY=:0 &&

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "Stop Paperzoom"
/home/paperzoom/Bureau/PaperZoom/stop.sh

echo "Relaunch Paperzoom"
$DIR/paperzoom_launch.sh
