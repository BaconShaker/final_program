#!/bin/sh
# First, let's change all the permissions in all_in_one.

# *.py files
find ~/GoogleDrive/all_in_one -iname "*.py" -print0 | while IFS= read -r -d $'\0' line; do
    chmod 755 $line
    echo "$line has been made executable." 
done

# *.sh files
find ~/GoogleDrive/all_in_one -iname "*.sh" -print0 | while IFS= read -r -d $'\0' line; do
    chmod 755 $line
    echo "$line has been made executable." 
done


if [[ -d /envs ]]; then
	cd /envs
	echo "Envs exists!"
else
	cd /
	sudo mkdir envs
	cd envs
fi
# This makes it so you can have the GDrive folder called anything
req_file=$(find ~/G* -iname CRES_requirements.txt)

if [[ -d /envs/CRES/bin ]]; then
	echo "Virtualenv CRES is in place. Now check if it's up to date."
	source /envs/CRES/bin/activate
	pip install -r $req_file
else
	echo "There was no virtualenv for some reason. Let's make one..."
	cd /envs
	sudo virtualenv CRES
	source /envs/CRES/bin/activate
	pip install -r $req_file
fi

mamp=$(find ~/G*/all_in_one -iname MAMP_db)
link=$(find /Applications/MAMP -lname '*MAMP_db')
if [[  $link = /Applications/MAMP/db ]]; then
	echo "Your SQL link is correct, it links $link --> $mamp"
else
	echo "Your link to SQL was either broken or didn't exist. Let's do something about it shall we?"
	cd /Applications/MAMP
	rm -rf db
	ln -s $mamp db
	echo "Now your link correctly points $link --> $mamp"
fi


chmod 771 ~/GoogleDrive/all_in_one/CRES.command
