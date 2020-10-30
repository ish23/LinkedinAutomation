import string

from utilities.configurations import *


# print(getPossiblePosts(1))
def getTextSharePayload():
    body_values = getFields(randomPost(1))
    fields = body_values['fields']
    share_id = body_values['primaryKey']
    rl1 = random.choice(string.ascii_letters)
    rl2 = random.choice(string.ascii_letters)
    dup_confuser = '(' + rl1 + rl2 + ')'
    json = {
        "author": fields['author'],
        "lifecycleState": fields['lifeCycleState'],
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": fields['shareCommentary'] + dup_confuser
                },
                "shareMediaCategory": fields['shareMediaCategory']
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": fields['visibility']
        }
    }

    body_values = {'json': json, 'shareID': share_id}
    return body_values



