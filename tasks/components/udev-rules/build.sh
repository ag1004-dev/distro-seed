#!/bin/bash

if [ "${CONFIG_DS_COMPONENT_UDEV_RULES_4900_8390_TOUCH}" == "y" ]; then
	install -d "${DS_OVERLAY}/etc/udev/rules.d/"
	install -m 644 \
		"${DS_TASK_PATH}/files/99-ts4900-8390-resistive-touchscreen.rules" \
		"${DS_OVERLAY}/etc/udev/rules.d/"
fi

if [ "${CONFIG_DS_COMPONENT_UDEV_RULES_4900_8950_TOUCH}" == "y" ]; then
	install -d "${DS_OVERLAY}/etc/udev/rules.d/"
	install -m 644 \
		"${DS_TASK_PATH}/files/99-ts4900-8950-resistive-touchscreen.rules" \
		"${DS_OVERLAY}/etc/udev/rules.d/"
fi

if [ "${CONFIG_DS_COMPONENT_UDEV_RULES_7100_TOUCH}" == "y" ]; then
	install -d "${DS_OVERLAY}/etc/udev/rules.d/"
	install -m 644 "${DS_TASK_PATH}/files/99-ts7100-resistive-touchscreen.rules" \
		"${DS_OVERLAY}/etc/udev/rules.d/"
fi

if [ "${CONFIG_DS_COMPONENT_UDEV_RULES_7990_TOUCH}" == "y" ]; then
	install -d "${DS_OVERLAY}/etc/udev/rules.d/"
	install -m 644 "${DS_TASK_PATH}/files/99-ts7990-resistive-touchscreen.rules" \
		"${DS_OVERLAY}/etc/udev/rules.d/"
fi
