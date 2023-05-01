manifest_config = 'JOURNAL_SIZE_OVERRIDE'
relevant_configs = 'JOURNAL_DISABLE_LOGS \
                    JOURNAL_SIZE_VALUE'
chroot_script_actions = [ 'set-logsize.sh' ]
chroot_script_descriptions = [ 'Setting Journal Size' ]
