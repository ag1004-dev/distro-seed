#!/bin/bash -e

SOURCE="$DS_WORK/components/lv_drivers"

cd "$SOURCE"

mkdir build
cd build
cmake .. -DCMAKE_INSTALL_PREFIX="${DS_OVERLAY}/usr" -DCMAKE_C_FLAGS="-L${DS_WORK}/components/lvgl/build/lib -I${DS_WORK}/components/ -I${DS_WORK}/components/lvgl/" -DCMAKE_CXX_FLAGS="-L${DS_WORK}/components/lvgl/build/lib -I${DS_WORK}/components/ -I${DS_WORK}/components/lvgl/" -DBUILD_SHARED_LIBS=TRUE -DCMAKE_TOOLCHAIN_FILE="${CMAKE_CROSS}"
make install
