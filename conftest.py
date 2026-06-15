"""
Configuración centralizada de fixtures para tests de ocupación de salas.
Proporciona datos, servicios e inyección de dependencias para todos los tests.
"""
import pytest
import json
from pathlib import Path
from typing import Dict, List, Optional
from room_manager import Room, RoomOccupancyService


# ==================== CARGA DE DATOS ====================

@pytest.fixture(scope="session")
def test_data_path():
    """Retorna la ruta al archivo de datos de prueba."""
    return Path(__file__).parent / "datos_prueba.json"


@pytest.fixture(scope="session")
def load_test_data(test_data_path):
    """Carga los datos de prueba desde JSON."""
    with open(test_data_path, 'r', encoding='utf-8') as f:
        return json.load(f)


# ==================== FIXTURES BÁSICAS ====================

@pytest.fixture
def room_default():
    """Fixture: Sala con capacidad estándar (10 personas)."""
    return Room(capacity=10, name="Sala A")


@pytest.fixture
def room_small():
    """Fixture: Sala pequeña (5 personas)."""
    return Room(capacity=5, name="Sala B - Pequeña")


@pytest.fixture
def room_large():
    """Fixture: Sala grande (50 personas)."""
    return Room(capacity=50, name="Sala C - Grande")


@pytest.fixture
def room_medium():
    """Fixture: Sala mediana (20 personas)."""
    return Room(capacity=20, name="Sala D - Mediana")


# ==================== FIXTURES DE SALAS CON OCUPACIÓN ====================

@pytest.fixture
def room_empty():
    """Fixture: Sala vacía (0/10)."""
    room = Room(capacity=10, name="Sala Vacía")
    return room


@pytest.fixture
def room_half_occupied():
    """Fixture: Sala a media capacidad (5/10)."""
    room = Room(capacity=10, name="Sala Semi-Llena")
    room.current_occupancy = 5
    room.movement_log.append({"type": "check_in", "count": 5})
    return room


@pytest.fixture
def room_almost_full():
    """Fixture: Sala casi llena (9/10)."""
    room = Room(capacity=10, name="Sala Casi Llena")
    room.current_occupancy = 9
    room.movement_log.append({"type": "check_in", "count": 9})
    return room


@pytest.fixture
def room_full():
    """Fixture: Sala completamente llena (10/10)."""
    room = Room(capacity=10, name="Sala Llena")
    room.current_occupancy = 10
    room.movement_log.append({"type": "check_in", "count": 10})
    return room


@pytest.fixture
def room_at_capacity():
    """Fixture: Sala exactamente a capacidad máxima."""
    room = Room(capacity=20, name="Sala Exacta")
    room.current_occupancy = 20
    return room


# ==================== FIXTURES DEL SERVICIO ====================

@pytest.fixture
def occupancy_service():
    """Fixture: Servicio de ocupación sin salas."""
    return RoomOccupancyService()


@pytest.fixture
def occupancy_service_with_rooms():
    """Fixture: Servicio preconfigurado con múltiples salas."""
    service = RoomOccupancyService()
    
    # Agregar salas de diferentes tamaños
    service.add_room(Room(capacity=10, name="Sala A"))
    service.add_room(Room(capacity=20, name="Sala B"))
    service.add_room(Room(capacity=5, name="Sala C"))
    service.add_room(Room(capacity=50, name="Auditorio"))
    
    return service


@pytest.fixture
def occupancy_service_populated():
    """Fixture: Servicio con salas y algunas ocupadas."""
    service = RoomOccupancyService()
    
    # Sala 1: Vacía
    room1 = Room(capacity=10, name="Sala A - Vacía")
    service.add_room(room1)
    
    # Sala 2: A media capacidad
    room2 = Room(capacity=20, name="Sala B - Semi-Llena")
    room2.current_occupancy = 10
    service.add_room(room2)
    
    # Sala 3: Casi llena
    room3 = Room(capacity=15, name="Sala C - Casi Llena")
    room3.current_occupancy = 14
    service.add_room(room3)
    
    # Sala 4: Llena
    room4 = Room(capacity=8, name="Sala D - Llena")
    room4.current_occupancy = 8
    service.add_room(room4)
    
    return service


# ==================== FIXTURES DE RESULTADOS ====================

@pytest.fixture
def result_container():
    """Fixture: Contenedor para almacenar resultados de operaciones."""
    return {
        "check_in_result": None,
        "check_out_result": None,
        "operation_results": [],
        "errors": []
    }


@pytest.fixture
def check_in_result():
    """Fixture: Almacena resultado del último check-in."""
    return {"success": None, "message": None}


@pytest.fixture
def check_out_result():
    """Fixture: Almacena resultado del último check-out."""
    return {"success": None, "message": None}


@pytest.fixture
def operation_log():
    """Fixture: Registro de todas las operaciones realizadas."""
    return []


# ==================== FIXTURES PARAMETRIZADAS ====================

@pytest.fixture(params=[
    {"capacity": 5, "name": "Pequeña"},
    {"capacity": 10, "name": "Estándar"},
    {"capacity": 20, "name": "Mediana"},
    {"capacity": 50, "name": "Grande"},
    {"capacity": 100, "name": "Auditorio"},
])
def rooms_various_capacities(request):
    """Fixture parametrizada: Salas con diferentes capacidades."""
    return Room(capacity=request.param["capacity"], name=f"Sala {request.param['name']}")


@pytest.fixture(params=[0, 1, 5, 10])
def various_occupancy_levels(request):
    """Fixture parametrizada: Diferentes niveles de ocupación."""
    return request.param


# ==================== FIXTURES DE DATOS DE PRUEBA ====================

@pytest.fixture
def datasets_checkin_success(load_test_data):
    """Fixture: Casos de éxito para check-in."""
    return load_test_data["check_in"]["success"]


@pytest.fixture
def datasets_checkin_failure(load_test_data):
    """Fixture: Casos de fallo para check-in."""
    return load_test_data["check_in"]["failure"]


@pytest.fixture
def datasets_checkout_success(load_test_data):
    """Fixture: Casos de éxito para check-out."""
    return load_test_data["check_out"]["success"]


@pytest.fixture
def datasets_checkout_failure(load_test_data):
    """Fixture: Casos de fallo para check-out."""
    return load_test_data["check_out"]["failure"]


@pytest.fixture
def datasets_edge_cases(load_test_data):
    """Fixture: Casos borde/extremos."""
    return load_test_data["edge_cases"]


@pytest.fixture
def datasets_occupancy_percentage(load_test_data):
    """Fixture: Casos para cálculo de porcentaje."""
    return load_test_data["occupancy_percentage"]


# ==================== FIXTURES DE ESTADO ====================

@pytest.fixture
def room_state_tracker():
    """Fixture: Rastreador de estados de salas para auditoría."""
    return {
        "initial_state": None,
        "state_changes": [],
        "final_state": None
    }


@pytest.fixture
def audit_log():
    """Fixture: Log de auditoría para rastrear todas las operaciones."""
    return {
        "timestamp": [],
        "operation": [],
        "room_name": [],
        "before_state": [],
        "after_state": [],
        "success": [],
        "error_message": []
    }


# ==================== FIXTURES COMBINADAS ====================

@pytest.fixture
def test_context(occupancy_service_populated, result_container, operation_log):
    """
    Fixture: Contexto completo para pruebas.
    Combina servicio, contenedor de resultados y log de operaciones.
    """
    return {
        "service": occupancy_service_populated,
        "results": result_container,
        "log": operation_log,
        "timestamp": None,
        "test_id": None
    }


# ==================== HELPERS Y UTILITARIOS ====================

@pytest.fixture
def room_factory():
    """Fixture: Factory para crear salas dinámicamente."""
    def _create_room(capacity: int, name: str = None, occupancy: int = 0):
        room = Room(capacity=capacity, name=name or f"Sala {capacity}")
        room.current_occupancy = occupancy
        return room
    return _create_room


@pytest.fixture
def bulk_room_creator():
    """Fixture: Crear múltiples salas de una vez."""
    def _create_rooms(configurations: List[Dict]) -> List[Room]:
        rooms = []
        for config in configurations:
            room = Room(
                capacity=config.get("capacity", 10),
                name=config.get("name", "Sala")
            )
            if "occupancy" in config:
                room.current_occupancy = config["occupancy"]
            rooms.append(room)
        return rooms
    return _create_rooms


@pytest.fixture
def assertion_helper():
    """Fixture: Funciones auxiliares para aserciones comunes."""
    class AssertionHelper:
        @staticmethod
        def assert_success(result):
            assert result["success"] is True, f"Operación falló: {result['message']}"
        
        @staticmethod
        def assert_failure(result):
            assert result["success"] is False, "Operación debería haber fallado"
        
        @staticmethod
        def assert_room_capacity(room, expected):
            assert room.current_occupancy == expected, \
                f"Ocupación esperada {expected}, obtenido {room.current_occupancy}"
        
        @staticmethod
        def assert_occupancy_percentage(room, expected):
            actual = room.occupancy_percentage()
            assert actual == expected, \
                f"Porcentaje esperado {expected}%, obtenido {actual}%"
    
    return AssertionHelper()


# ==================== HOOKS Y TEARDOWN ====================

@pytest.fixture(autouse=True)
def reset_occupancy_service(occupancy_service):
    """Hook: Reset automático del servicio después de cada test."""
    yield occupancy_service
    # Cleanup
    occupancy_service.rooms.clear()


@pytest.fixture
def cleanup_rooms():
    """Fixture: Limpieza manual de salas después del test."""
    rooms = []
    yield rooms
    rooms.clear()
