#!/bin/bash -e

ROOT_DST="${DS_OVERLAY}/tmp/"

# Debian distros shipping wpasupplicant 2.10 are:
# Debian 12 (Bookworm)
if [ "${DS_DISTRO}" == "debian" ] ; then
	LIBSSL_DEB="libssl1.1_1.1.1w-0+deb11u1_armhf.deb"
	LIBSSL_SITE="http://ftp.us.debian.org/debian/pool/main/o/openssl/${LIBSSL_DEB}"
	LIBSSL_SHA256="42130c140f972d938d4b4a5ab9638675e6d1223fcff3042bbcc1829e3646eb00"

	WPA_DEB="wpasupplicant_2.9.0-21_armhf.deb"
	WPA_SITE="http://ftp.us.debian.org/debian/pool/main/w/wpa/${WPA_DEB}"
	WPA_SHA256="7bb05cb4f6e3fa3a12d10ea900a4bc7d7d606cacc254115ac28583903b55a2a0"

	HOSTAPD_DEB="hostapd_2.9.0-21_armhf.deb"
	HOSTAPD_SITE="http://ftp.us.debian.org/debian/pool/main/w/wpa/${HOSTAPD_DEB}"
	HOSTAPD_SHA256="e9bd2195d497e420dfda9a77726c5bc9f79315faee5633517912e06154fe59c2"
# Ubuntu distros shipping wpasupplicant 2.10 are:
# 22.04 (Jammy)
# 23.04 (Focal)
elif [ "${DS_DISTRO}" == "ubuntu" ] ; then
	LIBSSL_DEB="libssl1.1_1.1.1f-1ubuntu2_armhf.deb"
	LIBSSL_SITE="http://ports.ubuntu.com/pool/main/o/openssl/${LIBSSL_DEB}"
	LIBSSL_SHA256="fde1628edbebc3b4aba18f2568b703a4c2003e4903c4e01f899b489f4e426d3f"

	WPA_DEB="wpasupplicant_2.9-1ubuntu4.3_armhf.deb"
	WPA_SITE="http://ports.ubuntu.com/pool/main/w/wpa/${WPA_DEB}"
	WPA_SHA256="6d89d49615e903445f0321ddeec6e1d30cbc9fae6fe02cb6aa6f524ae0be969f"

	HOSTAPD_DEB="hostapd_2.9-1ubuntu4_armhf.deb"
	HOSTAPD_SITE="http://ports.ubuntu.com/pool/universe/w/wpa/${HOSTAPD_DEB}"
	HOSTAPD_SHA256="b377567609908ec84a573e9c6bb52935ea15874603644cc068904728f19664f1"
else
	exit 1
fi

install -d "${ROOT_DST}"
common/host/fetch_blob.sh "${LIBSSL_SITE}" "${ROOT_DST}/${LIBSSL_DEB}" "${LIBSSL_SHA256}"
common/host/fetch_blob.sh "${WPA_SITE}" "${ROOT_DST}/${WPA_DEB}" "${WPA_SHA256}"
common/host/fetch_blob.sh "${HOSTAPD_SITE}" "${ROOT_DST}/${HOSTAPD_DEB}" "${HOSTAPD_SHA256}"
