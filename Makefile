all:
	common/build.py

%_defconfig:
	common/kconfiglib/defconfig.py --kconfig Kconfig configs/$@

menuconfig:
	common/kconfiglib/menuconfig.py

docker-shell:
	common/docker-shell.py

chroot-shell:
	common/chroot-shell.py

check:
	common/check.py

clean:
