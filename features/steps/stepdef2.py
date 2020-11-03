import random
import requests
from behave import *
from part2.getArticlePayload import *
from part2.getImagePayload import *
from part2.getTextPayload import *
from utilities.configurations import *
from utilities.resources import *


@given('the post request components and the json payloads associated with each {post_type}')
def step_impl(context, post_type):
    context.auth_header = getConfig()['API']['auth_header']
    context.url = getConfig()['API']['endpoint'] + APIResources.post
    context.headers = {'X-Restli-Protocol-Version': '2.0.0', 'Authorization': context.auth_header,
                      'Content-Type': 'application/json'}
    context.post_type = int(post_type)
    if context.post_type == 1:
        context.body_values = getTextSharePayload()
    elif context.post_type == 2:
        context.body_values = getArticleSharePayload()
    elif context.post_type == 3:
        context.body_values = getImageSharePayload()
        context.uploadURL = context.body_values['uploadURL']
        context.asset = context.body_values['asset']



@when('we construct and send the post request')
def step_impl(context):
    context.body = context.body_values['json']
    context.share_id = context.body_values['shareID']
    context.postID = requests.post(url=context.url, json=context.body, headers=context.headers)


@then('the post data will be visible in my postinfo table')
def step_impl(context):
    id = context.postID.json()['id']
    print(str(context.share_id) + '  ---------->  ' + id)
    if context.post_type == 1 or 2:
        query = 'INSERT INTO payloads.postinfo (shareID, postID, uploadURL, asset) VALUES' \
                ' ("' + str(context.share_id) + '", "' + id + '", "", "");'
    elif context.post_type == 3:
        query = 'INSERT INTO payloads.postinfo (shareID, postID, uploadURL, asset) VALUES' \
                ' ("' + str(context.share_id) + '", "' + id + '", "' + str(context.uploadURL) + '", "' + str(context.asset) + '");'

    cursor.execute(query)
    conn.commit()


@given(u'The post ids\' in the postinfo table')
def step_impl(context):
    context.auth_header = getConfig()['API']['auth_header']
    context.query = 'SELECT postID FROM payloads.postinfo;'
    context.cursor.execute(context.query)
    context.postIDs = cursor.fetchall()


@when(u'I send the delete requests')
def step_impl(context):
    for i in context.postIDs:
        context.post_id = i[0]
        print(context.post_id)
        context.url = getConfig()['API']['endpoint'] + APIResources.delete + context.post_id
        requests.delete(url=context.url, headers={'Authorization': context.auth_header})


@then(u'The postinfo table is wiped out')
def step_impl(context):
    context.query = 'DELETE FROM payloads.postinfo;'
    cursor.execute(context.query)
    conn.commit()
