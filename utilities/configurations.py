import configparser
import random

import mysql.connector
from mysql.connector import Error


def getConfig():
    config = configparser.ConfigParser()
    config.read('C:\\Users\\Chaka\\pycharm_workspace\\LinkedinAPItesting\\utilities\\properties.ini')
    return config


connect_config = {
    'host': getConfig()['SQL']['host'],
    'database': getConfig()['SQL']['database'],
    'user': getConfig()['SQL']['user'],
    'password': getConfig()['SQL']['password']
}


def getConnection():
    try:
        conn = mysql.connector.connect(**connect_config)
        if conn.is_connected():
            print('DB Connection Successful')
            return conn
    except Error as e:
        print(e)


conn = getConnection()
cursor = conn.cursor()


def getFields(share_id):
    cursor.execute('SELECT * FROM payloads.body WHERE shareID = {};'.format(share_id))
    row = cursor.fetchone()
    fields = {
        'postKind': row[1],
        'author': row[2],
        'lifeCycleState': row[3],
        'shareCommentary': row[4],
        'shareMediaCategory': row[5],
        'mediaStatus': row[6],
        'mediaDescription': row[7],
        'originalURL': row[8],
        'title': row[9],
        'visibility': row[10],
        'resourcePath': row[11],
    }
    bod_values = {'fields': fields, 'primaryKey': share_id}
    return bod_values

def getPossiblePosts(post_kind):
    if post_kind == 1:
        cursor.execute('SELECT * FROM payloads.body WHERE postType = 1;')
        textShares = cursor.fetchall()
        return textShares
    elif post_kind == 2:
        cursor.execute('SELECT * FROM payloads.body WHERE postType = 2;')
        articleShares = cursor.fetchall()
        return articleShares
    elif post_kind == 3:
        cursor.execute('SELECT * FROM payloads.body WHERE postType = 3;')
        imageShares = cursor.fetchall()
        return imageShares



def randomPost(post_kind):
    cursor.execute('SELECT * FROM payloads.body WHERE postKind = {};'.format(post_kind))
    allPosts = cursor.fetchall()
    length = len(allPosts) - 1
    randIndex = random.randint(0, length)
    randPost = allPosts[randIndex]
    randPrimaryKey = randPost[0]
    return randPrimaryKey
