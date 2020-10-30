import requests
import subprocess
from utilities.configurations import *
from utilities.resources import *


def getImageSharePayload():
    share_id = randomPost(3)
    fields = getFields(share_id)['fields']
    owner = fields['author']
    image_path = fields['resourcePath']

    regJson = \
        {
            "registerUploadRequest": {
                "owner": owner,
                "recipes": [
                    "urn:li:digitalmediaRecipe:feedshare-image"
                ],
                "serviceRelationships": [
                    {
                        "identifier": "urn:li:userGeneratedContent",
                        "relationshipType": "OWNER"
                    }
                ],
            }
        }
    auth_header = getConfig()['API']['auth_header']
    regURL = getConfig()['API']['endpoint'] + APIResources.register
    regInfo = requests.post(url=regURL, params={'action': 'registerUpload'}, json=regJson, headers={'Authorization': auth_header})
    uploadURL = regInfo.json()['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
    asset = regInfo.json()['value']['asset']

    subprocess.run(["curl", "-i", "--upload-file", "" + image_path + "", "-H", "Authorization: " + auth_header + "", "" + uploadURL + ""])
    print('Upload Success')

    json = \
        {
            "author": fields['author'],
            "lifecycleState": fields['lifeCycleState'],
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": fields['shareCommentary']
                    },
                    "shareMediaCategory": fields['shareMediaCategory'],
                    "media": [
                        {
                            "status": fields['mediaStatus'],
                            "description": {
                                "text": fields['mediaDescription']
                            },
                            "media": asset,
                            "title": {
                                "text": fields['title']
                            }
                        }
                    ]
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": fields['visibility']
            }
        }

    body_values = {'json': json, 'shareID': share_id, 'uploadURL': uploadURL, 'asset': asset}
    return body_values



