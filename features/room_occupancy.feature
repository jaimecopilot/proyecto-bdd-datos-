# language: es
Feature: Gestión de Ocupación de Salas
  Como responsable de salas de conferencias
  Quiero un sistema que controle la ocupación
  Para garantizar que no se supere la capacidad máxima

  Scenario: Check-in exitoso dentro de la capacidad
    Given una sala con capacidad máxima de 10 personas
    When entran 5 personas a la sala
    Then el check-in es exitoso
    And la ocupación actual es 5 personas
    And la capacidad disponible es 5 personas

  Scenario: Check-in falla al superar capacidad
    Given una sala con capacidad máxima de 10 personas
    And hay 7 personas en la sala
    When intenta entrar 5 personas más
    Then el check-in falla
    And la ocupación actual sigue siendo 7 personas

  Scenario: Check-out exitoso
    Given una sala con capacidad máxima de 10 personas
    And hay 8 personas en la sala
    When salen 3 personas
    Then el check-out es exitoso
    And la ocupación actual es 5 personas

  Scenario: Check-out falla al intentar sacar más de las presentes
    Given una sala con capacidad máxima de 10 personas
    And hay 4 personas en la sala
    When intenta salir 6 personas
    Then el check-out falla
    And la ocupación actual sigue siendo 4 personas

  Scenario: Cálculo correcto del porcentaje de ocupación
    Given una sala con capacidad máxima de 10 personas
    When entran 5 personas
    Then el porcentaje de ocupación es 50%
    When entran 5 personas más
    Then el porcentaje de ocupación es 100%
    When salen 3 personas
    Then el porcentaje de ocupación es 70%

  Scenario: Sala llena
    Given una sala con capacidad máxima de 10 personas
    When entran 10 personas
    Then la sala está llena
    And la capacidad disponible es 0

  Scenario: Reseteo de la sala
    Given una sala con capacidad máxima de 10 personas
    And hay 7 personas en la sala
    And hay 3 registros en el log
    When se resetea la sala
    Then la ocupación es 0
    And la capacidad disponible es 10
    And el registro de movimientos está vacío
