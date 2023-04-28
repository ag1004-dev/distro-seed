manifest_config = 'KERNEL_PROVIDER_GIT'
relevant_configs = 'KERNEL_PROVIDER_GIT_URL \
                    KERNEL_PROVIDER_GIT_VERSION \
                    KERNEL_DEFCONFIG \
                    KERNEL_INSTALL_DEVICETREE_FILESYSTEM'
docker_actions = [ '../build.sh' ]
docker_descriptions = [ 'Building Linux Kernel' ]
host_actions = [ 'fetch.sh' ]
host_descriptions = [ 'Fetching Linux Kernel from git' ]
