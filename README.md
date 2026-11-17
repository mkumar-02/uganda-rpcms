# Uganda RPCMS (OpenG2P)

Refugee Partnership Coordination & Monitoring System for the Office of the Prime Minister · Department of Refugees, implemented on **OpenG2P**.

## Documentation

- [Architecture baseline](docs/RPCMS-OpenG2P-Architecture.md)
- [Refugee Registry](registry/README.md) — extension layout, registers, Docker/Helm
- [Registry extension details](registry/docs/Registry-Refugee-Extension.md)
- [Partner onboarding](ngo/README.md) — verify · MoU · approve · provision
- [PBMS](pbms/README.md) — agency/program cycles; Refugee + Household adapters
- [IBR](ibr/README.md) — **paused** (awaiting design)

## Stack (agreed)

| Component | Role |
|-----------|------|
| Registry | Refugee registration, survey/intake forms, agents → `registry/` |
| PBMS | Agencies, programs, locations, cycles, entitlements → `pbms/` |
| IBR | Cross-agency double-dipping checks → `ibr/` (**paused**) |
| G2P Bridge | Govt → agency → beneficiary + POD (physical cash) |
| Partner onboarding | Verification, MoU, agent/agency/program setup → `ngo/` |
| Superset | Dashboards |

## Repository layout

```text
uganda-rpcms/
├── docs/                 # Cross-cutting architecture
├── registry/             # OpenG2P Registry refugee extension
├── ngo/                  # Partner onboarding (API + staff UI)
├── pbms/                 # PBMS connectors-style extension
├── ibr/                  # IBR (paused — design pending)
└── README.md
```

```bash
# Registry
cd registry && pip install -e ./refugee-extension
export REGISTRY_EXTENSION_MODULE=openg2p_registry_refugee_extension

# Partner onboarding API + UI
cd ngo/backend && pip install -e .
cd ../ui && npm install && NGO_API_ORIGIN=http://127.0.0.1:8000 npm run dev

# PBMS images (context = pbms/)
cd pbms && docker build -f docker/odoo/Dockerfile .
```

ID renewal booking is parked for a later phase.

## Upstream references

- https://github.com/OpenG2P/registry-platform
- https://github.com/OpenG2P/farmer-registry
- https://github.com/OpenG2P/pbms
- https://github.com/OpenG2P/pbms-connectors
- https://github.com/OpenG2P/awe
