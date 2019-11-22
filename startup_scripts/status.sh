#!/bin/bash
#
# Description
# -----------
# Specific script to get status
# Find if app is open
#
# Exit code
# ---------
# Respect code for handleTest :
# 0 : Success
# 1 : No success

# ****************
# IMPORT VARIABLES
# ****************

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Import every config file
setConfig() {
        for f in all*.cfg; do
                getASecureConfigFile.sh $f;
                source $f
        done
}
cd $DIR/../../../../config/ && setConfig;

# *********
# CONSTANTS
# *********

found="false"
programName="python" # useful to search process
programFullName="paperzoom_2016.py_-a" # useful to be sure it's THE process (replace space with _)

# *********
# MAIN CODE
# *********

processes=$(ps aux | grep "$programName" | awk '{print ""$12"_"$13}')

IFS=' '
while read line; do

        #echo "Debug - process : $line and programFullName : $programFullName"

        if [ "$line" == "$programFullName" ]
        then
                found="true"
                break;
        elif [ "$line" != "grep_$programName" ]; then
                found="maybe" # continue to search
        fi

done < <( echo $processes ) # process substitution to avoid subshells

# Handle result
if [ "$found" == "true" ]; then
        exit $STATUS_OK;
elif [ "$found" == "maybe" ]; then
        exit $STATUS_NOK;
else
        exit $STATUS_KO;
fi
