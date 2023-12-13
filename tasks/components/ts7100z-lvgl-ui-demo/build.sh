#!/bin/bash -e

SOURCE="$DS_WORK/components/ts7100z-lvgl-ui-demo"

cd "$SOURCE"

mkdir build
cd build
cmake .. -DCMAKE_INSTALL_PREFIX="${DS_OVERLAY}/usr" -DCMAKE_C_FLAGS="-L${DS_WORK}/components/lvgl/build/lib -L${DS_WORK}/components/lv_drivers/build/lib -I${DS_WORK}/components/ -I${DS_WORK}/components/lvgl/ -I${DS_WORK}/components/lv_drivers/" -DCMAKE_CXX_FLAGS="-L${DS_WORK}/components/lvgl/build/lib -L${DS_WORK}/components/lv_drivers/build/lib -I${DS_WORK}/components/ -I${DS_WORK}/components/lvgl/ -I${DS_WORK}/components/lv_drivers/" -DCMAKE_TOOLCHAIN_FILE="${CMAKE_CROSS}"
make install
