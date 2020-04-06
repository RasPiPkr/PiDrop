'''
Thank you for downloading PiDrop, I hope you find this software useful.

Change the value below to keep a backup of pidrop_log.csv file in your
dropbox account which will be kept in the root folder /.

The pidrop_log.csv file will automatically be saved locally in this folder
on your computer.

The file will only be updated when you run this program and connection is
made to save wasting commnuication with the api per action.

*** Do not delete the pidrop_log.csv file from the folder of this program
pidrop.py as this is for you and ONLY you to keep track of.

LOGGING OF DATA:
Time and date stamp for the following:

Creation of folders,
Uploaded file - file path of file uploaded and file path on dropbox,
Download file - file path from dropbox and file path saved to locally,
Deletion of files or folders upon confirmation from user.

Thanks again.
Martin Parker.
'''

# True = backup the log file in dropbox OR False = log file local only.
log_backup = True

# Enter your Dropbox Python API token provided when you setup your account as a developer.
acc_token = '' # Put your token in between the ''

''' Setup a Dropbox account whilst in the main screen of your account you will see 3x dots 
near bottom right of the page click on that to popup a list and select developer. Select 
Python for the API and then click generate token. Copy that and paste it inbetween the '' above 
here and then save this file.
'''
