import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rack.models.rack import Rack
from device.models.device import Device


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_suggest_algorithm_returns_assignment_and_unassigned(api_client):
    url = reverse("api-mds:suggest-algorithm")

    rack1 = Rack.objects.create(
        name="Rack 1",
        description="",
        serial_number="RACK-1",
        total_units=10,
        max_electricity_sustained=100,
    )
    rack2 = Rack.objects.create(
        name="Rack 2",
        description="",
        serial_number="RACK-2",
        total_units=10,
        max_electricity_sustained=100,
    )

    device1 = Device.objects.create(
        name="Device 1",
        description="",
        serial_number="DEV-1",
        number_of_rack_units=10,
        electricity_consumption=10,
    )
    device2 = Device.objects.create(
        name="Device 2",
        description="",
        serial_number="DEV-2",
        number_of_rack_units=1,
        electricity_consumption=10,
    )
    device3 = Device.objects.create(
        name="Device 3",
        description="",
        serial_number="DEV-3",
        number_of_rack_units=11,
        electricity_consumption=10,
    )

    payload = {
        "rack_ids": [rack1.id, rack2.id],
        "device_ids": [device1.id, device2.id, device3.id],
    }

    response = api_client.post(url, payload, format="json")

    assert response.status_code == 200
    data = response.json()

    assert "racks" in data
    assert "unassigned_devices" in data

    assert len(data["racks"]) == 2

    rack_items_by_id = {item["rack"]["id"]: item for item in data["racks"]}

    assert rack1.id in rack_items_by_id
    assert rack2.id in rack_items_by_id

    rack1_item = rack_items_by_id[rack1.id]
    rack2_item = rack_items_by_id[rack2.id]

    rack1_device_ids = [d["id"] for d in rack1_item["devices"]]
    rack2_device_ids = [d["id"] for d in rack2_item["devices"]]

    assert rack1_device_ids == [device1.id]
    assert rack2_device_ids == [device2.id]

    assert rack1_item["units_used"] == 10
    assert rack2_item["units_used"] == 1

    assert rack1_item["total_power_used"] == 10
    assert rack2_item["total_power_used"] == 10

    assert rack1_item["power_utilization_percent"] == pytest.approx(10.0)
    assert rack2_item["power_utilization_percent"] == pytest.approx(10.0)

    unassigned_ids = [d["id"] for d in data["unassigned_devices"]]
    assert unassigned_ids == [device3.id]


@pytest.mark.django_db
def test_suggest_algorithm_rejects_duplicate_rack_ids(api_client):
    url = reverse("api-mds:suggest-algorithm")

    payload = {
        "rack_ids": [1, 1],
        "device_ids": [1],
    }

    response = api_client.post(url, payload, format="json")

    assert response.status_code == 400
    data = response.json()
    assert "rack_ids" in data
    assert "Duplicate rack ids not allowed." in str(data["rack_ids"])


@pytest.mark.django_db
def test_suggest_algorithm_rejects_duplicate_device_ids(api_client):
    url = reverse("api-mds:suggest-algorithm")

    payload = {
        "rack_ids": [1],
        "device_ids": [2, 2],
    }

    response = api_client.post(url, payload, format="json")

    assert response.status_code == 400
    data = response.json()
    assert "device_ids" in data
    assert "Duplicate device ids not allowed." in str(data["device_ids"])


@pytest.mark.django_db
def test_suggest_algorithm_rejects_empty_lists(api_client):
    url = reverse("api-mds:suggest-algorithm")

    payload = {
        "rack_ids": [],
        "device_ids": [],
    }

    response = api_client.post(url, payload, format="json")

    assert response.status_code == 400
    data = response.json()

    assert "rack_ids" in data
    assert "device_ids" in data
