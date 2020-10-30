# Created by Chaka at 10/21/2020
Feature: Create posts via the Linkedin API and deletes them
  # Enter feature description here
  Scenario:Create a randomized post
  Given a random post type
  When we send the post request
  Then  the post is visible on my profile and inserted in my database

  Scenario:Create a post
  Given a random post type
  When we send the post request
  Then  the post is visible on my profile and inserted in my database