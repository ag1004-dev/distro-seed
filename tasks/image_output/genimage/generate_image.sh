#!/bin/bash -e

GENIMAGE="$DS_WORK/components/host-genimage/genimage"
OUTPUT="$DS_WORK/output"

export GENIMAGE_CONFIG="$CONFIG_DS_GENIMAGE_PATH"
export GENIMAGE_INPUTPATH="$OUTPUT"
export GENIMAGE_OUTPUTPATH="$OUTPUT"
export GENIMAGE_TMPPATH="$DS_WORK/genimage-tmp/"

$GENIMAGE
