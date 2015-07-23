# final_program
Installation instructions:
    Open Terminal
    	cd ~/GoogleDrive/all_in_one
    	chmod 755 install.command
    Double click install.command in the finder window.
    	A bunch of stuff shoud whiz by on the Terminal screen...

    Everything should be installed...
    	See if MAMP works.
    	Quit MAMP
    	Run the program (by double clicking CRES.command)
    		Everything should work! 
    		Or it won't and you'll see something like "Access Denied"
    			That's not what we want so go back to Terminal..
    				cd ~/GoogleDrive/all_in_one
    				chmod 755 CRES.command
    		Now everything should be running smoothly..?

If MAMP isn't working...

    cd /Applications/MAMP
    ls -al

    You should see something like this:

        drwxrwxr-x  40 *** admin 1360 Nov  4  2014 conf
        lrwxr-xr-x   1 *** admin   50 Jul 19 19:02 db -> /Users/***/GoogleDrive/all_in_one/MAMP_db
        drwxr-xr-x   6 *** admin  204 Jun  2 15:12 db_test
        drwxrwxr-x  31 *** admin 1054 Oct 20  2014 fcgi-bin

If MAMP isn't working it's probably because db is POINTING to the wrong file (it's a link so when something looks for the contents of db in /Applications/MAMP, the link POINTS to another path/physical memory location). Essentially, I think there's a space in your db --> PATH ..Google Drive/ should be GoogleDrive. 

Running changeMAMP_db.sh will take care of the problem but you have to set the permissions first. 
    cd ~/GoogleDrive/all_in_one
    chmod 755 changeMAMP_db.sh 
    ./changeMAMP_db.sh 

To do it manually, 
    # Navigte to MAMP
        cd /Applications/MAMP
    # Delete the old link; do it recursively and don't ask for permission (rf)
        rm -rf 
    # Make sure you have the correct PATH for the link.
        find ~/G*/all_in_one -iname MAMP_db
    # Make a new (symbolic) link FROM TO
        ln -s WHAT/YOU/GOT db

    # Mine looks like:
        # Mine looks like 
            ln -s /Users/***/GoogleDrive/all_in_one/MAMP_db db

If everything is in the right spot you should be able to type

    cd db
    ls

There should only be three files ( mysql, sqlite, mongodb ) and an ICON?. 

Try MAMP... 



    
