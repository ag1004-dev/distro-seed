import os

# Define a function to load the manifest from a file
def load_manifest(manifest_path):
    with open(manifest_path, 'r') as f:
        manifest_data = f.read()
        # Parse the manifest data into a dictionary or other data structure
        # that represents the information you want to extract
        manifest = {
            'manifest_config': None,
            'docker_actions': None,
            'docker_descriptions': None,
            'host_actions': None,
            'host_descriptions': None,
            'chroot_script_actions': None,
            'chroot_script_descriptions': None,
            'chroot_cmd_actions': None,
            'chroot_cmd_descriptions': None,
        }
        exec(manifest_data, {}, manifest)
        manifest['path'] = os.path.dirname(manifest_path)
        
        return manifest
