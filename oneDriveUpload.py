"""
Requires some installed modules:
pip3 install "msal>=0,<2"
pip3 install "requests>=2,<3"

The configuration file would look like this:
{
  "authority": "https://login.microsoftonline.com/YOUR_TENANT_ID / SITE ID",
  "client_id": "CLIENT_ID",
  "scope": [ "https://graph.microsoft.com/.default" ],
  "secret": "CLIENT_SECRET",
  "driveId": "YOUR_DRIVE_ID"
}

You can then run this with a JSON configuration file:
    python3 example.py
"""

import sys
import json
import logging
import os
import requests
import msal

def getToken(config):
    app = msal.ConfidentialClientApplication(
            config["client_id"], authority=config["authority"],
            client_credential=config["secret"]
        )
    result = None
    result = app.acquire_token_silent(config["scope"], account=None)

    if not result:
        logging.info("No suitable token exists in cache. Let's get a new one from AAD.")
        result = app.acquire_token_for_client(scopes=config["scope"])

    if "access_token" in result:
        return result['access_token']
    else:
        print(result.get("error"))
        print(result.get("error_description"))
        print(result.get("correlation_id"))
# end getToken

def uploadFile(session, filename, driveId, folder=None):
    # Upload a file to Sharepoint
    fnameOnly = os.path.basename(filename)

    # create the Graph endpoint to be used
    if folder is not None:
        endpoint = f'https://graph.microsoft.com/v1.0/drives/{driveId}/root:/{folder}/{fnameOnly}:/createUploadSession'
    else:
        endpoint = f'https://graph.microsoft.com/v1.0/drives/{driveId}/root:/{fnameOnly}:/createUploadSession'
    jsonResponse = session.put(endpoint).json()
    uploadUrl = jsonResponse["uploadUrl"]

    # upload in chunks
    filesize = os.path.getsize(filename)
    with open(filename, 'rb') as fhandle:
        startByte = 0
        while True:
            fileContent = fhandle.read(10*1024*1024)
            dataLength = len(fileContent)
            if dataLength <= 0:
                break

            endByte = startByte + dataLength - 1
            crange = "bytes "+str(startByte)+"-"+str(endByte)+"/"+str(filesize)
            print(crange)
            chunkResponse = session.put(uploadUrl, headers={"Content-Length": str(dataLength),"Content-Range": crange}, data=fileContent)
            if not chunkResponse.ok:
                # something went wrong
                print(f'<Response [{chunkResponse.status_code}]>')
                pprint.pprint(chunkResponse.json())
                break

            startByte = endByte + 1
    return chunkResponse
# end uploadFile
