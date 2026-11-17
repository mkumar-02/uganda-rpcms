# Uganda RPCMS — Refugee Registry

OpenG2P Registry domain for refugees, households, and self-reliance surveys.  
Follows the [farmer-registry](https://github.com/OpenG2P/farmer-registry) inverted-build pattern on [registry-platform](https://github.com/OpenG2P/registry-platform).

## Layout

```text
registry/
├── refugee-extension/     # pip package: openg2p_registry_refugee_extension
│   └── src/.../meta_data/ # register defs, sections, intake forms, AWE, languages
├── docker/                # thin images FROM openg2p/openg2p-registry-*
├── helm/openg2p-refugee-registry/
└── docs/
```

## Registers

| Mnemonic | Purpose |
|----------|---------|
| `Household` | Master household (settlement / zone) |
| `Refugee` | Primary registrant + **ProGres ID** |
| `HouseholdMember` | Household roster |
| `SelfRelianceSurvey` | Survey rounds (intake-style) |

**Auth ≠ registration:** ProGres v4 Yes/No authentication is a separate adapter. This package stores allowed intake attributes + `progres_id` only.

## Install extension locally

```bash
cd registry
pip install -e ./refugee-extension
export REGISTRY_EXTENSION_MODULE=openg2p_registry_refugee_extension
```

## Docker (build context = `registry/`)

```bash
cd registry
docker build -f docker/staff-api/Dockerfile .
docker build -f docker/agent-portal-api/Dockerfile .
docker build -f docker/partner-api/Dockerfile .
docker build -f docker/celery/Dockerfile .
```

Pin `RP_VERSION` in each Dockerfile to the registry-platform base tag you deploy.

## Helm

```bash
helm dependency build ./registry/helm/openg2p-refugee-registry
helm install refugee-registry ./registry/helm/openg2p-refugee-registry
```

## Docs

- [Registry-Refugee-Extension.md](docs/Registry-Refugee-Extension.md) — package details  
- [../docs/RPCMS-OpenG2P-Architecture.md](../docs/RPCMS-OpenG2P-Architecture.md) — full RPCMS architecture  
