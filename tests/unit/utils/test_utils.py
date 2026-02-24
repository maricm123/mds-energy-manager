import pytest
from rack.utils import calculate_average_rack_energy, calculate_average_rack_units, calculate_power_utilization_percent


################################################################
# CALCULATE POWER UTILIZATION PERCENT
################################################################
class DummyRack:
    def __init__(
        self,
        *,
        total_units: int = 0,
        max_electricity_sustained: int = 0,
    ):
        self.total_units = total_units
        self.max_electricity_sustained = max_electricity_sustained

def test_calculate_power_utilization_percent_returns_0_when_max_is_zero():
    rack = DummyRack(max_electricity_sustained=0)

    result = calculate_power_utilization_percent(rack, used_energy=50)

    assert result == 0.0

def test_calculate_power_utilization_percent_returns_0_when_max_is_negative():
    rack = DummyRack(max_electricity_sustained=-10)

    result = calculate_power_utilization_percent(rack, used_energy=50)

    assert result == 0.0

def test_calculate_power_utilization_percent_calculates_percent_correctly():
    rack = DummyRack(max_electricity_sustained=200)

    result = calculate_power_utilization_percent(rack, used_energy=50)

    assert result == 25.0

def test_calculate_power_utilization_percent_allows_float_result():
    rack = DummyRack(max_electricity_sustained=300)

    result = calculate_power_utilization_percent(rack, used_energy=50)

    assert pytest.approx(result, rel=1e-9) == (50 / 300) * 100


################################################################
# CALCULATE AVERAGE RACK MAX ENERGY
################################################################
def test_calculate_average_rack_max_energy_calculates_average():
    racks = [
        DummyRack(max_electricity_sustained=100),
        DummyRack(max_electricity_sustained=200),
        DummyRack(max_electricity_sustained=300),
    ]

    result = calculate_average_rack_energy(racks)

    assert result == 200


def test_calculate_average_rack_max_energy_returns_float_when_needed():
    racks = [
        DummyRack(max_electricity_sustained=100),
        DummyRack(max_electricity_sustained=101),
    ]

    result = calculate_average_rack_energy(racks)

    assert result == 100.5


################################################################
# CALCULATE AVERAGE MAX RACK UNITS
################################################################
def test_calculate_average_rack_units_returns_correct_average():
    racks = [
        DummyRack(total_units=10),
        DummyRack(total_units=20),
        DummyRack(total_units=30),
    ]

    result = calculate_average_rack_units(racks)

    assert result == 20


def test_calculate_average_rack_units_returns_float_when_needed():
    racks = [
        DummyRack(total_units=1),
        DummyRack(total_units=2),
    ]

    result = calculate_average_rack_units(racks)

    assert result == 1.5
