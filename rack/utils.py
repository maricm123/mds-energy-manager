

def calculate_average_rack_max_energy(racks):
    total = 0
    count = 0

    for rack in racks:
        total += rack.max_electricity_sustained
        count += 1

    return total / count


def calculate_average_rack_max_units(racks):
    total = 0
    count = 0

    for rack in racks:
        total += rack.max_electricity_sustained
        count += 1

    return total / count


def calculate_power_utilization_percent(rack, used_energy):
    if rack.max_electricity_sustained <= 0:
        return 0.0
    return (used_energy / rack.max_electricity_sustained) * 100
