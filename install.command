#!/bin/sh
if [[ -d /envs ]]; then
	cd /envs
	echo "Envs exists!"
else
	cd /
	mkdir envs
	cd envs
fi
# This makes it so you can have the GDrive folder called anything
req_file=$(find ~/G* -iname CRES_requirements.txt)

if [[ -d /envs/CRES ]]; then
	echo "Virtualenv CRES is in place. Now check if it's up to date."
	source /envs/CRES/bin/activate
	pip install -r $req_file
else
	echo "There was no virtualenv for some reason. Let's make one..."
	cd /envs
	virtualenv CRES
	source /envs/CRES/bin/activate
	pip install -r $req_file
fi

chmod 771 ~/GoogleDrive/all_in_one/CRES.command
