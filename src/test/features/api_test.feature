Feature: API Testing from Excel

  @test1
  Scenario Outline: Api Test
    Given se lee el endpoint y lo headers del excel "<datos>"
    When cuando envio un request al endpoint "<datos>"
    Then se valida el estado del response con el esperado del excel "<datos>"
    And the response should contain the expected content from the Excel file

    Examples:
      | datos |
      |     1 |
      |     2 |
      |     3 |
      |     4 |
