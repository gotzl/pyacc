#!/bin/bash

usage="Usage: acc_wrapper.sh PROTON_VERSION /path/to/steamapps/ [optional: /path/to/steamapps for proton]"

if [ "$#" -gt 3 -o "$#" -lt 2 ]; then
    echo $usage
    exit 1
fi

ACC_APPID=805550
PROTON_VERSION=$1

STEAMAPPS=$2
PROTONSTEAMAPPS=$2
if [ "$#" -eq 3 ]; then
    PROTONSTEAMAPPS=$3
fi

PROTONPATH="${PROTONSTEAMAPPS}/common/Proton ${PROTON_VERSION}/proton"

export STEAM_COMPAT_DATA_PATH=$STEAMAPPS/compatdata/$ACC_APPID
export WINEPREFIX=$STEAM_COMPAT_DATA_PATH/pfx


if [ ! -d "$STEAMAPPS" -o ! -d "$PROTONSTEAMAPPS" ]; then
    [ -d "$STEAM_COMPAT_DATA_PATH" ] || echo "Unable to find ACC compdata '$STEAM_COMPAT_DATA_PATH'"
    [ -d "$PROTONPATH" ] || echo "Unable to find Proton dir '$PROTONPATH'"
    echo $usage
    exit 1
fi

exec "$PROTONPATH" waitforexitandrun acc_wrapper.exe
