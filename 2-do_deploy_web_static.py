#!/usr/bin/env python3
"""Fabric script that distributes an archive to your web servers and
performs deployment"""

from fabric.api import env, put, run
from os.path import exists

# Define the hosts and user for Fabric
env.hosts = ['35.153.193.23', '54.146.94.67']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/alxse'


def do_deploy(archive_path):
    """Distributes an archive to your web servers and performs deployment"""

    # Check if the archive exists
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web servers
        put(archive_path, '/tmp/')

        # Extract the filename and folder name from the archive path
        archive_filename = archive_path.split('/')[-1]
        print('archive_filename: ', archive_filename)

        folder_name = archive_filename.split('.')[0]
        print('folder_name: ', folder_name)

        # Define the release folder path
        release_folder = '/data/web_static/releases/'
        full_path = release_folder + folder_name
        print('full_path: ', full_path)

        # Create the release folder if it doesn't exist
        run('mkdir -p {}'.format(full_path))

        # Extract the archive contents to the release folder
        run('tar -xzf /tmp/{} -C {}'.format(
            archive_filename, full_path))

        # Remove the uploaded archive from the /tmp/ directory
        run('rm /tmp/{}'.format(archive_filename))

        # Move the contents of the extracted folder to the release folder
        run('mv {}/web_static/* {}'.format(
            full_path, full_path))

        # Remove the web_static folder within the release folder
        run('rm -rf {}/web_static'.format(full_path))

        # Remove the current symbolic link
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link to the latest release folder
        run('ln -s {} /data/web_static/current'.format(
            full_path))

        # Return True if all operations have been completed successfully
        return True
    except:
        # Return False if any operation fails
        return False
