# IBR (paused)

Cross-agency double-dipping checks for Uganda RPCMS.

**Status:** parked until a design document is available.

## Intended role (from architecture)

- Key: `(progres_id, benefit_type, cycle_period)` — optional household key later
- Called by PBMS before entitlement / Bridge instruction
- Not a substitute for per-program dedup inside PBMS alone

See [Architecture §5.3](../docs/RPCMS-OpenG2P-Architecture.md).
