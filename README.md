# PiDrop
A tkinter GUI file transfer to and from Dropbox using the Python API.

This saves logging in through the Dropbox website to save time and you remembering your logging in details.

FIRST OF ALL:

install dropbox so in terminal enter: sudo pip3 install dropbox
this should be the only thing you'll need to install as everything else should be on your Raspbian.

then....

Setup a Dropbox account and whilst in the main screen of your account you will see 3x dots near bottom right of the page
click on that to popup a list and select developer. Select Python for the API and then click 
generate token. Copy that and paste it inbetween the '' next to acc_token, then save this file.
You can then run the pidrop.py script to use it.

python3 ./pidrop.py

A log file is kept locally on your computer but it can be backed up on the Dropbox account, this can be turned off so only local saving.

LOGGING OF DATA:
Time and date stamp for the following:

Creation of folders,
Uploaded file - file path of file uploaded and file path on dropbox,
Download file - file path from dropbox and file path saved to locally,
Deletion of files or folders upon confirmation from user.

Many thanks
Martin Parker.
