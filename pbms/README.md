# Uganda RPCMS — PBMS

Programme & Beneficiary Management System for RPCMS, extended from OpenG2P **pbms** via the same inverted-build pattern as **pbms-connectors**.

Upstream:

- https://github.com/OpenG2P/pbms — platform (`*-base` images + `openg2p-pbms-platform` chart)
- https://github.com/OpenG2P/pbms-connectors — reference for registry adapters / thin Docker / Helm overlay

## What this package owns

| Path | Purpose |
|------|---------|
| `extensions/registry-adapters/` | Refugee + Household DB/DCI adapters (`progres_id`, settlement/zone) |
| `odoo/` | Registry type enum + Odoo register models/views |
| `docker/` | Thin images `FROM openg2p/openg2p-pbms-*-base` |
| `helm/openg2p-rpcms-pbms/` | Values overlay (images + `REGISTRY_ADAPTERS_*`) |
| `docs/` | RPCMS PBMS notes |

## Registers

| Type | Registry table | IBR / enrolment note |
|------|----------------|----------------------|
| `refugee` | `g2p_register_refugees` | Match on **`progres_id`** |
| `household` | `g2p_register_households` | Uganda household shape (`size_of_group`, settlement/zone) |

Core PBMS already provides **Agency**, **Program**, **admin large/small**, **cycles**, **benefit codes** (`CASH_PHYSICAL`), Bridge wizards. Partner onboarding stubs create agency/program IDs; wire live provisioning later.

## Geography convention

| RPCMS | PBMS |
|-------|------|
| Settlement | `g2p.administrative.area.large` (`area_mnemonic` = `settlement_code`) |
| Zone | `g2p.administrative.area.small` under that large |
| Partner coverage | Agency → small areas |

## Docker (build context = `pbms/`)

```bash
cd pbms
docker build -f docker/odoo/Dockerfile .
docker build -f docker/celery/Dockerfile .
docker build -f docker/staff-portal-api/Dockerfile .
```

Pin `PBMS_VERSION` with `./scripts/bump-pbms-version.sh` (lockstep with Helm platform dependency).

## Helm

```bash
helm dependency build ./pbms/helm/openg2p-rpcms-pbms
helm upgrade --install rpcms-pbms ./pbms/helm/openg2p-rpcms-pbms \
  --namespace pbms --create-namespace
```

Set `global.registers.refugee.connectionString` (and household) to the Uganda Registry DB.

## Later

- IBR pre-pay gate before entitlement / Bridge instruction
- Live partner-onboarding → `g2p.agency` / `g2p.program.definition` create
- Service-point model (today partner locations stub)

## Docs

- [PBMS-Refugee-Extension.md](docs/PBMS-Refugee-Extension.md)
- [Architecture](../docs/RPCMS-OpenG2P-Architecture.md)
