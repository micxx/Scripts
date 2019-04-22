# GoogleDrive
Use Google Drive with CLI.  

## How to use

1. Get Python3 and install google-api-python-client, PyDrive    
    $ pip install google-api-python-client PyDrive  

2. Get JSON file from <https://console.developers.google.com/> and save as "client_secret.json"

3. Set Google Drive API enable


## Command

#### up[upload] file_path1 (file_path2 ...)  
Upload files.  

#### dl[download] file_id1 (file_id2 ...)  
Download files.  

#### rm[remove,delete] file_id1 (file_id2 ...)  
Remove to trash box.  

#### cd file_id  
Change directory.  

#### ls[dir]  
Show files in current directory.  
[id] filename  
.  
..  
...  

#### exit[quit]  
Exit
