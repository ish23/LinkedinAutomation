# Created by Chaka at 10/21/2020
Feature: Create posts via the Linkedin API and deletes them
  # Enter feature description here

  @create
  Scenario Outline:Create a post
    Given the post request components and the json payloads associated with each <post_type>
    When we construct and send the post request
    Then the post data will be visible in my postinfo table
    #POST TYPE KEY: 1 = text, 2 = article, 3 = image
    Examples:
      |post_type|
      | 1       |
      | 3       |

  @delete
  Scenario: Delete all posts
    Given The post ids' in the postinfo table
    When I send the delete requests
    Then The postinfo table is wiped out