"""
Definiciones de pasos para los tests BDD de gestión de ocupación de salas.
Utiliza pytest-bdd para mapear Gherkin a código Python.
"""
from pytest_bdd import given, when, then, scenarios
import pytest
from room_manager import Room

# Cargar todos los escenarios desde el archivo feature
scenarios('room_occupancy.feature')


# ==================== GIVEN (Precondiciones) ====================

@given('una sala con capacidad máxima de 10 personas')
def given_room_with_capacity_10(room):
    """Proporciona una sala con capacidad máxima de 10 personas."""
    assert room.capacity == 10
    return room


@given('hay 7 personas en la sala')
def given_7_people_in_room(room):
    """Establece 7 personas en la sala."""
    room.current_occupancy = 7
    assert room.current_occupancy == 7


@given('hay 8 personas en la sala')
def given_8_people_in_room(room):
    """Establece 8 personas en la sala."""
    room.current_occupancy = 8
    assert room.current_occupancy == 8


@given('hay 4 personas en la sala')
def given_4_people_in_room(room):
    """Establece 4 personas en la sala."""
    room.current_occupancy = 4
    assert room.current_occupancy == 4


@given('hay 3 registros en el log')
def given_3_log_entries(room):
    """Agrega 3 registros al log de movimientos."""
    room.movement_log = [
        {"type": "check_in", "count": 2},
        {"type": "check_in", "count": 3},
        {"type": "check_in", "count": 2},
    ]
    assert len(room.movement_log) == 3


# ==================== WHEN (Acciones) ====================

@when('entran 5 personas a la sala')
def when_5_people_enter(room, check_in_result):
    """Registra la entrada de 5 personas."""
    check_in_result.update(room.check_in(5))


@when('intenta entrar 5 personas más')
def when_5_more_people_try_enter(room, check_in_result):
    """Intenta registrar la entrada de 5 personas más."""
    check_in_result.update(room.check_in(5))


@when('salen 3 personas')
def when_3_people_leave(room, check_out_result):
    """Registra la salida de 3 personas."""
    check_out_result.update(room.check_out(3))


@when('intenta salir 6 personas')
def when_6_people_try_leave(room, check_out_result):
    """Intenta registrar la salida de 6 personas."""
    check_out_result.update(room.check_out(6))


@when('entran 10 personas')
def when_10_people_enter(room, check_in_result):
    """Registra la entrada de 10 personas."""
    check_in_result.update(room.check_in(10))


@when('se resetea la sala')
def when_room_reset(room):
    """Resetea la sala."""
    room.reset()


# ==================== THEN (Verificaciones) ====================

@then('el check-in es exitoso')
def then_checkin_successful(check_in_result):
    """Verifica que el check-in fue exitoso."""
    assert check_in_result["success"] is True, \
        f"Check-in debería ser exitoso, pero falló: {check_in_result['message']}"


@then('el check-in falla')
def then_checkin_fails(check_in_result):
    """Verifica que el check-in falló."""
    assert check_in_result["success"] is False, \
        f"Check-in debería fallar, pero fue exitoso"


@then('el check-out es exitoso')
def then_checkout_successful(check_out_result):
    """Verifica que el check-out fue exitoso."""
    assert check_out_result["success"] is True, \
        f"Check-out debería ser exitoso, pero falló: {check_out_result['message']}"


@then('el check-out falla')
def then_checkout_fails(check_out_result):
    """Verifica que el check-out falló."""
    assert check_out_result["success"] is False, \
        f"Check-out debería fallar, pero fue exitoso"


@then('la ocupación actual es 5 personas')
def then_occupancy_is_5(room):
    """Verifica que la ocupación actual es 5 personas."""
    assert room.current_occupancy == 5, \
        f"La ocupación debería ser 5, pero es {room.current_occupancy}"


@then('la ocupación actual sigue siendo 7 personas')
def then_occupancy_still_7(room):
    """Verifica que la ocupación sigue siendo 7 personas."""
    assert room.current_occupancy == 7, \
        f"La ocupación debería seguir siendo 7, pero es {room.current_occupancy}"


@then('la ocupación actual sigue siendo 4 personas')
def then_occupancy_still_4(room):
    """Verifica que la ocupación sigue siendo 4 personas."""
    assert room.current_occupancy == 4, \
        f"La ocupación debería seguir siendo 4, pero es {room.current_occupancy}"


@then('la capacidad disponible es 5 personas')
def then_available_capacity_is_5(room):
    """Verifica que la capacidad disponible es 5 personas."""
    assert room.available_capacity() == 5, \
        f"La capacidad disponible debería ser 5, pero es {room.available_capacity()}"


@then('la capacidad disponible es 0')
def then_available_capacity_is_0(room):
    """Verifica que la capacidad disponible es 0."""
    assert room.available_capacity() == 0, \
        f"La capacidad disponible debería ser 0, pero es {room.available_capacity()}"


@then('la sala está llena')
def then_room_is_full(room):
    """Verifica que la sala está llena."""
    assert room.is_full() is True, \
        f"La sala debería estar llena, pero no lo está"


@then('el porcentaje de ocupación es 50%')
def then_occupancy_percentage_50(room):
    """Verifica que el porcentaje de ocupación es 50%."""
    assert room.occupancy_percentage() == 50.0, \
        f"El porcentaje debería ser 50%, pero es {room.occupancy_percentage()}%"


@then('el porcentaje de ocupación es 100%')
def then_occupancy_percentage_100(room):
    """Verifica que el porcentaje de ocupación es 100%."""
    assert room.occupancy_percentage() == 100.0, \
        f"El porcentaje debería ser 100%, pero es {room.occupancy_percentage()}%"


@then('el porcentaje de ocupación es 70%')
def then_occupancy_percentage_70(room):
    """Verifica que el porcentaje de ocupación es 70%."""
    assert room.occupancy_percentage() == 70.0, \
        f"El porcentaje debería ser 70%, pero es {room.occupancy_percentage()}%"


@then('la ocupación es 0')
def then_occupancy_is_0(room):
    """Verifica que la ocupación es 0."""
    assert room.current_occupancy == 0, \
        f"La ocupación debería ser 0, pero es {room.current_occupancy}"


@then('el registro de movimientos está vacío')
def then_movement_log_empty(room):
    """Verifica que el registro de movimientos está vacío."""
    assert len(room.movement_log) == 0, \
        f"El registro debería estar vacío, pero tiene {len(room.movement_log)} entradas"
