from part2.getTextPayload import *
from part2.getArticlePayload import *
from part2.getImagePayload import *


def sendPost(post_type):
    auth_header = getConfig()['API']['auth_header']
    url = getConfig()['API']['endpoint'] + APIResources.post
    headers = {'X-Restli-Protocol-Version': '2.0.0', 'Authorization': auth_header, 'Content-Type': 'application/json'}
    if post_type == 1:
        body_values = getTextSharePayload()
    elif post_type == 2:
        body_values = getArticleSharePayload()
    elif post_type == 3:
        body_values = getImageSharePayload()
        uploadURL = body_values['uploadURL']
        asset = body_values['asset']

    body = body_values['json']
    share_id = body_values['shareID']
    postID = requests.post(url=url, json=body, headers=headers)
    id = postID.json()['id']
    print(str(share_id) + '  ---------->  ' + id)
    if post_type == 1 or 2:
        query = 'INSERT INTO payloads.postinfo (shareID, postID, uploadURL, asset) VALUES' \
                ' ("' + str(share_id) + '", "' + id + '", "", "");'
    elif post_type == 3:
        query = 'INSERT INTO payloads.postinfo (shareID, postID, uploadURL, asset) VALUES' \
                ' ("' + str(share_id) + '", "' + id + '", "' + str(uploadURL) + '", "' + str(asset) + '");'

    cursor.execute(query)
    conn.commit()


def delete_Posts():
    auth_header = getConfig()['API']['auth_header']
    query = 'SELECT postID FROM payloads.postinfo;'
    cursor.execute(query)
    postIDs = cursor.fetchall()

    for i in postIDs:
        post_id = i[0]
        print(post_id)
        url = getConfig()['API']['endpoint'] + APIResources.delete + post_id
        requests.delete(url=url, headers={'Authorization': auth_header})
        # query = 'UPDATE payloads.postinfo SET postID = NULL WHERE (postID = "' + post_id + '");'
        # cursor.execute(query)
        # conn.commit()
    query = 'DELETE FROM payloads.postinfo;'
    cursor.execute(query)
    conn.commit()


