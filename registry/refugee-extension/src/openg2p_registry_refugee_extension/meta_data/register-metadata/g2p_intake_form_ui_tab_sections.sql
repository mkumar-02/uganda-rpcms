INSERT INTO "public"."g2p_intake_form_ui_tab_sections" ("tab_section_id","tab_id","section_id","section_order") VALUES
-- Refugee intake
('rf_intake_ts_hh','c703f74f-0e66-4784-8cba-505c318265b5','rpcms_refugee_household_lookup_01',10),
('rf_intake_ts_personal','c703f74f-0e66-4784-8cba-505c318265b5','rpcms_refugee_personal_section_01',20),
('rf_intake_ts_settlement','c703f74f-0e66-4784-8cba-505c318265b5','rpcms_refugee_location_section_02',30),
('rf_intake_ts_socio','c703f74f-0e66-4784-8cba-505c318265b5','rpcms_refugee_socio_section_03',40),
-- Household intake
('hh_intake_ts_info','1e1ee059-55f6-4658-83e2-145a699d0a79','rpcms_household_information_01',10),
('hh_intake_ts_members','1e1ee059-55f6-4658-83e2-145a699d0a79','rpcms_household_members_02',20),
('hh_intake_ts_survey','1e1ee059-55f6-4658-83e2-145a699d0a79','rpcms_self_reliance_survey_03',30)
ON CONFLICT ("tab_section_id") DO UPDATE SET
  "tab_id" = EXCLUDED."tab_id",
  "section_id" = EXCLUDED."section_id",
  "section_order" = EXCLUDED."section_order";
