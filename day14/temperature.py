def convert_temperature(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value

    if from_unit == "C":
        if value < -273.15:
            raise ValueError("Temperature below absolute zero")
        if to_unit == "F":
            return (value * 9/5) + 32
        if to_unit == "K":
            return value + 273.15

    elif from_unit == "F":
        if value < -459.67:
            raise ValueError("Temperature below absolute zero")
        if to_unit == "C":
            return (value - 32) * 5/9
        if to_unit == "K":
            return ((value - 32) * 5/9) + 273.15

    elif from_unit == "K":
        if value < 0:
            raise ValueError("Temperature below absolute zero")
        if to_unit == "C":
            return value - 273.15
        if to_unit == "F":
            return ((value - 273.15) * 9/5) + 32

    raise ValueError("Invalid unit")
