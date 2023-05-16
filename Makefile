all:
	@common/build.py

dry-run:
	@common/build.py --dry-run

%_defconfig:
	@common/lib/kconfiglib/defconfig.py --kconfig Kconfig configs/$@

menuconfig:
	@common/lib/kconfiglib/menuconfig.py

docker-shell:
	@common/utils/docker-shell.py

chroot-shell:
	@common/utils/chroot-shell.py

checkdeps:
	@common/utils/check.py

plotdeps:
	@common/build.py --plot-deps

clean:
	-@common/utils/clean-work.py

clean-cache:
	@common/utils/clean-cache.py

clean-all:
	-@rm -rf dl/
	-@common/utils/clean-cache.py
	-@common/utils/clean-work.py
