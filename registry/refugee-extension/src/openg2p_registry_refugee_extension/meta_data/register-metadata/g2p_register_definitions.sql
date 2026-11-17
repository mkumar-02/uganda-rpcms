-- Uganda RPCMS Refugee Registry — register definitions
-- Household is the master register; Refugee / HouseholdMember / SelfRelianceSurvey hang under it.
--
-- UUIDs (stable):
--   Household:            cc31d36d-8140-4eb5-b041-f1090f3d733b
--   Refugee:              b6127ac1-1987-4dcb-86e3-3a0fb10d6497
--   HouseholdMember:      1cdc9f46-34bf-46f1-ba24-e6c992e44e8d
--   SelfRelianceSurvey:   f54fc2f1-de59-430e-86f7-e0edfaa9cce6

INSERT INTO "public"."g2p_register_definitions" (
  "register_id","register_mnemonic","register_subject","register_description",
  "master_register_id","register_rank","functional_id_generation_required","register_purpose",
  "program_id","program_mnemonic","register_icon","has_image","dedup_is_enabled",
  "dedup_threshold_score","completion_score_required","outgest_applicable",
  "requires_registrant_authentication","registrant_authentication_validity_days",
  "registrant_re_auth_warning_days_before"
) VALUES
(
  'cc31d36d-8140-4eb5-b041-f1090f3d733b','Household','Households',
  'Refugee household register (Uganda RPCMS)',NULL,1,'TRUE','REGISTER',
  NULL,NULL,'','FALSE','TRUE',70,'FALSE','FALSE','FALSE',730,30
),
(
  'b6127ac1-1987-4dcb-86e3-3a0fb10d6497','Refugee','Refugees',
  'Primary refugee registrant — holds ProGres ID; auth against ProGres is Yes/No only',
  'cc31d36d-8140-4eb5-b041-f1090f3d733b',2,'TRUE','REGISTER',
  NULL,NULL,'','FALSE','TRUE',70,'TRUE','FALSE','TRUE',730,30
),
(
  '1cdc9f46-34bf-46f1-ba24-e6c992e44e8d','HouseholdMember','Household Members',
  'Household member roster','cc31d36d-8140-4eb5-b041-f1090f3d733b',10,'FALSE','TABLE',
  NULL,NULL,NULL,'FALSE','FALSE',0,'FALSE','FALSE','FALSE',730,30
),
(
  'f54fc2f1-de59-430e-86f7-e0edfaa9cce6','SelfRelianceSurvey','Self-Reliance Surveys',
  'Self-reliance survey rounds (intake-style), linked to household',
  'cc31d36d-8140-4eb5-b041-f1090f3d733b',20,'FALSE','TABLE',
  NULL,NULL,NULL,'FALSE','FALSE',0,'FALSE','FALSE','FALSE',730,30
)
ON CONFLICT ("register_id") DO UPDATE SET
  "register_mnemonic" = EXCLUDED."register_mnemonic",
  "register_subject" = EXCLUDED."register_subject",
  "register_description" = EXCLUDED."register_description",
  "master_register_id" = EXCLUDED."master_register_id",
  "register_rank" = EXCLUDED."register_rank",
  "functional_id_generation_required" = EXCLUDED."functional_id_generation_required",
  "register_purpose" = EXCLUDED."register_purpose",
  "program_id" = EXCLUDED."program_id",
  "program_mnemonic" = EXCLUDED."program_mnemonic",
  "register_icon" = EXCLUDED."register_icon",
  "has_image" = EXCLUDED."has_image",
  "dedup_is_enabled" = EXCLUDED."dedup_is_enabled",
  "dedup_threshold_score" = EXCLUDED."dedup_threshold_score",
  "completion_score_required" = EXCLUDED."completion_score_required",
  "outgest_applicable" = EXCLUDED."outgest_applicable",
  "requires_registrant_authentication" = EXCLUDED."requires_registrant_authentication",
  "registrant_authentication_validity_days" = EXCLUDED."registrant_authentication_validity_days",
  "registrant_re_auth_warning_days_before" = EXCLUDED."registrant_re_auth_warning_days_before";
