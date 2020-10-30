import requests
import urllib.request
from utilities.configurations import *
from utilities.resources import *


def getEmailAddress():
    auth_header = getConfig()['API']['auth_header']
    url = getConfig()['API']['endpoint'] + APIResources.email
    parameters = {'q': 'members', 'projection': '(elements*(handle~))'}
    get_email_address = requests.get(url, params=parameters, headers={'Authorization': auth_header})
    email_address = get_email_address.json()['elements'][0]['handle~']['emailAddress']
    return str(email_address)


def getProfilePic():
    auth_header = getConfig()['API']['auth_header']
    url = getConfig()['API']['endpoint'] + APIResources.profile_info
    parameters = {'projection': '(id,firstName,lastName,profilePicture(displayImage~:playableStreams))'}
    pic_list = requests.get(url, params=parameters, headers={'Authorization': auth_header})
    image_path = pic_list.json()['profilePicture']['displayImage~']['elements'][2]['identifiers'][0]['identifier']
    url = image_path
    file_path = 'C:\\Users\\Chaka\\OneDrive\\Desktop\\'
    file_name = 'profile-pic.jpeg'
    full_path = file_path + file_name
    return str(full_path)


