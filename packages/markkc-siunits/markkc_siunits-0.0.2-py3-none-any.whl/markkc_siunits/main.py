#!/usr/bin/env python

from typing import Dict, List, Optional, Tuple
from math import pow, log10, floor
import re
from functools import cached_property


class SiUnits():

    @cached_property
    def prefix_list(self) -> List[Tuple[str, int, bool]]:
        return sorted(
            [
                (char.strip(), 3 * (index - 8), False)
                for index, char in enumerate("yzafpnμm kMGTPEZY")
                # Don't bother with the new q/r/Q/R prefixes, we already have far wider
                # range than we'll practically need and the "R" one clashes with the "R"
                # latin-alternative for Ω (Ohm) unit
            ] + [
                ("u", -6, True),
                ("c", -2, True),
                ("d", -1, True),
                ("da", 1, True),
                ("D", 1, True),  # "da" prefix, but single-char
                ("h", 2, True),
            ],
            key=lambda item: (item[2], item[1])
        )

    @cached_property
    def prefix_alternatives(self) -> Dict[str, str]:
        return {
            "u": "μ"
        }

    @property
    def format_with_space(self) -> bool:
        return True

    @cached_property
    def si_prefixes(self):
        return {
            char: exponent
            for char, exponent, _ in self.prefix_list
        }

    @cached_property
    def value_regex(self):
        def group(name, expr):
            return f"(?P<{name}>({expr}))"
        units = set(self.units) | set(self.unit_alternatives.keys())
        radix = r"\."
        space = r"\ "
        intpart = group("intpart", r"[-+]?\d+")
        fracpart = group("fracpart", r"\d*")
        explead = group("explead", "[eE]")
        exppart = group("exppart", r"[-+]?\d+")
        prefix = group("prefix", "|".join([prefix for prefix in self.si_prefixes.keys() if prefix]))
        unit = group("unit", "|".join([re.escape(unit) for unit in units]))
        formats = {
            "scientific": f"{intpart}({radix}{fracpart})?({explead}{exppart})?{space}?{prefix}?{unit}?",
            "radix_dot": f"{intpart}({radix}{fracpart})?{space}?{prefix}?{unit}?",
            "radix_prefix": f"{intpart}({prefix}{fracpart}){space}?{unit}?",
        }
        return [
            f"^{expr}$"
            for expr in formats.values()
        ]

    def __init__(self, units: List[str] = [], unit_alternatives: Dict[str, str] = {}):
        self.units = units
        self.unit_alternatives = unit_alternatives

    def parse_value_and_unit(self, value: str) -> Tuple[float, str]:
        rx_patterns = self.value_regex
        match = None
        for rx_pattern in rx_patterns:
            rx = re.compile(rx_pattern)
            match = rx.match(value)
            if match:
                break
        if not match:
            raise ValueError(f"Invalid value: {value}")
        groups = {
            k: v
            for k, v in match.groupdict().items()
            if v is not None
        }
        number_str = groups["intpart"]
        if "fracpart" in groups:
            number_str += "." + groups["fracpart"]
        if "explead" in groups:
            number_str += "e" + groups["exppart"]
        number = float(number_str)
        prefix = groups.get("prefix", "")
        prefix = self.prefix_alternatives.get(prefix, prefix)
        exponent = self.si_prefixes[prefix]
        number = number * pow(10, exponent)
        unit = groups.get("unit", "")
        unit = self.unit_alternatives.get(unit, unit)
        return number, unit

    def parse_value(self, value: str) -> float:
        return self.parse_value_and_unit(value)[0]

    def format_value(self, value: float, unit: Optional[str] = None) -> str:
        exponent = floor(log10(value))
        if unit is None:
            if len(self.units) == 1:
                unit = self.units[0]
            else:
                unit = ""
        if abs(exponent) > 30:
            return f"{value:.2e} {unit}"
        for prefix, prefix_exponent, parse_only in reversed(self.prefix_list):
            if parse_only:
                continue
            if prefix_exponent % 3:
                continue
            if exponent >= prefix_exponent:
                break
        else:
            prefix = ""
            prefix_exponent = 0
        value = value * pow(10, -prefix_exponent)
        if value >= 100:
            value = round(value)
            fmt = "{:1.0f}"
        elif value >= 10:
            value = round(value * 10) / 10
            fmt = "{:1.1f}"
        else:
            value = round(value * 100) / 100
            fmt = "{:1.2f}"
        value_str = fmt.format(value)
        return f"{value_str} {prefix}{unit}".strip()
