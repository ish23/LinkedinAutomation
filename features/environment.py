# def after_scenario(context, scenario):
#     auth_header = context.getConfig()['API']['auth_header']
#     query = 'SELECT postID FROM payloads.body;'
#     context.cursor.execute(query)
#     postIDs = context.cursor.fetchall()
#
#     for i in postIDs:
#         if i[0] != None and i[0] != '':
#             post_id = i[0]
#             url = context.getConfig()['API']['endpoint'] + context.APIResources.delete + post_id
#             context.requests.delete(url=url, headers={'Authorization': auth_header})
#             query = 'UPDATE payloads.body SET postID = NULL WHERE (postID = "' + post_id + '");'
#             context.cursor.execute(query)
#             context.conn.commit()
