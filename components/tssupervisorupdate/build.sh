#!/bin/bash -e

SOURCE="$DS_WORK/components/tssupervisorupdate/"
INSTALL="$DS_WORK/deploy/80-tssupervisorupdate/"

cd "$SOURCE"

meson setup --cross-file "$MESON_CROSS" builddir
cd builddir
meson compile
DESTDIR="$INSTALL" meson install
