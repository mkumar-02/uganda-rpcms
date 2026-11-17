INSERT INTO "public"."g2p_registry_awe_policy_configurations" (
    "awe_policy_config_id",
    "policy_scope",
    "register_id",
    "intake_form_id",
    "section_id",
    "policy_type",
    "policy_key",
    "context_field_names"
) VALUES
    ('6f8048da-6674-43ed-9dd7-046097ee62a9', 'REGISTER', 'b6127ac1-1987-4dcb-86e3-3a0fb10d6497', '', '', 'registry.change_request', 'registry.change_request.refugee', 'null'),
    ('fa6c87c6-4ac2-452e-9b6f-0320d15194b5', 'INTAKE_FORM', 'b6127ac1-1987-4dcb-86e3-3a0fb10d6497', '4f0ea4b6-246e-4b72-b8c6-ac5dbc4a5501', '', 'registry.intake_form', 'registry.intake_form.refugee', 'null'),
    ('d32b35fe-69f1-48d1-9a15-6a9e5f5e469f', 'REGISTER', 'cc31d36d-8140-4eb5-b041-f1090f3d733b', '', '', 'registry.change_request', 'registry.change_request.household', 'null'),
    ('586696a7-ea52-431a-827e-44229748379e', 'INTAKE_FORM', 'cc31d36d-8140-4eb5-b041-f1090f3d733b', 'e1a01aff-ae7f-4672-b748-05138f7e341d', '', 'registry.intake_form', 'registry.intake_form.household', 'null')
ON CONFLICT ("awe_policy_config_id") DO NOTHING;
