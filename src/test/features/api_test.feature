Feature: API Testing from Excel

  @test1 @Prueba
  Scenario Outline: Api Test
    Given se lee el endpoint y lo headers del excel "<datos>"
    When cuando envio un request al endpoint "<datos>"
    Then se valida el estado del response con el esperado del excel "<datos>"
    And el response debe contener el contenido esperado del excel "<datos>"
    
    Examples:
      | datos |
      |     1 |
      |     2 |
      |     3 |
      |     4 |
      |     5 |
