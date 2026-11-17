INSERT INTO "public"."g2p_intake_form_definitions" (
  "form_id","register_id","form_mnemonic","form_description",
  "number_of_verifications","used_only_in_ingestion_pipeline"
) VALUES
(
  '4f0ea4b6-246e-4b72-b8c6-ac5dbc4a5501',
  'b6127ac1-1987-4dcb-86e3-3a0fb10d6497',
  'refugee_ingestion_intake',
  'Refugee registration / ingestion intake (Uganda RPCMS)',
  1,'TRUE'
),
(
  'e1a01aff-ae7f-4672-b748-05138f7e341d',
  'cc31d36d-8140-4eb5-b041-f1090f3d733b',
  'household_ingestion_intake',
  'Household registration / ingestion intake (Uganda RPCMS)',
  1,'TRUE'
)
ON CONFLICT ("form_id") DO UPDATE SET
  "register_id" = EXCLUDED."register_id",
  "form_mnemonic" = EXCLUDED."form_mnemonic",
  "form_description" = EXCLUDED."form_description",
  "number_of_verifications" = EXCLUDED."number_of_verifications",
  "used_only_in_ingestion_pipeline" = EXCLUDED."used_only_in_ingestion_pipeline";
