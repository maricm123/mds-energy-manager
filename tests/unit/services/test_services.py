from rack import services
from rack.services import (
    order_devices_per_power_and_units,
    suggest_algorithm_for_rack,
    _choose_best_rack_for_device, _calculate_extend_after_placement, _can_store_device_in_rack
)


class DummyRack:
    def __init__(
        self,
        *,
        id: int = 1,
        total_units: int = 0,
        max_electricity_sustained: int = 0,
    ):
        self.id = id
        self.total_units = total_units
        self.max_electricity_sustained = max_electricity_sustained


class DummyDevice:
    def __init__(
        self,
        *,
        electricity_consumption: int,
        number_of_rack_units: int = 0,
        name: str = "",
    ):
        self.electricity_consumption = electricity_consumption
        self.number_of_rack_units = number_of_rack_units
        self.name = name


################################################################
# ORDER DEVICES PER POWER AND UNITS
################################################################
def test_order_devices_per_power_and_units_orders_by_score_desc():
    racks = [
        DummyRack(max_electricity_sustained=100, total_units=10),
        DummyRack(max_electricity_sustained=300, total_units=30),
    ]

    # score = 0.7*(w/avg_energy) + 0.3*(u/avg_units)
    # A: w=200 => 0.7*(1) + 0.3*(10/20=0.5) = 0.7 + 0.15 = 0.85
    # B: w=300 => 0.7*(1.5) + 0.3*(1/20=0.05) = 1.05 + 0.015 = 1.065
    # C: w=50  => 0.7*(0.25) + 0.3*(20/20=1) = 0.175 + 0.3 = 0.475
    device_a = DummyDevice(name="A", electricity_consumption=200, number_of_rack_units=10)
    device_b = DummyDevice(name="B", electricity_consumption=300, number_of_rack_units=1)
    device_c = DummyDevice(name="C", electricity_consumption=50, number_of_rack_units=20)

    result = order_devices_per_power_and_units(racks, [device_a, device_b, device_c])

    assert result == [device_b, device_a, device_c]


def test_order_devices_per_power_and_units_returns_empty_when_no_devices():
    racks = [DummyRack(max_electricity_sustained=100, total_units=10)]

    result = order_devices_per_power_and_units(racks, [])

    assert result == []


def test_order_devices_per_power_and_units_preserves_device_instances():
    racks = [DummyRack(max_electricity_sustained=100, total_units=10)]
    d1 = DummyDevice(name="d1", electricity_consumption=10, number_of_rack_units=1)
    d2 = DummyDevice(name="d2", electricity_consumption=20, number_of_rack_units=2)

    result = order_devices_per_power_and_units(racks, [d1, d2])

    assert set(result) == {d1, d2}


################################################################
# CHOOSE BEST RACK FOR DEVICE
################################################################
def test_choose_best_rack_returns_none_when_no_rack_can_store(monkeypatch):
    racks = [DummyRack(id=1), DummyRack(id=2)]
    device = DummyDevice(electricity_consumption=50)

    def fake_can_store(*, rack, device, used_units, used_energy):
        return False

    def fake_extend(*, racks, used_energy_by_rack, candidate_rack_id, device_energy):
        raise AssertionError("extend should not be called if cannot store")

    monkeypatch.setattr(services, "_can_store_device_in_rack", fake_can_store)
    monkeypatch.setattr(services, "_calculate_extend_after_placement", fake_extend)

    used_units_by_rack = {1: 0, 2: 0}
    used_energy_by_rack = {1: 0, 2: 0}

    result = _choose_best_rack_for_device(
        racks=racks,
        device=device,
        used_units_by_rack=used_units_by_rack,
        used_energy_by_rack=used_energy_by_rack,
    )

    assert result is None


def test_choose_best_rack_picks_rack_with_smallest_extend(monkeypatch):
    racks = [DummyRack(id=1), DummyRack(id=2), DummyRack(id=3)]
    device = DummyDevice(electricity_consumption=50)

    def fake_can_store(*, rack, device, used_units, used_energy):
        return True

    extend_by_rack_id = {1: 10, 2: 3, 3: 7}

    def fake_extend(*, racks, used_energy_by_rack, candidate_rack_id, device_energy):
        return extend_by_rack_id[candidate_rack_id]

    monkeypatch.setattr(services, "_can_store_device_in_rack", fake_can_store)
    monkeypatch.setattr(services, "_calculate_extend_after_placement", fake_extend)

    used_units_by_rack = {1: 0, 2: 0, 3: 0}
    used_energy_by_rack = {1: 0, 2: 0, 3: 0}

    result = _choose_best_rack_for_device(
        racks=racks,
        device=device,
        used_units_by_rack=used_units_by_rack,
        used_energy_by_rack=used_energy_by_rack,
    )

    assert result.id == 2


def test_choose_best_rack_skips_racks_that_cannot_store(monkeypatch):
    racks = [DummyRack(id=1), DummyRack(id=2)]
    device = DummyDevice(electricity_consumption=50)

    def fake_can_store(*, rack, device, used_units, used_energy):
        return rack.id == 2

    def fake_extend(*, racks, used_energy_by_rack, candidate_rack_id, device_energy):
        assert candidate_rack_id == 2
        return 999

    monkeypatch.setattr(services, "_can_store_device_in_rack", fake_can_store)
    monkeypatch.setattr(services, "_calculate_extend_after_placement", fake_extend)

    used_units_by_rack = {1: 0, 2: 0}
    used_energy_by_rack = {1: 0, 2: 0}

    result = _choose_best_rack_for_device(
        racks=racks,
        device=device,
        used_units_by_rack=used_units_by_rack,
        used_energy_by_rack=used_energy_by_rack,
    )

    assert result.id == 2


def test_choose_best_rack_tie_breaker_keeps_first_with_min_extend(monkeypatch):
    racks = [DummyRack(id=1), DummyRack(id=2)]
    device = DummyDevice(electricity_consumption=50)

    def fake_can_store(*, rack, device, used_units, used_energy):
        return True

    def fake_extend(*, racks, used_energy_by_rack, candidate_rack_id, device_energy):
        return 5

    monkeypatch.setattr(services, "_can_store_device_in_rack", fake_can_store)
    monkeypatch.setattr(services, "_calculate_extend_after_placement", fake_extend)

    used_units_by_rack = {1: 0, 2: 0}
    used_energy_by_rack = {1: 0, 2: 0}

    result = _choose_best_rack_for_device(
        racks=racks,
        device=device,
        used_units_by_rack=used_units_by_rack,
        used_energy_by_rack=used_energy_by_rack,
    )

    assert result.id == 1


################################################################
# CALCULATE EXTEND AFTER PLACEMENT
################################################################
def test_calculate_extend_after_placement_returns_difference_between_max_and_min_utilization():
    racks = [
        DummyRack(id=1, max_electricity_sustained=100),
        DummyRack(id=2, max_electricity_sustained=100),
    ]
    used_energy_by_rack = {1: 0, 2: 50}

    result = _calculate_extend_after_placement(
        racks=racks,
        used_energy_by_rack=used_energy_by_rack,
        candidate_rack_id=1,
        device_energy=50,
    )

    assert result == 0


def test_calculate_extend_after_placement_increases_extend_when_it_creates_imbalance():
    racks = [
        DummyRack(id=1, max_electricity_sustained=100),
        DummyRack(id=2, max_electricity_sustained=100),
    ]
    used_energy_by_rack = {1: 0, 2: 50}

    result = _calculate_extend_after_placement(
        racks=racks,
        used_energy_by_rack=used_energy_by_rack,
        candidate_rack_id=2,
        device_energy=50,
    )

    assert result == 100


def test_calculate_extend_after_placement_handles_different_max_per_rack():
    racks = [
        DummyRack(id=1, max_electricity_sustained=200),
        DummyRack(id=2, max_electricity_sustained=100),
    ]
    used_energy_by_rack = {1: 100, 2: 0}

    result = _calculate_extend_after_placement(
        racks=racks,
        used_energy_by_rack=used_energy_by_rack,
        candidate_rack_id=2,
        device_energy=50,
    )

    assert result == 0


def test_calculate_extend_after_placement_works_with_single_rack():
    racks = [DummyRack(id=1, max_electricity_sustained=100)]
    used_energy_by_rack = {1: 20}

    result = _calculate_extend_after_placement(
        racks=racks,
        used_energy_by_rack=used_energy_by_rack,
        candidate_rack_id=1,
        device_energy=10,
    )

    assert result == 0


################################################################
# CAN STORE DEVICE IN RACK
################################################################
def test_can_store_device_in_rack_returns_true_when_fits_units_and_energy():
    rack = DummyRack(total_units=10, max_electricity_sustained=100)
    device = DummyDevice(number_of_rack_units=3, electricity_consumption=20)

    result = _can_store_device_in_rack(
        rack=rack,
        device=device,
        used_units=5,
        used_energy=70,
    )

    assert result is True


def test_can_store_device_in_rack_returns_false_when_units_exceed_total():
    rack = DummyRack(total_units=10, max_electricity_sustained=100)
    device = DummyDevice(number_of_rack_units=6, electricity_consumption=10)

    result = _can_store_device_in_rack(
        rack=rack,
        device=device,
        used_units=5,
        used_energy=0,
    )

    assert result is False


def test_can_store_device_in_rack_returns_false_when_energy_exceeds_max():
    rack = DummyRack(total_units=10, max_electricity_sustained=100)
    device = DummyDevice(number_of_rack_units=1, electricity_consumption=40)

    result = _can_store_device_in_rack(
        rack=rack,
        device=device,
        used_units=0,
        used_energy=70,
    )

    assert result is False


def test_can_store_device_in_rack_allows_exact_fit_units_and_energy():
    rack = DummyRack(total_units=10, max_electricity_sustained=100)
    device = DummyDevice(number_of_rack_units=5, electricity_consumption=30)

    result = _can_store_device_in_rack(
        rack=rack,
        device=device,
        used_units=5,
        used_energy=70,
    )

    assert result is True


################################################################
# SUGGEST ALGORITHM
################################################################
def test_suggest_algorithm_for_rack_assigns_devices_updates_usage_and_collects_unassigned(monkeypatch):
    racks = [DummyRack(id=1), DummyRack(id=2)]

    d1 = DummyDevice(name="d1", electricity_consumption=10, number_of_rack_units=1)
    d2 = DummyDevice(name="d2", electricity_consumption=30, number_of_rack_units=3)
    d3 = DummyDevice(name="d3", electricity_consumption=50, number_of_rack_units=5)

    def fake_ordering(racks_, devices_):
        return [d1, d2, d3]

    def fake_choose_best(*, racks, device, used_units_by_rack, used_energy_by_rack):
        if device.name == "d1":
            return racks[0]
        if device.name == "d2":
            return racks[1]
        return None

    monkeypatch.setattr(services, "order_devices_per_power_and_units", fake_ordering)
    monkeypatch.setattr(services, "_choose_best_rack_for_device", fake_choose_best)

    assigned, used_energy, used_units, unassigned = suggest_algorithm_for_rack(
        racks=racks,
        devices=[d3, d2, d1],
    )

    assert unassigned == [d3]

    assert assigned[1] == [d1]
    assert assigned[2] == [d2]

    assert used_energy == {1: 10, 2: 30}
    assert used_units == {1: 1, 2: 3}
