from tkinter import messagebox
from tkinter import filedialog
import tkinter as tk
from pidrop_settings import acc_token, log_backup
import dropbox, time, csv, os


def checkDBox(): # Check what files and folders in dropbox account
    try:
        statusText.set('Collecting\nall files in\nyour account.')
        status.config(bg='white')
        root.update()
        files.clear()
        posFolders.clear()
        infoArea.delete(0, 'end')
        for entry in dBox.files_list_folder('').entries:
            filename, file_extension = os.path.splitext(entry.name)
            if len(file_extension) == 0:
                posFolders.append('/' + entry.name) # No extension so possible folder'/' + 
            else:
                files.append('/' + entry.name)
        files.append('/')
        for folder in posFolders: # Now iterating through the possible folders
            files.append(folder)
            for entry in dBox.files_list_folder(folder).entries:
                files.append(folder + '/' + entry.name)
        for file in files: # Populate the infoArea listbox
            infoArea.insert(0, file)
        statusText.set('Dropbox\nfiles\ncollected.')
        status.config(bg='yellow')
    except:
        statusText.set('Failed\nto get\nfiles.')
        status.config(bg='red')

def downFile():
    try:
        selected = ''
        if len(files) >= 1:
            selected = infoArea.get(infoArea.curselection())
            if len(selected) != 0:
                filename = selected.split('/')
                save_as = filedialog.asksaveasfile(parent=root, initialdir='/home/pi/',
                                                   initialfile=filename[-1], 
                                                   title = 'Dropbox download.',
                                                   filetypes=(('all files','*.*'),))
                if not save_as:
                    messagebox.showinfo('Information', 'User cancelled download.')
                else:
                    statusText.set('Download\nstarted.')
                    status.config(bg='yellow')
                    root.update()
                    with open(save_as.name, 'wb') as f:
                        metadata, res = dBox.files_download(path=selected)
                        f.write(res.content)
                    statusText.set('Download\ncomplete\n& saved.')
                    status.config(bg='green')
                    write_data_file('Download', selected + ' -> ' + save_as.name)
        else:
            statusText.set('Nothing to\ndownload.')
            status.config(bg='red')
    except:
        statusText.set('Select a\nfile and\ntry again.')
        status.config(bg='red')

def upFile():
    try:
        selected = infoArea.get(infoArea.curselection())
        if len(selected) != 0:
            upload_as = filedialog.askopenfile(parent=root, initialdir='/home/pi/',
                                               title = 'Upload Dropbox.',
                                               filetypes=(('all files','*.*'),))
            if not upload_as:
                messagebox.showinfo('Information', 'No file specified, cancelled.')
            else:
                filename = upload_as.name.split('/')
                statusText.set('Upload\nstarted.')
                status.config(bg='yellow')
                root.update()
                file = open(upload_as.name, 'rb').read()
                if selected == '/':
                    dBox.files_upload(file, '/' + filename[-1])
                else:
                    dBox.files_upload(file, selected+'/'+filename[-1])
                statusText.set('Upload\ncompleted.')
                status.config(bg='green')
                write_data_file('Upload', upload_as.name + ' -> ' + selected)
                root.after(1000, checkDBox)
        else:
            statusText.set('Select a\ndropbox\ndirectory,\ntry again.')
            status.config(bg='red')
    except:
        statusText.set('Upload\nfailed.')

def makeDir():
    try:
        temp = newDir.get()
        filename, file_extension = os.path.splitext(temp)
        if len(file_extension) >= 1:
            statusText.set('Only create\nfolders.')
            status.config(bg='red')
        else:
            if temp[0] != '/': # to remove if not entered at beginning.
                temp = '/' + temp
            if temp[-1] == '/': # to remove if entered at end.
                temp = temp[:-1]
            dBox.files_create_folder(temp)
            statusText.set('Folder\nCreated.')
            status.config(bg='green')
            write_data_file('New Folder', temp)
            newDir.set('')
            root.after(1000, checkDBox)
    except:
        statusText.set('Folder\nalready\nexists\nor not valid\entry.')
        status.config(bg='red')
        write_data_file('New Folder', temp + ' failed creation')

def delItem():
    try:
        selected = infoArea.get(infoArea.curselection())
        if len(selected) != 0:
            filename, file_extension = os.path.splitext(selected)
            if len(file_extension) >= 1:
                statusText.set('Confirm\nDeletion.')
                status.config(bg='white')
                root.update()
                confirm = messagebox.askquestion(title='!!! WARNING !!!',
                                             message='Are you sure you want to delete the file {}?'.format(selected))

            else:
                confirm = messagebox.askquestion(title='!!! WARNING !!!',
                                                 message='Are you sure you want to delete the folder {}, all files in the folder will be deleted!'.format(selected))
            if confirm == 'yes':
                dBox.files_delete(selected)
                statusText.set('Deleted.')
                status.config(bg='yellow')
                write_data_file('Deletion', selected + ' = User Confirmed')
                root.update()
                root.after(1000, checkDBox)
            else:
                statusText.set('Deletion\nCancelled.')
                status.config(bg='white')
                write_data_file('Deletion', selected + ' = User Cancelled')
                root.update()
        else:
            statusText.set('Select a\file or\ndirectory,\ntry again.')
            status.config(bg='red')
    except:
        statusText.set('Deletion\nfailed.')

def do_log_backup():
    try:
        dBox.files_delete('/pidrop_log.csv')
        file = open('pidrop_log.csv', 'rb').read()
        dBox.files_upload(file, '/pidrop_log.csv')
        write_data_file('Backup pidrop_log', 'Completed')
    except:
        statusText.set('Backup of\npidrop_log.csv\nfile missing or\ncheck settings.')
        status.config(bg='yellow')

def write_data_file(action, withFile):
    try:
        logTime = time.strftime('%Y/%m/%d_%H:%M:%S')
        with open('pidrop_log.csv', 'a+', newline='') as dBoxlog:
            data = csv.writer(dBoxlog)
            data.writerow([logTime, action, withFile])
    except:
        messagebox.showinfo('!!! Warning !!!', 'Error, unable to write data.')

menuWidth = 200
files = []
posFolders = []
root = tk.Tk()
root.title('PiDrop - Simple File Transfer Client for Dropbox')
root.geometry('600x400+0+0')
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=10)

# Main frames left and right.
menuFrame = tk.Frame(root, width=menuWidth, bg='grey')
menuFrame.pack(side='left', fill='y')
fileFrame = tk.Frame(root, bg='grey')
fileFrame.pack(side='right', fill='both', expand=True)

# Left side menu items
checkBtn = tk.Button(menuFrame, text='Check\nDropBox', bg='yellow',
                     command=checkDBox, width=10, height=3)
checkBtn.pack(padx=5, pady=5)
uploadBtn = tk.Button(menuFrame, text='Upload\nFiles', bg='blue',
                      command=upFile, width=10, height=3)
uploadBtn.pack(padx=5)
downBtn = tk.Button(menuFrame, text='Download\nFiles', bg='blue',
                    command=downFile, width=10, height=3)
downBtn.pack(padx=5, pady=5)
delBtn = tk.Button(menuFrame, text='Delete', bg='red', width=10, command=delItem)
delBtn.pack(padx=5, pady=5)
statusText = tk.StringVar()
status = tk.Label(menuFrame, textvariable=statusText, bg='white')
status.pack(padx=5, pady=5, fill='both', expand=True)

# Right side frames
dirFrame = tk.Frame(fileFrame, height=3)
dirFrame.pack(padx=5, pady=5, fill='x')
listFrame = tk.Frame(fileFrame, bg='grey')
listFrame.pack(anchor='s', padx=5, pady=5, fill='both', expand=True)

# Right top frame items
how2use = tk.Label(dirFrame, text='USAGE: Click check dropbox to get a fresh list of files.\nUPLOAD: Click to highlight the directory in dropbox list, click upload.\nDOWNLOAD: click to highlight the file in dropbos list, click download.\nDELETE: click to highlight the file or folder in the list, click delete.')
how2use.grid(row=0, columnspan=3)
dirBtn = tk.Button(dirFrame, text='Create\ndirectory:', bg='yellow', width=10, command=makeDir)
dirBtn.grid(row=1, column=0, padx=5, pady=5)
newDir = tk.StringVar()
dirName = tk.Entry(dirFrame, textvariable=newDir, width=21)
dirName.grid(row=1, column=1, padx=5, sticky='ew')

# Right bottom frame items
scrollbar1 = tk.Scrollbar(listFrame)
infoArea = tk.Listbox(listFrame, listvariable=files, yscrollcommand=scrollbar1.set, bg='white')
infoArea.pack(side='left', fill='both', expand=True)
scrollbar1.pack(side='left', fill='y')
scrollbar1.config(command=infoArea.yview)

try:
    dBox = dropbox.Dropbox(acc_token)
    statusText.set('Dropbox\nconnected.')
    write_data_file('API Connection', 'OK')
    if log_backup == True:
        do_log_backup()
except TypeError:
    statusText.set('Dropbox\nfailed.\n\nCheck\nToken.')
    write_data_file('API Connection', 'FAILED')
root.mainloop()




