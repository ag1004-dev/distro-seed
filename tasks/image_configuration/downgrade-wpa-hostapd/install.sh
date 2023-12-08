#!/bin/bash -e

ROOT_DST="/tmp/"


if [ "${DS_DISTRO}" == "debian" ]; then
	LIBSSL_DEB="libssl1.1_1.1.1w-0+deb11u1_armhf.deb"
	WPA_DEB="wpasupplicant_2.9.0-21_armhf.deb"
	HOSTAPD_DEB="hostapd_2.9.0-21_armhf.deb"
elif [ "${DS_DISTRO}" == "ubuntu" ] ; then
	LIBSSL_DEB="libssl1.1_1.1.1f-1ubuntu2_armhf.deb"
	WPA_DEB="wpasupplicant_2.9-1ubuntu4.3_armhf.deb"
	HOSTAPD_DEB="hostapd_2.9-1ubuntu4_armhf.deb"
else
	exit 1
fi

# Don't do anything if wpasupplicant is not installed
# Don't fail if wpasupplicant is not installed
set +e
dpkg -l |grep wpasupplicant >/dev/null 2>&1
RES="${?}"
set -e
if [ "${RES}" -eq 0 ] ; then
	# Remove both wpa_supplicant and hostapd if its installed
	apt-get remove -y wpasupplicant

	# Don't fail if hostapd is not installed
	set +e
	dpkg -l |grep hostapd >/dev/null 2>&1
	RES="${?}"
	set -e
	if [ "${RES}" -eq 0 ] ; then
		apt-get remove -y hostapd
	fi
	dpkg -i "${ROOT_DST}/${LIBSSL_DEB}"
	dpkg -i "${ROOT_DST}/${WPA_DEB}"
	# Note that, this always installs hostapd simply because it is also
	# affected by the same issue as wpa_supplicant. If the end user is
	# going to install one, they may end up installing the other and that
	# could cause a lot of strange issues.
	dpkg -i "${ROOT_DST}/${HOSTAPD_DEB}"
	systemctl disable hostapd

	apt-mark hold libssl1.1
	apt-mark hold wpasupplicant
	apt-mark hold hostapd

	rm -r "${ROOT_DST}"
fi
