This is a simple (large) file upload Python 3 script against the Microsoft Graph API. It uses the special api for large files where it's uploading the file in chunks. This is tested against the OneDrive api which is identical to the SharePoint API.

## Installation
Prerequisite: make sure you use Python 3
Install the required packages:
```
pip install -r requirements.txt
```

## Usage
* Create the parameters.json with your own values
** tenant id / drive id: https://docs.microsoft.com/en-us/onedrive/developer/rest-api/
** client id / secret: https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps/ApplicationsListBlade
* Put the parameters.json, oneDriveUpload.py and your Python file (see [example.py](https://github.com/MaxxtonGroup/oneDriveUploader/blob/master/example.py)
* Execute:
```
python3 example.py
```

Tip: use the [Graph Explorer](https://developer.microsoft.com/en-us/graph/graph-explorer) to get above info and play around with the API.

## Possible improvements
* Check for existing files and / or support overriding
* Better error handling and resuming uploads

## Disclaimer
This script is a gathering of all kind of examples found on the internet. Since none of them was simple to use, we combined this into one simple script and put it online under the MIT license. In case you want to be mentioned, get in touch.
