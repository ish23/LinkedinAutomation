# Created by Chaka at 10/16/2020
Feature: Verify to see that details are retrieved via Linkedin API and sent via email
  # Enter feature description here

  Scenario: Verify Email Address retrieved
    Given the email address that needs to be pulled from the LinkedIn API
    When we execute the getEmailAddress method
    Then the Email is successfully retrieved

  Scenario: Verify Profile Picture retrieved
    Given the profile picture that needs to be pulled from the LinkedIn API
    When we execute the getProfilePic method
    Then the picture is successfully retrieved

  Scenario: Verify Email is sent
    Given the message I want to send
    When we execute the send_email method
    Then the email is successfully sent