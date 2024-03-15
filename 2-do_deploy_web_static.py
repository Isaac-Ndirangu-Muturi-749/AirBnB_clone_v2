#!/usr/bin/python3
"""Fabric script that distributes an archive to your web servers and
performs deployment"""

from fabric.api import env, put, run
import os

# Define the hosts and user for Fabric
env.hosts = ['web-01.inm-749.tech', 'web-02.inm-749.tech']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/alxse'


def do_deploy(archive_path):
	"""Distributes an archive to your web servers and performs deployment"""

	# Check if the archive exists
	if not os.path.exists(archive_path):
		return False

	try:
		# Upload the archive to the /tmp/ directory of the web servers
		put(archive_path, '/tmp/')

		# Extract the filename and folder name from the archive path
		archive_name = archive_path.split('/')[-1]
		print('archive_filename: ', archive_name)

		folder_name = archive_name.split('.')[0]
		print('folder_name: ', folder_name)

		# Define the release folder path
		release_folder = '/data/web_static/releases/'
		full_path = release_folder + folder_name
		print('full_path: ', full_path)

		# Create the release folder if it doesn't exist
		run('mkdir -p {}'.format(full_path))

		# Extract the archive contents to the release folder
		# tar: This is the command-line utility for handling tar archives.
		# -x: tells tar to extract files from the archive.
		# -z: tells tar to filter the archive through gzip to decompress it.
		# -f: specifies the name of the archive file.
		# -C specify a directory where the extracted files should be placed
		run('tar -xzf /tmp/{} -C {}'.format(
			archive_name, full_path))

		# Remove the uploaded archive from the /tmp/ directory
		run('rm /tmp/{}'.format(archive_name))

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
		print('New version deployed!')

		return True
	except:
		# Return False if any operation fails
		return False
