
import pytest
from irrigation_scheduler import should_irrigate, water_volume, schedule


# ==========================================
# TEST CASES FOR should_irrigate()
# ==========================================

def test_wet_soil():
    assert should_irrigate(70, 0, "seedling") is False


def test_heavy_rainfall():
    assert should_irrigate(40, 10, "seedling") is False


def test_seedling_low_moisture():
    assert should_irrigate(30, 0, "seedling") is True


def test_seedling_sufficient_moisture():
    assert should_irrigate(50, 0, "seedling") is False


def test_flowering_low_moisture():
    assert should_irrigate(40, 0, "flowering") is True


def test_flowering_high_moisture():
    assert should_irrigate(55, 0, "flowering") is False


def test_moderate_rainfall():
    assert should_irrigate(35, 5, "other") is False


def test_other_stage_low_moisture():
    assert should_irrigate(30, 0, "other") is True


def test_other_stage_sufficient_moisture():
    assert should_irrigate(40, 0, "other") is False


# ==========================================
# TEST CASES FOR water_volume()
# ==========================================

def test_invalid_area():
    with pytest.raises(ValueError, match="invalid area"):
        water_volume(0, "seedling", 20)


def test_seedling_water_volume():
    assert water_volume(10, "seedling", 20) == 20


def test_flowering_water_volume():
    assert water_volume(10, "flowering", 20) == 50


def test_other_stage_water_volume():
    assert water_volume(10, "other", 20) == 40


def test_high_temperature_adjustment():
    assert water_volume(10, "seedling", 40) == 30


def test_low_temperature_adjustment():
    assert water_volume(10, "seedling", 5) == 10


def test_normal_temperature():
    assert water_volume(10, "seedling", 20) == 20


# ==========================================
# TEST CASES FOR schedule()
# ==========================================

def test_schedule_skips_zone():
    zones = [
        ("Zone-A", 10, 70, 0, "seedling", 20)
    ]
    assert schedule(zones, 100) == []


def test_schedule_adds_zone():
    zones = [
        ("Zone-A", 10, 30, 0, "seedling", 20)
    ]
    assert schedule(zones, 100) == ["Zone-A"]


def test_schedule_insufficient_budget():
    zones = [
        ("Zone-A", 10, 30, 0, "seedling", 20)
    ]
    assert schedule(zones, 15) == []


def test_schedule_multiple_zones():
    zones = [
        ("Zone-A", 10, 30, 0, "seedling", 20),
        ("Zone-B", 5, 30, 0, "seedling", 20)
    ]
    assert schedule(zones, 50) == ["Zone-A", "Zone-B"]


def test_schedule_stops_when_budget_exceeded():
    zones = [
        ("Zone-A", 10, 30, 0, "seedling", 20),
        ("Zone-B", 10, 30, 0, "seedling", 20)
    ]
    assert schedule(zones, 25) == ["Zone-A"]
