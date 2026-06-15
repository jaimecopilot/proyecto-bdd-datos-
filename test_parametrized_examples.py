"""
Ejemplos de tests parametrizados usando las fixtures y datos de prueba.
"""
import pytest


class TestCheckInParametrized:
    """Tests parametrizados para check-in."""

    @pytest.mark.parametrize("dataset", [
        {"capacity": 10, "occupancy": 0, "people": 1, "expected_success": True},
        {"capacity": 10, "occupancy": 5, "people": 5, "expected_success": True},
        {"capacity": 10, "occupancy": 9, "people": 2, "expected_success": False},
        {"capacity": 5, "occupancy": 5, "people": 1, "expected_success": False},
    ])
    def test_check_in_various_scenarios(self, room_factory, dataset):
        """Test check-in con múltiples escenarios parametrizados."""
        room = room_factory(
            capacity=dataset["capacity"],
            occupancy=dataset["occupancy"]
        )
        result = room.check_in(dataset["people"])
        assert result["success"] == dataset["expected_success"]

    def test_check_in_from_json(self, datasets_checkin_success, room_factory):
        """Test check-in usando datos del JSON."""
        for test_case in datasets_checkin_success:
            room = room_factory(
                capacity=test_case["room"]["capacity"],
                occupancy=test_case["room"]["current_occupancy"]
            )
            result = room.check_in(test_case["people_count"])
            assert result["success"] == test_case["expected_result"]["success"]
            assert room.current_occupancy == test_case["expected_result"]["final_occupancy"]


class TestOccupancyPercentage:
    """Tests para cálculo de porcentaje con parametrización."""

    @pytest.mark.parametrize("capacity,occupancy,expected_pct", [
        (10, 0, 0.0),
        (10, 5, 50.0),
        (10, 10, 100.0),
        (20, 5, 25.0),
        (100, 1, 1.0),
    ])
    def test_occupancy_percentage(self, room_factory, capacity, occupancy, expected_pct):
        """Test cálculo de porcentaje con múltiples casos."""
        room = room_factory(capacity=capacity, occupancy=occupancy)
        assert room.occupancy_percentage() == expected_pct

    def test_occupancy_from_json_dataset(self, datasets_occupancy_percentage, room_factory):
        """Test porcentaje usando dataset del JSON."""
        for test_case in datasets_occupancy_percentage:
            room = room_factory(
                capacity=test_case["room"]["capacity"],
                occupancy=test_case["room"]["current_occupancy"]
            )
            percentage = room.occupancy_percentage()
            assert abs(percentage - test_case["expected_percentage"]) < 0.01


class TestBatchOperations:
    """Tests para operaciones en lote."""

    def test_batch_check_in_operations(self, occupancy_service_with_rooms, operation_log):
        """Test múltiples check-ins en secuencia."""
        room = occupancy_service_with_rooms.get_room("Sala A")
        
        operations = [
            {"people": 2, "expected_occupancy": 2},
            {"people": 3, "expected_occupancy": 5},
            {"people": 4, "expected_occupancy": 9},
        ]
        
        for op in operations:
            result = room.check_in(op["people"])
            assert result["success"]
            assert room.current_occupancy == op["expected_occupancy"]
            operation_log.append(result)

    def test_mixed_operations(self, room_factory, operation_log):
        """Test mezcla de check-in y check-out."""
        room = room_factory(capacity=10)
        
        sequence = [
            ("check_in", 8),
            ("check_out", 2),
            ("check_in", 3),
            ("check_out", 4),
        ]
        
        expected_occupancies = [8, 6, 9, 5]
        
        for (op_type, count), expected in zip(sequence, expected_occupancies):
            if op_type == "check_in":
                result = room.check_in(count)
            else:
                result = room.check_out(count)
            
            assert result["success"]
            assert room.current_occupancy == expected
            operation_log.append({"operation": op_type, "count": count})


class TestEdgeCases:
    """Tests para casos borde."""

    @pytest.mark.parametrize("capacity", [1, 2, 5, 10, 50, 100, 1000])
    def test_various_room_capacities(self, room_factory, capacity):
        """Test salas con diversas capacidades."""
        room = room_factory(capacity=capacity)
        assert room.capacity == capacity
        assert room.is_empty()
        assert room.available_capacity() == capacity

    def test_single_person_room(self, room_factory):
        """Test sala de 1 persona."""
        room = room_factory(capacity=1)
        assert room.check_in(1)["success"]
        assert room.is_full()
        assert room.check_in(1)["success"] == False

    def test_very_large_room(self, room_factory):
        """Test sala muy grande."""
        room = room_factory(capacity=10000)
        result = room.check_in(5000)
        assert result["success"]
        assert room.current_occupancy == 5000


class TestServiceOperations:
    """Tests para operaciones del servicio."""

    def test_service_add_multiple_rooms(self, occupancy_service, bulk_room_creator):
        """Test agregar múltiples salas al servicio."""
        configurations = [
            {"capacity": 10, "name": "Sala A", "occupancy": 0},
            {"capacity": 20, "name": "Sala B", "occupancy": 10},
            {"capacity": 5, "name": "Sala C", "occupancy": 5},
        ]
        
        rooms = bulk_room_creator(configurations)
        for room in rooms:
            occupancy_service.add_room(room)
        
        assert len(occupancy_service.rooms) == 3

    def test_service_summary(self, occupancy_service_populated):
        """Test resumen del servicio."""
        summary = occupancy_service_populated.get_occupancy_summary()
        
        assert summary["total_rooms"] == 4
        assert summary["total_capacity"] == 53  # 10+20+15+8
        assert summary["total_occupancy"] == 32  # 0+10+14+8
        assert summary["full_rooms"] == 1
        assert summary["empty_rooms"] == 1
