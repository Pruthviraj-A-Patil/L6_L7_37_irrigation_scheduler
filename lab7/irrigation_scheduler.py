
import math


def parse_zone(text):
    if not isinstance(text, str):
        raise ValueError("Zone input must be a string")

    if text.count(":") != 1:
        raise ValueError("Input must contain exactly one colon")

    name, area = text.split(":")

    name = name.strip()

    if not name:
        raise ValueError("Zone name cannot be empty")

    try:
        area = float(area.strip())
    except ValueError:
        raise ValueError("Area must be a valid number")

    if not math.isfinite(area) or area < 0:
        raise ValueError("Area must be finite and non-negative")

    return name.title(), area


def moisture_average(readings_csv):
    if not isinstance(readings_csv, str):
        raise ValueError("Readings must be a string")

    if not readings_csv.strip():
        raise ValueError("Readings cannot be empty")

    parts = readings_csv.split(",")

    values = []

    for reading in parts:
        reading = reading.strip()

        if not reading:
            raise ValueError("Empty moisture reading")

        try:
            value = int(reading)
        except ValueError:
            raise ValueError("Moisture readings must be integers")

        if value < 0 or value > 100:
            raise ValueError("Moisture must be between 0 and 100")

        values.append(value)

    return sum(values) // len(values)


def water_needed(text):
    if not isinstance(text, str):
        raise ValueError("Water input must be a string")

    if text.count("|") != 1:
        raise ValueError("Input must contain exactly one pipe")

    plot, rain = text.split("|")

    try:
        area = float(plot.strip())
        rainfall = float(rain.strip())
    except ValueError:
        raise ValueError("Area and rainfall must be valid numbers")

    if not math.isfinite(area) or not math.isfinite(rainfall):
        raise ValueError("Values must be finite")

    if area < 0 or rainfall < 0:
        raise ValueError("Area and rainfall cannot be negative")

    need = area * 5 - rainfall

    return max(need, 0)


def main():
    print("==== Running parse_zone ====")
    user_input = input("Enter zone:area in m2 (e.g. north:120): ")
    result = parse_zone(user_input)
    print("Zone and Area:", result)

    print("\n==== Running moisture_average ====")
    user_input = input("Enter moisture readings as CSV (e.g. 40,35,50): ")
    result = moisture_average(user_input)
    print("Average Moisture:", result)

    print("\n==== Running water_needed ====")
    user_input = input("Enter area|rainfall (e.g. 120|8): ")
    result = water_needed(user_input)
    print("Water Needed:", result)


if __name__ == "__main__":
    main()
