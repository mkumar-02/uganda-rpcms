# RPCMS Partner Onboarding

Custom partner lifecycle for Uganda RPCMS: **Verify → MoU → Approve → provision** Registry Agent + PBMS Agency/Program + Locations.

Staff portal uses OpenG2P AppShell / brand tokens (same look as other OpenG2P staff UIs).

## Layout

```text
ngo/
├── backend/          # FastAPI: openg2p_rpcms_ngo_api
├── ui/               # Next.js staff portal
├── docker/
│   ├── staff-api/
│   └── staff-ui/
└── docs/
```

## Gate order

1. **Verify** — URSB + NGO Bureau adapters (stubs today; swap for live bureaus)
2. **MoU** — attach document + mark signed (UGPass e-sign later)
3. **Approve** — staff / AWE decision
4. **Provision** — stub IDs for Registry Agent, PBMS Agency, PBMS Program; locations managed on the partner record

## Local API

```bash
cd ngo/backend
cp .env.example .env   # edit DB credentials
pip install -e .
python -m openg2p_rpcms_ngo_api.main migrate
python -m openg2p_rpcms_ngo_api.main
```

## Local UI

```bash
cd ngo/ui
cp .env.example .env.local
npm install
npm run dev
# http://localhost:3010
```

Rewrites `/api/ngo/*` → FastAPI.

## Docker

```bash
cd ngo
docker build -f docker/staff-api/Dockerfile .
docker build -f docker/staff-ui/Dockerfile ./ui
```

## Docs

- [Partner-Onboarding.md](docs/Partner-Onboarding.md)
- [Architecture](../docs/RPCMS-OpenG2P-Architecture.md)
