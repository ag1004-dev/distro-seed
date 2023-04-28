manifest_config = 'IMAGE_ROOTFS_TAR'
relevant_configs = 'IMAGE_ROOTFS_TAR_NONE \
                    IMAGE_ROOTFS_TAR_XZ \
                    IMAGE_ROOTFS_TAR_BZIP2'
docker_actions = [ 'package-tar.sh' ]
docker_descriptions = [ 'Packaging up output tar' ]
