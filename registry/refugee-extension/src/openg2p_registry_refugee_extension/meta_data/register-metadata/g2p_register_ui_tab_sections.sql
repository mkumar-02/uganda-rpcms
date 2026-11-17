INSERT INTO "public"."g2p_register_ui_tab_sections" ("tab_section_id","register_id","tab_id","section_id","section_order") VALUES
-- Refugee register tabs
('rf_ts_header','b6127ac1-1987-4dcb-86e3-3a0fb10d6497','refugee_refugee_tab','rpcms_refugee_header_00',5),
('rf_ts_personal','b6127ac1-1987-4dcb-86e3-3a0fb10d6497','refugee_refugee_tab','rpcms_refugee_personal_section_01',10),
('rf_ts_settlement','b6127ac1-1987-4dcb-86e3-3a0fb10d6497','refugee_refugee_tab','rpcms_refugee_location_section_02',20),
('rf_ts_socio','b6127ac1-1987-4dcb-86e3-3a0fb10d6497','refugee_refugee_tab','rpcms_refugee_socio_section_03',30),
('rf_ts_hh_lookup','b6127ac1-1987-4dcb-86e3-3a0fb10d6497','refugee_household_link_tab','rpcms_refugee_household_lookup_01',10),
-- Household register tabs
('hh_ts_header','cc31d36d-8140-4eb5-b041-f1090f3d733b','household_household_tab','rpcms_household_header_00',5),
('hh_ts_info','cc31d36d-8140-4eb5-b041-f1090f3d733b','household_household_tab','rpcms_household_information_01',10),
('hh_ts_members','cc31d36d-8140-4eb5-b041-f1090f3d733b','household_household_tab','rpcms_household_members_02',20),
('hh_ts_survey','cc31d36d-8140-4eb5-b041-f1090f3d733b','household_survey_tab','rpcms_self_reliance_survey_03',10)
ON CONFLICT ("tab_section_id") DO UPDATE SET
  "register_id" = EXCLUDED."register_id",
  "tab_id" = EXCLUDED."tab_id",
  "section_id" = EXCLUDED."section_id",
  "section_order" = EXCLUDED."section_order";
