# Partner Onboarding Module

## Purpose

Onboard a refugee-assistance partner so it can:

1. Act as a **Registry Agent** (intake / surveys)
2. Operate as a **PBMS Agency** with one or more **Programs**
3. Serve defined **Locations** (settlement / zone / service point)
4. Do so only after **compliance verification** and a signed **MoU**

This is the custom layer described in the [RPCMS architecture](../../docs/RPCMS-OpenG2P-Architecture.md) §5.6.

## Gate order

```text
Apply  →  Verify (URSB + NGO Bureau)  →  MoU signed  →  Approve  →  Provision
```

| Step | Request status | Partner status | Downstream |
|------|----------------|----------------|------------|
| Apply | `created` | `pending_compliance` | — |
| Verify pass | `compliance_passed` | `pending_mou` | — |
| MoU attached | `mou_attached` | `pending_approval` | — |
| Approve | `approved` | `active` | Agent + Agency + Program IDs |
| Reject | `rejected` | `rejected` | — |

## API (staff)

| Method | Path | Action |
|--------|------|--------|
| POST | `/onboard` | Create partner + onboarding request |
| GET | `/requests` | List requests |
| GET | `/requests/{id}` | Request detail |
| POST | `/requests/{id}/run-compliance` | Run URSB + NGO Bureau stubs |
| GET | `/requests/{id}/compliance` | List check results |
| POST | `/ngos/{id}/mous` | Attach MoU (`mark_signed: true` for stub sign) |
| POST | `/mous/{id}/sign` | Mark MoU signed |
| POST | `/requests/{id}/mark-mou-attached` | Advance after signed MoU |
| POST | `/requests/{id}/approve` | Approve + provision stubs |
| POST | `/requests/{id}/reject` | Reject |
| GET/PATCH | `/ngos`, `/ngos/{id}` | Partner master |
| GET/POST | `/ngos/{id}/locations` | Locations |
| DELETE | `/locations/{id}` | Remove location |

## Adapters & hooks

| Integration | Status | Config |
|-------------|--------|--------|
| URSB | Stub (`FAIL*` numbers fail) | Replace `compliance_adapters.check_ursb` |
| NGO Bureau | Stub | Replace `check_ngo_bureau` |
| UGPass e-sign | Not wired | MoU `document_uri` + `sign` |
| AWE workflow | Hook only | `rpcms_ngo_awe_enabled`, `rpcms_ngo_awe_base_url` |
| Registry Agent API | Stub IDs | `rpcms_ngo_registry_provision_enabled` |
| PBMS Agency/Program | Stub IDs | `rpcms_ngo_pbms_provision_enabled` |

## UI

Next.js App Router staff portal under `ngo/ui`:

- Dark sidebar AppShell + OpenG2P logo
- Roboto / Roboto Slab + brand yellow accent
- Pages: Requests, Request detail (workflow), Partners, Partner detail (locations), Onboard

Demo auth (`opm.staff`) until Keycloak staff realm is shared with other portals.
