# Room Occupancy BDD Tests 🚀

Sistema completo de pruebas BDD usando **pytest-bdd** para gestión de ocupación de salas de conferencias.

## 📋 Características

✅ **Tests BDD en Gherkin** (7 escenarios completos)  
✅ **Fixtures parametrizadas** (25+ fixtures reutilizables)  
✅ **Datos de prueba en JSON** (50+ casos de prueba)  
✅ **pytest.mark.parametrize** para tests escalables  
✅ **CI/CD con GitHub Actions** (test automáticos en push)  
✅ **Rama de desarrollo** separada (develop)  
✅ **Cobertura de tests** y reportes  

## 🏗️ Estructura del Proyecto

```
proyecto-bdd-datos-/
├── room_manager.py              # Lógica de negocio + servicio
├── conftest.py                  # Fixtures reutilizables (25+)
├── datos_prueba.json            # Datos de prueba (50+ casos)
├── features/
│   ├── room_occupancy.feature   # 7 escenarios Gherkin
│   └── steps.py                 # 25 definiciones de pasos
├── test_parametrized_examples.py # Tests parametrizados
├── .github/workflows/
│   └── tests.yml                # CI/CD automático
├── requirements.txt
├── pytest.ini
└── README.md
```

## 🚀 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/jaimecopilot/proyecto-bdd-datos-.git
cd proyecto-bdd-datos-

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

## ▶️ Ejecutar Tests

### Todos los tests
```bash
pytest -v
```

### Solo tests BDD
```bash
pytest features/ -v
```

### Solo tests parametrizados
```bash
pytest test_parametrized_examples.py -v
```

### Un test específico
```bash
pytest -k "test_occupancy_percentage" -v
```

### Con cobertura
```bash
pytest --cov=. --cov-report=html
```

### Con reporte JSON
```bash
pytest --json-report --json-report-file=report.json
```

## 📊 Datos de Prueba

El archivo `datos_prueba.json` contiene:

- **10 casos check-in exitosos**
- **10 casos check-in fallidos**
- **10 casos check-out exitosos**
- **10 casos check-out fallidos**
- **6 casos porcentaje ocupación**
- **4 casos borde/extremos**
- **2 operaciones en lote**

## 🔧 Fixtures Disponibles

### Salas Básicas
- `room_default` - Sala estándar (10 personas)
- `room_small` - Sala pequeña (5 personas)
- `room_medium` - Sala mediana (20 personas)
- `room_large` - Sala grande (50 personas)

### Salas con Ocupación
- `room_empty` - Vacía
- `room_half_occupied` - A media capacidad
- `room_almost_full` - Casi llena
- `room_full` - Completamente llena

### Servicio
- `occupancy_service` - Servicio sin salas
- `occupancy_service_with_rooms` - Con 4 salas precargadas
- `occupancy_service_populated` - Con salas ocupadas

### Datos
- `load_test_data` - Carga JSON completo
- `datasets_checkin_success` - Casos éxito check-in
- `datasets_checkin_failure` - Casos fallo check-in
- `datasets_checkout_success` - Casos éxito check-out
- `datasets_occupancy_percentage` - Casos porcentaje
- `datasets_edge_cases` - Casos borde

### Helpers
- `room_factory` - Factory para crear salas dinámicamente
- `bulk_room_creator` - Crear múltiples salas
- `assertion_helper` - Funciones auxiliares para aserciones

## 🌲 Ramas del Repositorio

- **main** - Rama de producción (releases)
- **develop** - Rama de desarrollo (features en progress)

## 🔄 CI/CD con GitHub Actions

La acción automática en `.github/workflows/tests.yml`:

✅ Se ejecuta en cada push y pull request  
✅ Ejecuta todos los tests  
✅ Genera reporte de cobertura  
✅ Publica resultados  

## 📝 Ejemplos de Uso

### Test simple con fixture
```python
def test_room_check_in(room_default):
    result = room_default.check_in(5)
    assert result["success"] is True
    assert room_default.current_occupancy == 5
```

### Test parametrizado
```python
@pytest.mark.parametrize("capacity,occupancy,expected", [
    (10, 0, 0.0),
    (10, 5, 50.0),
    (10, 10, 100.0),
])
def test_occupancy_percentage(room_factory, capacity, occupancy, expected):
    room = room_factory(capacity=capacity, occupancy=occupancy)
    assert room.occupancy_percentage() == expected
```

### Test con datos JSON
```python
def test_from_json(datasets_checkin_success, room_factory):
    for test_case in datasets_checkin_success:
        room = room_factory(
            capacity=test_case["room"]["capacity"],
            occupancy=test_case["room"]["current_occupancy"]
        )
        result = room.check_in(test_case["people_count"])
        assert result["success"] == test_case["expected_result"]["success"]
```

### Test BDD
```gherkin
Scenario: Check-in exitoso dentro de la capacidad
    Given una sala con capacidad máxima de 10 personas
    When entran 5 personas a la sala
    Then el check-in es exitoso
    And la ocupación actual es 5 personas
```

## 🛠️ Desarrollo

### Agregar un nuevo escenario

1. Agregar en `features/room_occupancy.feature`:
```gherkin
Scenario: Mi nuevo escenario
    Given ...
    When ...
    Then ...
```

2. Implementar pasos en `features/steps.py`

3. Ejecutar: `pytest features/`

### Agregar un nuevo test parametrizado

1. Crear en `test_parametrized_examples.py`:
```python
@pytest.mark.parametrize("param", [...])
def test_mi_test(room_factory, param):
    # test logic
```

2. Ejecutar: `pytest test_parametrized_examples.py -v`

## 📊 Estadísticas

- **Arquivos**: 9
- **Tests BDD**: 7 escenarios
- **Tests parametrizados**: 10+ tests
- **Fixtures**: 25+ disponibles
- **Casos de prueba JSON**: 50+
- **Líneas de código**: 1500+

## 📞 Contacto

**Autor**: @jaimecopilot  
**Repositorio**: https://github.com/jaimecopilot/proyecto-bdd-datos-

---

**Última actualización**: 2026-06-15  
**Estado**: ✅ Activo y en desarrollo
