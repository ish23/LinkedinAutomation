from utilities.configurations import *
import random
import string

# print(getPossiblePosts(2))
def getArticleSharePayload():
    body_values = getFields(randomPost(2))
    fields = body_values['fields']
    share_id = body_values['primaryKey']
    rl1 = random.choice(string.ascii_letters)
    rl2 = random.choice(string.ascii_letters)
    dup_confuser = '('+rl1+rl2+')'
    json = {
        "author": fields['author'],
        "lifecycleState": fields['lifeCycleState'],
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": fields['shareCommentary'] + dup_confuser
                },
                "shareMediaCategory": fields['shareMediaCategory'],
                "media": [
                    {
                        "status": fields['mediaStatus'],
                        "description": {
                            "text": fields['mediaDescription']
                        },
                        "originalUrl": fields['originalURL'],
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


    body_values = {'json': json, 'shareID': share_id}
    return body_values


