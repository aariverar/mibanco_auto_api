Feature: API Testing from Excel

Scenario Outline: Generic API Test
  Given the API endpoint is read from the Excel file
  And the headers are read from the Excel file
  When I send a "<Request Type>" request to the endpoint
  Then the response status code should be read from the Excel file
  And the response should contain the expected content from the Excel file

  Examples:
    | Request Type |
    | GET          |
    | POST         |
    | PUT          |