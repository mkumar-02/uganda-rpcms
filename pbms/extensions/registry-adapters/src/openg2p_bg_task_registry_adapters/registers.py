"""Every register the adapters serve, mapped to its (DB, DCI) computations.

Each register also needs a block in the wrapper chart's values.yaml and
questions.own.yaml; test/test_register_config.py keeps them in step.
"""

from .computations import (
    HouseholdDB,
    HouseholdDCI,
    RefugeeDB,
    RefugeeDCI,
)
from .models import G2PRegistryType

REGISTERS = {
    G2PRegistryType.REFUGEE.value: (RefugeeDB, RefugeeDCI),
    G2PRegistryType.HOUSEHOLD.value: (HouseholdDB, HouseholdDCI),
}
