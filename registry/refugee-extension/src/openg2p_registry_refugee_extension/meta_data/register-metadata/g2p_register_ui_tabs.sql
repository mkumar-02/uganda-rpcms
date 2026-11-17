INSERT INTO "public"."g2p_register_ui_tabs" ("tab_id","register_id","tab_label","tab_order","is_active") VALUES
('refugee_refugee_tab','b6127ac1-1987-4dcb-86e3-3a0fb10d6497','refugee_refugee_tab',0,'TRUE'),
('refugee_household_link_tab','b6127ac1-1987-4dcb-86e3-3a0fb10d6497','refugee_household_link_tab',10,'TRUE'),
('household_household_tab','cc31d36d-8140-4eb5-b041-f1090f3d733b','household_household_tab',0,'TRUE'),
('household_refugee_tab','cc31d36d-8140-4eb5-b041-f1090f3d733b','household_refugee_tab',10,'TRUE'),
('household_survey_tab','cc31d36d-8140-4eb5-b041-f1090f3d733b','household_survey_tab',20,'TRUE')
ON CONFLICT ("tab_id") DO UPDATE SET
  "register_id" = EXCLUDED."register_id",
  "tab_label" = EXCLUDED."tab_label",
  "tab_order" = EXCLUDED."tab_order",
  "is_active" = EXCLUDED."is_active";
