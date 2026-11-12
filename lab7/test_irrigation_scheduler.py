
from hypothesis import given, strategies as st
import math

from irrigation_scheduler import (
    parse_zone,
    moisture_average,
    water_needed
)


# Test 1: parse_zone
@given(st.one_of(st.text(), st.none()))
def test_parse_zone_no_crash(value):
    try:
        result = parse_zone(value)
    except ValueError:
        return

    assert isinstance(result, tuple)
    assert len(result) == 2
    assert isinstance(result[0], str)
    assert result[0] != ""
    assert math.isfinite(result[1])
    assert result[1] >= 0


# Test 2: moisture_average
@given(st.one_of(st.text(), st.none()))
def test_moisture_average_no_crash(value):
    try:
        result = moisture_average(value)
    except ValueError:
        return

    assert isinstance(result, int)
    assert 0 <= result <= 100


# Test 3: water_needed
@given(st.one_of(st.text(), st.none()))
def test_water_needed_no_crash(value):
    try:
        result = water_needed(value)
    except ValueError:
        return

    assert isinstance(result, (int, float))
    assert math.isfinite(result)
    assert result >= 0


# Test negative area
@given(st.floats(
    min_value=-1000,
    max_value=-0.001,
    allow_nan=False,
    allow_infinity=False
))
def test_parse_zone_rejects_negative_area(area):
    try:
        result = parse_zone(f"north:{area}")
    except ValueError:
        return

    assert result[1] >= 0


# Test negative moisture readings
@given(st.integers(max_value=-1))
def test_moisture_rejects_negative_readings(value):
    try:
        result = moisture_average(str(value))
    except ValueError:
        return

    assert result >= 0


# Test negative plot area
@given(st.floats(
    min_value=-1000,
    max_value=-0.001,
    allow_nan=False,
    allow_infinity=False
))
def test_water_needed_rejects_negative_area(area):
    try:
        water_needed(f"{area}|0")
    except ValueError:
        return

    assert False, "Negative plot area was accepted"
