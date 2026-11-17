# RPCMS on OpenG2P — Architecture & Implementation Baseline

**Product:** Refugee Partnership Coordination & Monitoring System (RPCMS)  
**Owner context:** Office of the Prime Minister · Department of Refugees (Uganda)  
**Platform:** OpenG2P  
**Status:** Agreed baseline for implementation (locked decisions as of planning)  
**Source requirement:** `RPCMS-Refugee-Coordination-Demo` (interactive demo / season story for Bidibidi)

---

## 1. Purpose

RPCMS coordinates many partners serving refugees so that:

- Partners are verified and operate under signed MoUs
- Refugees are registered in a shared registry (with allowed attributes)
- Assistance is authenticated, paid/handed over with proof, and **not duplicated** across partners
- National reporting (dashboards, and later AMP/NIMES) can see delivery end-to-end

This document maps that requirement onto **OpenG2P building blocks** and records implementation decisions.

---

## 2. Locked decisions

| # | Topic | Decision |
|---|--------|----------|
| 1 | **ID renewal booking** | **Parked** for a later phase. Not in current implementation scope. |
| 2 | **Payout model** | NGO hands out **physical cash**. Accountability and money movement are handled **via G2P Bridge** (govt → agency → beneficiary instruction + POD). No separate “record-only” assistance path in current scope. |
| 3 | **IBR key (double dipping)** | `(ProGres ID, benefit type, cycle period)` — optional household key if household-level benefits require it. |
| 4 | **Auth vs registration** | **Different concerns.** Registration = intake into Registry. Authentication = Yes/No check that the person/ID is genuine and active (ProGres v4). Auth does **not** replace or feed full ProGres demographics into Registry. |

---

## 3. OpenG2P product cut

| Component | Role in RPCMS | Build vs reuse |
|-----------|---------------|----------------|
| **Registry** | Refugee registration, survey/intake forms, agents who register | Reuse + Uganda configuration / extensions |
| **PBMS** | Agencies (NGOs/partners), programs per agency, cycles, entitlements, locations | Reuse + extensions |
| **IBR** | Cross-agency **double-dipping** / integrated assistance check | **New** OpenG2P capability (to be built) |
| **G2P Bridge** | Govt → agency funds; agency → beneficiary cash instruction; **POD** | Reuse + cash-distribution / POD patterns |
| **Partner onboarding (custom)** | Partner lifecycle: agent, agency, program, locations, MoU, verification | Custom (workflow) |
| **Superset** | National / settlement dashboards | Reuse (analytics on Registry, PBMS, IBR, Bridge) |

**Out of current scope:** ID renewal / online refugee services booking, AMP/NIMES push (can follow once core data exists), full GIS overlap engine (locations first).

---

## 4. Requirement → OpenG2P mapping

Derived from the RPCMS demo season flow.

| Demo / requirement area | OpenG2P home | Notes |
|-------------------------|--------------|--------|
| Partner verification & compliance (URSB, NGO Bureau) | Partner onboarding | Approval workflow; creates Agent + Agency |
| e-MoU (UGPass / e-Seal) | Partner onboarding | Gate before Agency/Program active |
| Project / program registration | PBMS Program | Per agency; benefit codes & cycles |
| Funding / AMP link | Later / reference fields | Not blocking core delivery |
| GIS / service points | PBMS + location master | Admin areas + agency locations |
| Refugee registration | Registry | Partner/OPM intake; ProGres ID as functional ID when known |
| Beneficiary authentication | Auth adapter → ProGres v4 | Yes/No + txn ref only |
| Duplicate assistance check | **IBR** | Before entitlement issue / POD |
| Physical cash handover | Bridge + POD | After ProGres auth |
| Offline field capture | Field client → Registry / Bridge POD | Design with sync; detail in impl |
| Self-reliance / survey | Registry intake forms | Same pattern as registration forms |
| National dashboard | Superset | KPIs from core stores |
| ID renewal / SMS appointments | Parked | — |

---

## 5. Module responsibilities

### 5.1 Registry

**Owns:** people (individuals / households) and field intake.

| Activity | Responsibility |
|----------|----------------|
| Refugee registration | Create/update registrant with attributes the system is allowed to hold; store ProGres ID when available |
| Survey / intake forms | Configurable forms (similar to registration intake) writing attributes onto registrant/household |
| Agents | NGO (or OPM) users permitted to register and run intake |

**Does not own:** ProGres demographic dump, payment, cross-program double-dipping, MoU.

### 5.2 Authentication (adapter; used with Registry / Bridge)

| Activity | Responsibility |
|----------|----------------|
| Refugee authentication | Call ProGres v4 with ProGres ID + biometric (as supported); receive **Yes/No** + transaction reference |

**Constraint (from requirement):** No eKYC data sharing from ProGres. RPCMS/OpenG2P must not depend on name, photo, DoB, household composition, or protection history from ProGres.

### 5.3 IBR (Integrated Beneficiary Registry — new)

**Owns:** cross-agency assistance integrity.

| Activity | Responsibility |
|----------|----------------|
| Double dipping check | Given IBR key, answer whether the same benefit type was already delivered / committed for this cycle by any agency |
| Assistance event index | Record committed/paid/POD events so later checks see prior assistance |

**IBR key (locked):**

```text
progres_id + benefit_type + cycle_period
(+ household_id when benefit is household-scoped)
```

**Implementation:** `ibr/` directory reserved; **paused** until a dedicated design document is available.

### 5.4 PBMS

**Owns:** who delivers what, under which program rules.

| Activity | Responsibility |
|----------|----------------|
| Agencies | NGO / partner as delivery agency |
| Programs | One or more programs per agency (e.g. cash-for-food) |
| Locations | Link agency/program to administrative areas (large → small) and service points |
| Cycles & entitlements | Enrol from Registry; compute entitlements; approve lists |
| Pre-pay / pre-POD gate | Call **IBR** before issuing entitlement / instructing Bridge |

**Implementation:** `pbms/` — connectors-style extension on [OpenG2P pbms](https://github.com/OpenG2P/pbms) / [pbms-connectors](https://github.com/OpenG2P/pbms-connectors). Refugee + Household registry adapters (`progres_id`, settlement/zone); Agency/Program/geography/cycles remain core `g2p_pbms`. See [pbms/docs/PBMS-Refugee-Extension.md](../pbms/docs/PBMS-Refugee-Extension.md).

### 5.5 G2P Bridge

**Owns:** money movement and proof of delivery for physical cash.

| Leg | Responsibility |
|-----|----------------|
| Govt → agency | Disburse / track tranche to NGO (agency float) |
| Agency → beneficiary | Payment instruction for cash distribution (physical cash by NGO) |
| POD | Proof of delivery: authenticated handover (auth ref, amount, officer, time, GPS as applicable) |

Physical cash is compatible with Bridge: the NGO is the **cash channel**; Bridge is the **system of record** for instruction status and POD.

### 5.6 Partner onboarding (custom)

Onboards a partner as:

1. **Agent in Registry** — so the partner can register refugees / run intake & surveys  
2. **Agency + Program(s) in PBMS**  
3. **Locations** on the agency (administrative large area and small area; service points as needed)  
4. **MoU** (document + digital signature integration as required)  
5. **Verification** — approval workflow (e.g. URSB / NGO Bureau checks + OPM approval)

**Suggested gate order:** Verify → MoU signed → Agency Active → Program Active → Agents & locations enabled.

**Implementation:** `ngo/` — FastAPI staff API (`openg2p_rpcms_ngo_api`) + Next.js AppShell UI. See [ngo/docs/Partner-Onboarding.md](../ngo/docs/Partner-Onboarding.md). Compliance adapters and Registry/PBMS provisioners are stubs until bureau credentials and platform APIs are wired; AWE can replace the staff approve step via `rpcms_ngo_awe_*` config.

### 5.7 Superset

**Owns:** dashboards for OPM / settlements (partners, coverage, authenticated events, duplicates avoided, spend/POD volumes). Reads from Registry, PBMS, IBR, Bridge (not a transactional system of record).

---

## 6. Target architecture

```text
                    ┌─────────────────────────────┐
                    │  Partner onboarding         │
                    │  Verify · MoU · Approve     │
                    └─────────────┬───────────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              ▼                   ▼                   ▼
     ┌────────────────┐  ┌────────────────┐  ┌────────────────┐
     │ Registry Agent │  │ PBMS Agency    │  │ Locations      │
     └───────┬────────┘  │ + Program(s)   │  └────────────────┘
             │           └───────┬────────┘
             ▼                   │
     ┌────────────────┐          │
     │ Registry       │          │
     │ Registration + │◄─────────┘ enrol
     │ Survey intake  │
     └───────┬────────┘
             │
             ▼
     ┌────────────────┐     ┌────────────────┐
     │ PBMS           │────►│ IBR            │
     │ Cycles /       │ check│ Double dipping │
     │ Entitlements   │◄────│ (progres_id,   │
     └───────┬────────┘     │  benefit_type, │
             │              │  cycle_period) │
             ▼              └────────▲───────┘
     ┌────────────────┐              │
     │ G2P Bridge     │──────────────┘ assistance / POD events
     │ Govt→Agency→   │
     │ Beneficiary +  │
     │ POD            │
     └───────┬────────┘
             │
             │  At handover: ProGres Auth (Yes/No) then POD
             ▼
     ┌────────────────┐
     │ Superset       │
     │ Dashboards     │
     └────────────────┘
```

---

## 7. Core end-to-end flow (current scope)

### 7.1 Partner ready

1. Partner applies via partner onboarding  

2. Verification (compliance) + MoU  
3. Create Registry **Agent**, PBMS **Agency** + **Program**, attach **Locations**  
4. Program configured: benefit type, cycle recurrence, entitlement rules  

### 7.2 Refugee on Registry

1. Agent runs **registration** (and/or survey intake forms) into Registry  
2. ProGres ID captured when available (functional ID)  
3. Registrant eligible for enrolment into agency program(s)  

### 7.3 Cycle → pay → POD

1. PBMS opens cycle; enrols / refreshes beneficiaries from Registry  
2. Entitlements computed  
3. **IBR check** per entitlement key → block or flag duplicates  
4. Bridge: ensure agency funding (govt → agency) as designed  
5. Bridge: agency → beneficiary cash instructions for the cycle  
6. At distribution point:  
   - **Authenticate** with ProGres (Yes/No + ref)  
   - Hand physical cash  
   - Record **POD** on Bridge  
7. IBR updated with assistance/POD event  
8. Superset reflects coverage, duplicates avoided, POD volumes  

---

## 8. Auth vs registration (detail)

| | Registration | Authentication |
|--|--------------|----------------|
| Purpose | Create/maintain the person/household record used by programs | Prove the presenter is the holder of the ProGres ID and the record is active |
| When | Intake, updates, surveys | At payout / critical service moments |
| System | Registry | ProGres v4 adapter |
| Data stored | Allowed attributes + ProGres ID | Auth result + transaction reference (with POD / audit) |
| Not allowed | Treating ProGres as full demographic source | Assuming auth returns name/photo/DoB/household |

---

## 9. Entity sketch (implementation-oriented)

| Entity | System | Key fields (indicative) |
|--------|--------|-------------------------|
| Agent | Registry | user, organisation, roles, status |
| Registrant / Household | Registry | ids (incl. progres_id), intake attributes, location |
| Agency | PBMS | org, compliance status, MoU ref, status |
| Program | PBMS | agency_id, benefit_type(s), cycle rules, entitlement rules |
| Location | Shared / PBMS | admin hierarchy (large → small), service points, agency link |
| MoU | Custom | parties, document, signatures, status |
| Cycle / Entitlement | PBMS | program, period, beneficiary, amount |
| Assistance / IBR event | IBR | progres_id, benefit_type, cycle_period, agency/program, status |
| Payment instruction | Bridge | agency, beneficiary, amount, status |
| POD | Bridge | instruction_id, auth_ref, amount, officer, time, GPS |

---

## 10. Integrations (current vs later)

| System | Use | Phase |
|--------|-----|-------|
| UNHCR ProGres v4 | Authentication Yes/No only | Current |
| UGPass / NITA-U | MoU e-sign / e-Seal (as confirmed) | With partner onboarding |
| URSB / NGO Bureau | Partner verification | With partner onboarding |
| AMP (MoFPED) | Funding / expenditure link | Later |
| NIMES | NDP IV indicator push | Later |
| SMS / portal for ID renewal | Appointments & reminders | Parked |

---

## 11. Implementation sequencing (suggested)

1. **Foundation — Registry extension** — all under `registry/` (Household, Refugee + `progres_id`, HouseholdMember, SelfRelianceSurvey; intake forms, UI tabs, AWE hooks, Docker/Helm). See [registry/README.md](../registry/README.md).  
2. **PBMS** — agency, program, locations, cycles  
3. **Partner onboarding** — agent + agency + program + MoU + verification gates  
4. **ProGres auth adapter** — Yes/No path usable at POD  
5. **IBR** — key model + check API + event write from Bridge/PBMS  
6. **Bridge** — govt→agency, agency→beneficiary cash instructions, POD  
7. **Superset** — OPM dashboards on the above  
8. **Later** — ID renewal services, AMP/NIMES, richer GIS overlap  

---

## 12. Non-goals (current phase)

- Building a full ProGres clone or importing ProGres case/protection data  
- OpenG2P replacing partner cash handling on the ground (Bridge instructs and records; NGO still pays physical cash)  
- ID renewal booking and full online refugee service catalogue  
- Treating PBMS per-program dedup alone as sufficient for cross-partner double dipping (that is **IBR**)

---

## 13. Open points (non-blocking)

- Exact ProGres v4 auth API contract (biometric modalities, timeout, offline policy)  
- Whether IBR blocks hard or soft-flags with settlement override  
- Agency float reconciliation rules in Bridge vs MoFPED/AMP  
- UGPass organisation onboarding assumptions for NGOs (confirm with NITA-U)  
- Field app offline sync technology choice  

---

## 14. References

- OpenG2P docs: https://docs.openg2p.org/  
- OpenG2P PBMS: https://docs.openg2p.org/products/pbms  
- Registry platform: https://github.com/OpenG2P/registry-platform  
- Farmer registry (extension pattern): https://github.com/OpenG2P/farmer-registry  
- This repo’s registry package: [registry/README.md](../registry/README.md) · [Registry-Refugee-Extension.md](../registry/docs/Registry-Refugee-Extension.md)  
- Requirement demo: `RPCMS-Refugee-Coordination-Demo` (local HTML prototype)

---

*Document owner: Uganda RPCMS / OpenG2P implementation team. Update this file when locked decisions change.*
