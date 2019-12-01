import oneDriveUpload
import json
import sys

# read the parameters.json
config = json.load(open(sys.argv[1]))
# get a token and store it in a session
token = getToken(config)
session = requests.Session()
session.headers.update({'Authorization': 'Bearer ' + token})

# and upload the file to OneDrive
uploadFile(session, "test.txt", config["driveId"])