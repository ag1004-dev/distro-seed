all:
	@common/build.py

%_defconfig:
	@common/lib/kconfiglib/defconfig.py --kconfig Kconfig configs/$@

menuconfig:
	@common/lib/kconfiglib/menuconfig.py

docker-shell:
	@common/docker-shell.py

chroot-shell:
	@common/chroot-shell.py

checkdeps:
	@common/check.py

clean:
	-@common/clean-work.py

clean-cache:
	@common/clean-cache.py

clean-all:
	-@rm -rf dl/
	-@common/clean-cache.py
	-@common/clean-work.py
