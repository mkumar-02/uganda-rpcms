# OpenG2P Registry Refugee Extension (Uganda RPCMS)

Domain extension for the [OpenG2P Registry Platform](https://github.com/OpenG2P/registry-platform), modelled on the [Farmer Registry](https://github.com/OpenG2P/farmer-registry) extension pattern.

Used by Uganda **RPCMS** for refugee registration, household roster, and self-reliance survey intake. ProGres v4 authentication (Yes/No only) is a separate adapter — not part of this package’s demographic model.

## Registers

| Mnemonic | Table | Extends | Purpose |
|---|---|---|---|
| `Household` | `g2p_register_households` | `G2PRegister`, `G2PGeo` | Refugee household |
| `Refugee` | `g2p_register_refugees` | `G2PRegister`, `G2PPerson`, `G2PGeo` | Primary refugee registrant (holds ProGres ID) |
| `HouseholdMember` | `g2p_register_household_members` | `G2PRegister`, `G2PPerson`, `G2PGeo` | Household roster |
| `SelfRelianceSurvey` | `g2p_register_self_reliance_surveys` | `G2PRegister` | Survey rounds (intake-style), linked to household |

Every register has `*_history` and `g2p_intake_form_*` twins.

## Install (from source)

```bash
# from repo root
pip install -e ./registry/refugee-extension/

# or from registry/
pip install -e ./refugee-extension/
```

At runtime set:

```bash
export REGISTRY_EXTENSION_MODULE=openg2p_registry_refugee_extension
```

See [../README.md](../README.md) for Docker/Helm layout.

## Notes

- `progres_id` is stored on the Refugee (and optionally on members). Authentication against ProGres v4 is **out of band** (auth adapter); this registry does not import ProGres demographics.
- Self-reliance survey uses the same intake-form pattern as registration.
- ID renewal booking is **parked** (see project architecture doc).
