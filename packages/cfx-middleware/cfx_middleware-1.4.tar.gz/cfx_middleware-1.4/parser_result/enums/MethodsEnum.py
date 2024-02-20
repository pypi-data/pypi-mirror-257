from enum import Enum


class Methods(Enum):
    validate_units = "validate_units"
    units_inspected = "units_inspected"
    units_departed = "units_departed"
    state_change = "state_change"
