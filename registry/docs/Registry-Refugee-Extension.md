# Refugee Registry Extension

Package: `openg2p_registry_refugee_extension` under `registry/refugee-extension/`.

## Aspects covered

| Aspect | Status | Location |
|--------|--------|----------|
| Domain models + history + intake tables | Done | `register_domain/models/` |
| Pydantic schemas | Done | `register_domain/schemas/` |
| Domain validation / search / record name | Done | `register_domain/services/` |
| Functional ID prefixes (`HH-`, `RF-`, `HM-`, `SR-`) | Done | `register_domain/id_generator/` |
| DB migrate + service registration | Done | `app.py` |
| Register definitions | Done | `meta_data/register-metadata/g2p_register_definitions.sql` |
| Search / filter / dedup schemas | Done | `g2p_register_schemas.sql` |
| Register UI sections (personal, settlement, socio, members, survey, headers) | Done | `g2p_register_sections.sql` |
| Register UI tabs + tab↔section map | Done | `g2p_register_ui_tabs.sql`, `g2p_register_ui_tab_sections.sql` |
| Intake form definitions | Done | `g2p_intake_form_definitions.sql` |
| Intake form UI tabs + sections | Done | `g2p_intake_form_ui_tabs.sql`, `g2p_intake_form_ui_tab_sections.sql` |
| AWE policy hooks (change request + intake) | Done | `meta_data/awe-integration/` |
| Registry name + default language | Done | `registry-configurations/` |
| Domain translations (EN) | Done | `registry_languages.sql` |
| Thin Docker images | Done | `registry/docker/` |
| Helm overlay chart | Done | `registry/helm/openg2p-refugee-registry/` |
| ProGres Yes/No auth adapter | Later | Outside this package |
| VC / eKYC from ProGres | Out of scope | Consent / auth-only constraint |
| Score engine for self-reliance | Stub | score SQL placeholders |

## Register IDs (stable)

| Register | UUID |
|----------|------|
| Household | `cc31d36d-8140-4eb5-b041-f1090f3d733b` |
| Refugee | `b6127ac1-1987-4dcb-86e3-3a0fb10d6497` |
| HouseholdMember | `1cdc9f46-34bf-46f1-ba24-e6c992e44e8d` |
| SelfRelianceSurvey | `f54fc2f1-de59-430e-86f7-e0edfaa9cce6` |

## Runtime

```bash
export REGISTRY_EXTENSION_MODULE=openg2p_registry_refugee_extension
pip install -e ./registry/refugee-extension
```

Platform db-seed applies SQL under `meta_data/` when the extension image is deployed.
