#!/usr/bin/env bash

NOW="$(date +'%Y%m%d_%H%M%S')"
ING_RESOURCE_DIR="${1}"
ING_YEAR="${2:-2023}"
ING_DATA_TARGET_PREFIX="${3:-$NOW}"

if [ ! -d "$ING_RESOURCE_DIR" ] ; then
    echo "Bad resources directory $ING_RESOURCE_DIR"
    exit 1
fi

BASE_DATA_DIR="./data"

if [ ! -d "$BASE_DATA_DIR" ] ; then
    echo "Bad data directory $BASE_DATA_DIR"
    exit 1
fi

# add data
ING_DATA_IDENT="${ING_DATA_TARGET_PREFIX}_for_${ING_YEAR}"
ING_DATA="$BASE_DATA_DIR/$ING_DATA_IDENT"
mkdir -p "$ING_DATA"
cp -t "$ING_DATA" $ING_RESOURCE_DIR/Girokonto_*_Kontoauszug_{$ING_YEAR*,$((ING_YEAR+1))01*}.pdf

# run converter
mkdir -p output
poetry run python3 main.py $ING_DATA/*.pdf > "output/$ING_DATA_IDENT.csv"
