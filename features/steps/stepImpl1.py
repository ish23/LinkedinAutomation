import os.path
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
from behave import *
from part1.getProfileDetails import *
from part1.sendEmail import send_email
from utilities.configurations import *
from utilities.resources import *


@given('the email address that needs to be pulled from the LinkedIn API')
def step_impl(context):
    context.auth_header = getConfig()['API']['auth_header']
    context.url = getConfig()['API']['endpoint'] + APIResources.email
    context.parameters = {'q': 'members', 'projection': '(elements*(handle~))'}

@when('we execute the getEmailAddress method')
def step_impl(context):
    context.get_email_address = requests.get(context.url, params=context.parameters, headers={'Authorization': context.auth_header})

@then('the Email is successfully retrieved')
def step_impl(context):
    email_address = context.get_email_address.json()['elements'][0]['handle~']['emailAddress']
    return str(email_address)


@given('the profile picture that needs to be pulled from the LinkedIn API')
def step_ipl(context):
    context.auth_header = getConfig()['API']['auth_header']
    context.url = getConfig()['API']['endpoint'] + APIResources.profile_info
    context.parameters = {'projection': '(id,firstName,lastName,profilePicture(displayImage~:playableStreams))'}

@when('we execute the getProfilePic method')
def step_impl(context):
    context.pic_list = requests.get(context.url, params=context.parameters, headers={'Authorization': context.auth_header})


@then('the picture is successfully retrieved')
def step_impl(context):
    image_path = context.pic_list.json()['profilePicture']['displayImage~']['elements'][2]['identifiers'][0]['identifier']
    context.url = image_path
    file_path = 'C:\\Users\\Chaka\\OneDrive\\Desktop\\'
    file_name = 'profile-pic.jpeg'
    full_path = file_path + file_name
    return str(full_path)

@given('the message I want to send')
def step_impl(context):
    context.email_recipient = getEmailAddress()
    context.email_subject = 'API Test'
    context.email_message = 'Automation is cool.'
    context.attachment_location = getProfilePic()


@when('we execute the send_email method')
def step_impl(context):
    context.email_sender = getConfig()['API']['email_address']

    context.msg = MIMEMultipart()
    context.msg['From'] = context.email_sender
    context.msg['To'] = context.email_recipient
    context.msg['Subject'] = context.email_subject

    context.msg.attach(MIMEText(context.email_message, 'plain'))

    if context.attachment_location != '':
        context.filename = os.path.basename(context.attachment_location)
        context.attachment = open(context.attachment_location, "rb")
        context.part = MIMEBase('application', 'octet-stream')
        context.part.set_payload(context.attachment.read())
        encoders.encode_base64(context.part)
        context.part.add_header('Content-Disposition',
                        "attachment; filename= %s" % context.filename)
        context.msg.attach(context.part)


@then('the email is successfully sent')
def step_impl(context):
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(context.email_sender, getConfig()['API']['email_password'])
        text = context.msg.as_string()
        server.sendmail(context.email_sender, context.email_recipient, text)
        print('email sent')
        server.quit()
    except:
        print("SMPT server connection error")
    return True
