
import pytest
from irrigation_scheduler import should_irrigate, water_volume, schedule


# ==========================================
# BRANCH TESTS: should_irrigate()
# ==========================================

def test_moisture_above_threshold():
    assert should_irrigate(60, 0, "seedling") is False


def test_rainfall_at_heavy_threshold():
    assert should_irrigate(30, 10, "seedling") is False


def test_seedling_moisture_below_45():
    assert should_irrigate(44, 0, "seedling") is True


def test_seedling_moisture_at_45():
    assert should_irrigate(45, 0, "seedling") is False


def test_flowering_moisture_below_55():
    assert should_irrigate(54, 0, "flowering") is True


def test_flowering_moisture_at_55():
    assert should_irrigate(55, 0, "flowering") is False


def test_other_stage_rainfall_at_5():
    assert should_irrigate(30, 5, "other") is False


def test_other_stage_rainfall_below_5():
    assert should_irrigate(30, 4, "other") is True


def test_other_stage_moisture_below_40():
    assert should_irrigate(39, 0, "other") is True


def test_other_stage_moisture_at_40():
    assert should_irrigate(40, 0, "other") is False


# ==========================================
# BRANCH TESTS: water_volume()
# ==========================================

def test_area_zero():
    with pytest.raises(ValueError):
        water_volume(0, "seedling", 20)


def test_area_negative():
    with pytest.raises(ValueError):
        water_volume(-5, "seedling", 20)


def test_seedling_stage():
    assert water_volume(10, "seedling", 20) == 20


def test_flowering_stage():
    assert water_volume(10, "flowering", 20) == 50


def test_other_stage():
    assert water_volume(10, "other", 20) == 40


def test_temperature_above_35():
    assert water_volume(10, "seedling", 36) == 30


def test_temperature_at_35():
    assert water_volume(10, "seedling", 35) == 20


def test_temperature_below_10():
    assert water_volume(10, "seedling", 9) == 10


def test_temperature_at_10():
    assert water_volume(10, "seedling", 10) == 20


# ==========================================
# BRANCH TESTS: schedule()
# ==========================================

def test_empty_schedule():
    assert schedule([], 100) == []


def test_schedule_skips_irrigation_zone():
    zones = [
        ("Zone-A", 10, 70, 0, "seedling", 20)
    ]
    assert schedule(zones, 100) == []


def test_schedule_adds_irrigation_zone():
    zones = [
        ("Zone-A", 10, 30, 0, "seedling", 20)
    ]
    assert schedule(zones, 100) == ["Zone-A"]


def test_schedule_budget_exactly_sufficient():
    zones = [
        ("Zone-A", 10, 30, 0, "seedling", 20)
    ]
    assert schedule(zones, 20) == ["Zone-A"]


def test_schedule_stops_when_budget_insufficient():
    zones = [
        ("Zone-A", 10, 30, 0, "seedling", 20),
        ("Zone-B", 10, 30, 0, "seedling", 20)
    ]
    assert schedule(zones, 25) == ["Zone-A"]


def test_schedule_multiple_zones():
    zones = [
        ("Zone-A", 10, 30, 0, "seedling", 20),
        ("Zone-B", 5, 30, 0, "seedling", 20)
    ]
    assert schedule(zones, 50) == ["Zone-A", "Zone-B"]
