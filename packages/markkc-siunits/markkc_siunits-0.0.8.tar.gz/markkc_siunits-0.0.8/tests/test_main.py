from src.markkc_siunits import SiUnits


def test_parser():
    si = SiUnits(
        units=["Ω", "A", "V"],
        unit_alternatives={"R": "Ω"}
    )
    assert si.parse_value_and_unit("47kΩ") == (47e3, "Ω")
    assert si.parse_value_and_unit("47 kR") == (47e3, "Ω")
    assert si.parse_value_and_unit("47.00 kR") == (47e3, "Ω")
    assert si.parse_value_and_unit("47e+3Ω") == (47e3, "Ω")
    assert si.parse_value_and_unit("2.4 A") == (2.4, "A")
    assert si.parse_value_and_unit("150kV") == (150e3, "V")
    assert si.parse_value_and_unit("0.022R") == (22e-3, "Ω")
    assert si.parse_value_and_unit("15mΩ") == (15e-3, "Ω")
    assert si.parse_value_and_unit("6e-3R") == (6e-3, "Ω")


def test_formatter():
    si = SiUnits(
        units=["W"],
    )
    assert si.format_value(0.002012) == "2.01 mW"
    assert si.format_value(0.02012) == "20.1 mW"
    assert si.format_value(0.2012) == "201 mW"
    assert si.format_value(2.012) == "2.01 W"
    assert si.format_value(20.12) == "20.1 W"
    assert si.format_value(201.2) == "201 W"
    assert si.format_value(2012) == "2.01 kW"
    si = SiUnits(
        units=["W", "J", "N"],
    )
    assert si.format_value(20.18) == "20.2"
    assert si.format_value(2018) == "2.02 k"
    assert si.format_value(20.18, "N") == "20.2 N"
    assert si.format_value(2018, "N") == "2.02 kN"
    assert si.format_value(20.18e6) == "20.2 M"
