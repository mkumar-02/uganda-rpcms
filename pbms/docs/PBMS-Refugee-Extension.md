# PBMS — Refugee & Household registers (Uganda RPCMS)

## Pattern

Same as [pbms-connectors](https://github.com/OpenG2P/pbms-connectors):

1. Platform images from [pbms](https://github.com/OpenG2P/pbms) (`openg2p-pbms-*-base`)
2. This repo installs Odoo addons + `openg2p_bg_task_registry_adapters`
3. Helm chart has **no templates** — depends on `openg2p-pbms-platform` and overrides images/env

## Refugee adapter

- ORM: `G2PRefugeeRegistry` → table `g2p_register_refugees`
- Key field for IBR / matching: **`progres_id`**
- Domain fields: settlement/zone, arrival, displacement, disability flags (aligned with `registry/refugee-extension`)

## Household adapter

Uganda-shaped (not the generic connectors household):

- `household_head`, `size_of_group`, children/elderly/female/male counts
- `settlement_code`, `zone_code`

## Operational seed (manual / later automation)

1. Benefit code with type **`CASH_PHYSICAL`**
2. Program with `target_registry = refugee` (or household)
3. Admin large = settlement; admin small = zones
4. Agency linked to zones + program benefit codes
5. Point Celery/Staff env at Registry DB via `REGISTRY_ADAPTERS_REFUGEE_*`

## IBR gate (stub later)

Before entitlement issue / Bridge instruction, check:

```text
(progres_id, benefit_type, cycle_period)
```

Not in upstream PBMS today — add as an RPCMS hook when IBR lands.
