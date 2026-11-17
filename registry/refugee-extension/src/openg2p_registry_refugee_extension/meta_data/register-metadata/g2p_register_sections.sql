-- Minimal register UI sections for Uganda RPCMS Refugee Registry.
-- Expand tabs / intake form wiring in follow-up (farmer-registry has the full pattern).

INSERT INTO "public"."g2p_register_sections" (
  "register_id","section_id","section_register_id","is_core_section","section_mnemonic",
  "section_description","documents_required","no_of_verifications_required","is_list",
  "section_weightage","section_ui_schema",
  "cr_auto_approve_for_bene_portal","cr_auto_approve_for_agent_portal",
  "cr_auto_approve_for_staff_portal","cr_auto_approve_for_partner"
) VALUES
-- Refugee: personal + ProGres
(
  'b6127ac1-1987-4dcb-86e3-3a0fb10d6497',
  'rpcms_refugee_personal_section_01',
  'b6127ac1-1987-4dcb-86e3-3a0fb10d6497',
  'FALSE','rf_personal_info','Refugee personal identification including ProGres ID',
  'FALSE',0,'FALSE',10,
  '{"panels": [{"panels": [{"widgets": [{"widget": "text", "widget-id": "first_name", "widget-type": "input", "widget-label": "first_name", "widget-required": true, "widget-data-path": "b6127ac1-1987-4dcb-86e3-3a0fb10d6497.first_name"}, {"widget": "text", "widget-id": "middle_name", "widget-type": "input", "widget-label": "middle_name", "widget-data-path": "b6127ac1-1987-4dcb-86e3-3a0fb10d6497.middle_name"}, {"widget": "text", "widget-id": "last_name", "widget-type": "input", "widget-label": "last_name", "widget-required": true, "widget-data-path": "b6127ac1-1987-4dcb-86e3-3a0fb10d6497.last_name"}], "panel-id": "panel_names", "panel-orientation": "vertical"}, {"widgets": [{"widget": "text", "widget-id": "progres_id", "widget-type": "input", "widget-label": "progres_id", "widget-required": true, "widget-data-path": "b6127ac1-1987-4dcb-86e3-3a0fb10d6497.progres_id", "widget-data-helptext": "ProGres individual ID from the refugee card (e.g. UGA-00423318). Auth against ProGres is Yes/No only."}, {"widget": "date", "widget-id": "progres_id_valid_to", "widget-type": "input", "widget-label": "progres_id_valid_to", "widget-data-path": "b6127ac1-1987-4dcb-86e3-3a0fb10d6497.progres_id_valid_to", "widget-data-format": {"dateFormat": "DD/MM/YYYY", "inputMethod": "picker"}}, {"widget": "select", "widget-id": "displacement_status", "widget-type": "input", "widget-label": "displacement_status", "widget-data-path": "b6127ac1-1987-4dcb-86e3-3a0fb10d6497.displacement_status", "widget-data-source": {"type": "static", "options": [{"label": "REFUGEE", "value": "REFUGEE"}, {"label": "ASYLUM_SEEKER", "value": "ASYLUM_SEEKER"}, {"label": "OTHER_OF_CONCERN", "value": "OTHER_OF_CONCERN"}]}}], "panel-id": "panel_progres", "panel-orientation": "vertical"}, {"widgets": [{"widget": "date", "widget-id": "birth_date", "widget-type": "input", "widget-label": "birth_date", "widget-data-path": "b6127ac1-1987-4dcb-86e3-3a0fb10d6497.birth_date", "widget-data-format": {"dateFormat": "DD/MM/YYYY", "dateConstraint": "past-only"}}, {"widget": "select", "widget-id": "gender", "widget-type": "input", "widget-label": "gender", "widget-required": true, "widget-data-path": "b6127ac1-1987-4dcb-86e3-3a0fb10d6497.gender", "widget-data-source": {"type": "static", "options": [{"label": "MALE", "value": "MALE"}, {"label": "FEMALE", "value": "FEMALE"}, {"label": "OTHER", "value": "OTHER"}, {"label": "UNKNOWN", "value": "UNKNOWN"}]}}, {"widget": "text", "widget-id": "country_of_origin", "widget-type": "input", "widget-label": "country_of_origin", "widget-data-path": "b6127ac1-1987-4dcb-86e3-3a0fb10d6497.country_of_origin"}], "panel-id": "panel_demographics", "panel-orientation": "vertical"}], "panel-id": "panel_personal_main", "panel-orientation": "horizontal"}], "section-id": "refugee_personal_information", "section-title": "refugee_personal_information", "section-editable": true}',
  'FALSE','FALSE','FALSE','FALSE'
),
-- Refugee: settlement / zone
(
  'b6127ac1-1987-4dcb-86e3-3a0fb10d6497',
  'rpcms_refugee_location_section_02',
  'b6127ac1-1987-4dcb-86e3-3a0fb10d6497',
  'FALSE','rf_settlement','Settlement and zone',
  'FALSE',0,'FALSE',10,
  '{"panels": [{"panels": [{"widgets": [{"widget": "text", "widget-id": "settlement_code", "widget-type": "input", "widget-label": "settlement_code", "widget-required": true, "widget-data-path": "b6127ac1-1987-4dcb-86e3-3a0fb10d6497.settlement_code"}, {"widget": "text", "widget-id": "zone_code", "widget-type": "input", "widget-label": "zone_code", "widget-required": true, "widget-data-path": "b6127ac1-1987-4dcb-86e3-3a0fb10d6497.zone_code"}, {"widget": "date", "widget-id": "arrival_date", "widget-type": "input", "widget-label": "arrival_date", "widget-data-path": "b6127ac1-1987-4dcb-86e3-3a0fb10d6497.arrival_date", "widget-data-format": {"dateFormat": "DD/MM/YYYY", "dateConstraint": "past-only"}}], "panel-id": "panel_settlement", "panel-orientation": "vertical"}], "panel-id": "panel_settlement_main", "panel-orientation": "horizontal"}], "section-id": "refugee_settlement", "section-title": "refugee_settlement", "section-editable": true}',
  'FALSE','FALSE','FALSE','FALSE'
),
-- Refugee ↔ household link
(
  'b6127ac1-1987-4dcb-86e3-3a0fb10d6497',
  'rpcms_refugee_household_lookup_01',
  'b6127ac1-1987-4dcb-86e3-3a0fb10d6497',
  'FALSE','rf_household_lookup','Link refugee to household',
  'FALSE',0,'FALSE',10,
  '{"panels": [{"panels": [{"widgets": [{"widget": "register-lookup", "widget-id": "household_lookup", "widget-type": "input", "widget-label": "household", "widget-required": false, "widget-data-path": "b6127ac1-1987-4dcb-86e3-3a0fb10d6497.link_internal_record_id", "widget-data-source": {"type": "api", "method": "POST", "params": {"register_id": "cc31d36d-8140-4eb5-b041-f1090f3d733b"}, "service": "register", "endpoint": "records"}, "widget-lookup-config": {"page_size": 10, "action_label": "search_household", "search_placeholder": "search_by_name_or_id", "select_record_label": "select_household"}}], "panel-id": "household_lookup_inside", "panel-orientation": "vertical"}], "panel-id": "household_lookup_outside", "panel-orientation": "horizontal"}], "section-id": "refugee_household_lookup", "section-title": "refugee_household_lookup", "section-editable": true}',
  'FALSE','FALSE','FALSE','FALSE'
),
-- Household information
(
  'cc31d36d-8140-4eb5-b041-f1090f3d733b',
  'rpcms_household_information_01',
  'cc31d36d-8140-4eb5-b041-f1090f3d733b',
  'FALSE','hh_information','Household information',
  'FALSE',0,'FALSE',10,
  '{"panels": [{"panels": [{"widgets": [{"widget": "text", "widget-id": "household_head", "widget-type": "input", "widget-label": "household_head", "widget-data-path": "cc31d36d-8140-4eb5-b041-f1090f3d733b.household_head"}, {"widget": "number", "widget-id": "size_of_group", "widget-type": "input", "widget-label": "size_of_group", "widget-required": true, "widget-data-path": "cc31d36d-8140-4eb5-b041-f1090f3d733b.size_of_group", "widget-data-format": {"minimum": 1, "numericType": "integer"}}, {"widget": "number", "widget-id": "number_of_children", "widget-type": "input", "widget-label": "number_of_children", "widget-data-path": "cc31d36d-8140-4eb5-b041-f1090f3d733b.number_of_children", "widget-data-format": {"minimum": 0, "numericType": "integer"}}], "panel-id": "hh_info_1", "panel-orientation": "vertical"}, {"widgets": [{"widget": "number", "widget-id": "number_of_male_members", "widget-type": "input", "widget-label": "number_of_male_members", "widget-required": true, "widget-data-path": "cc31d36d-8140-4eb5-b041-f1090f3d733b.number_of_male_members", "widget-data-format": {"minimum": 0, "numericType": "integer"}}, {"widget": "number", "widget-id": "number_of_female_members", "widget-type": "input", "widget-label": "number_of_female_members", "widget-required": true, "widget-data-path": "cc31d36d-8140-4eb5-b041-f1090f3d733b.number_of_female_members", "widget-data-format": {"minimum": 0, "numericType": "integer"}}, {"widget": "number", "widget-id": "number_of_elderly_members", "widget-type": "input", "widget-label": "number_of_elderly_members", "widget-data-path": "cc31d36d-8140-4eb5-b041-f1090f3d733b.number_of_elderly_members", "widget-data-format": {"minimum": 0, "numericType": "integer"}}], "panel-id": "hh_info_2", "panel-orientation": "vertical"}, {"widgets": [{"widget": "text", "widget-id": "settlement_code", "widget-type": "input", "widget-label": "settlement_code", "widget-data-path": "cc31d36d-8140-4eb5-b041-f1090f3d733b.settlement_code"}, {"widget": "text", "widget-id": "zone_code", "widget-type": "input", "widget-label": "zone_code", "widget-data-path": "cc31d36d-8140-4eb5-b041-f1090f3d733b.zone_code"}], "panel-id": "hh_info_3", "panel-orientation": "vertical"}], "panel-id": "hh_info_main", "panel-orientation": "horizontal"}], "section-id": "household_information", "section-title": "household_information", "section-editable": true}',
  'FALSE','FALSE','FALSE','FALSE'
),
-- Household members table
(
  'cc31d36d-8140-4eb5-b041-f1090f3d733b',
  'rpcms_household_members_02',
  '1cdc9f46-34bf-46f1-ba24-e6c992e44e8d',
  'FALSE','hh_members','Household members',
  'FALSE',0,'TRUE',10,
  '{"panels": [{"panels": [{"widgets": [{"widget": "dialog-table", "widget-id": "members_table", "widget-type": "table", "widget-label": "household_members_records", "widget-data-path": "1cdc9f46-34bf-46f1-ba24-e6c992e44e8d.records", "widget-data-columns": [{"widget": "text", "column-key": "progres_id", "widget-type": "input", "widget-label": "progres_id", "widget-data-path": "progres_id"}, {"widget": "text", "column-key": "first_name", "widget-type": "input", "widget-label": "first_name", "widget-required": true, "widget-data-path": "first_name"}, {"widget": "text", "column-key": "last_name", "widget-type": "input", "widget-label": "last_name", "widget-required": true, "widget-data-path": "last_name"}, {"widget": "date", "column-key": "birth_date", "widget-type": "input", "widget-label": "birth_date", "widget-data-path": "birth_date", "widget-data-format": {"dateFormat": "DD/MM/YYYY", "dateConstraint": "past-only"}}, {"widget": "select", "column-key": "gender", "widget-type": "input", "widget-label": "gender", "widget-required": true, "widget-data-path": "gender", "widget-data-source": {"type": "static", "options": [{"label": "MALE", "value": "MALE"}, {"label": "FEMALE", "value": "FEMALE"}, {"label": "OTHERS", "value": "OTHERS"}, {"label": "UNKNOWN", "value": "UNKNOWN"}]}}, {"widget": "boolean", "column-key": "is_head", "widget-type": "input", "widget-label": "is_head", "widget-data-path": "is_head", "widget-data-format": {"booleanControlType": "checkbox", "booleanRepresentation": "yes-no"}, "widget-data-default": false}, {"widget": "select", "column-key": "relationship_to_the_head", "widget-type": "input", "widget-label": "relationship_to_the_head", "widget-data-path": "relationship_to_the_head", "widget-data-source": {"type": "static", "options": [{"label": "SELF", "value": "SELF"}, {"label": "SPOUSE", "value": "SPOUSE"}, {"label": "CHILD", "value": "CHILD"}, {"label": "PARENT", "value": "PARENT"}, {"label": "SIBLING", "value": "SIBLING"}, {"label": "OTHER_RELATIVE", "value": "OTHER_RELATIVE"}, {"label": "NON_RELATIVE", "value": "NON_RELATIVE"}]}}], "widget-data-add-label": "add_member", "widget-data-operations": {"add": true, "edit": true, "remove": true}}], "panel-id": "members_inner", "panel-column-span": 3, "panel-orientation": "vertical"}], "panel-id": "members_outer", "panel-orientation": "horizontal"}], "section-id": "household_members", "section-title": "household_members", "section-editable": true}',
  'FALSE','FALSE','FALSE','FALSE'
),
-- Self-reliance survey table under household
(
  'cc31d36d-8140-4eb5-b041-f1090f3d733b',
  'rpcms_self_reliance_survey_03',
  'f54fc2f1-de59-430e-86f7-e0edfaa9cce6',
  'FALSE','hh_self_reliance_survey','Self-reliance survey rounds',
  'FALSE',0,'TRUE',10,
  '{"panels": [{"panels": [{"widgets": [{"widget": "table", "widget-id": "survey_table", "widget-type": "table", "widget-label": "self_reliance_surveys", "widget-data-path": "f54fc2f1-de59-430e-86f7-e0edfaa9cce6.records", "widget-data-columns": [{"widget": "text", "column-key": "survey_round", "widget-type": "input", "widget-label": "survey_round", "widget-required": true, "widget-data-path": "survey_round"}, {"widget": "date", "column-key": "survey_date", "widget-type": "input", "widget-label": "survey_date", "widget-data-path": "survey_date", "widget-data-format": {"dateFormat": "DD/MM/YYYY"}}, {"widget": "select", "column-key": "main_food_source", "widget-type": "input", "widget-label": "main_food_source", "widget-data-path": "main_food_source", "widget-data-source": {"type": "static", "options": [{"label": "ASSISTANCE_ONLY", "value": "ASSISTANCE_ONLY"}, {"label": "OWN_PRODUCTION_AND_ASSISTANCE", "value": "OWN_PRODUCTION_AND_ASSISTANCE"}, {"label": "MARKET_INCOME", "value": "MARKET_INCOME"}]}}, {"widget": "boolean", "column-key": "earns_income", "widget-type": "input", "widget-label": "earns_income", "widget-data-path": "earns_income", "widget-data-format": {"booleanRepresentation": "yes-no"}}, {"widget": "text", "column-key": "income_activity", "widget-type": "input", "widget-label": "income_activity", "widget-data-path": "income_activity"}, {"widget": "select", "column-key": "children_in_school", "widget-type": "input", "widget-label": "children_in_school", "widget-data-path": "children_in_school", "widget-data-source": {"type": "static", "options": [{"label": "0", "value": "0"}, {"label": "1-2", "value": "1-2"}, {"label": "3-4", "value": "3-4"}, {"label": "5+", "value": "5+"}]}}, {"widget": "boolean", "column-key": "savings_group_member", "widget-type": "input", "widget-label": "savings_group_member", "widget-data-path": "savings_group_member", "widget-data-format": {"booleanRepresentation": "yes-no"}}, {"widget": "number", "column-key": "self_reliance_index", "widget-type": "input", "widget-label": "self_reliance_index", "widget-data-path": "self_reliance_index", "widget-data-format": {"numericType": "integer"}, "widget-data-validation": {"min": 0, "max": 100}}], "widget-data-add-label": "add_survey", "widget-data-operations": {"add": true, "edit": true, "remove": true}}], "panel-id": "survey_inner", "panel-column-span": 3, "panel-orientation": "vertical"}], "panel-id": "survey_outer", "panel-orientation": "horizontal"}], "section-id": "household_self_reliance_survey", "section-title": "household_self_reliance_survey", "section-editable": true}',
  'FALSE','FALSE','FALSE','FALSE'
),
-- Refugee: socio-economic & health
(
  'b6127ac1-1987-4dcb-86e3-3a0fb10d6497',
  'rpcms_refugee_socio_section_03',
  'b6127ac1-1987-4dcb-86e3-3a0fb10d6497',
  'FALSE','rf_socio_health','Refugee socio-economic and health',
  'FALSE',0,'FALSE',10,
  '{"panels": [{"panels": [{"widgets": [{"widget": "select", "widget-id": "disabled", "widget-type": "input", "widget-label": "disabled", "widget-data-path": "b6127ac1-1987-4dcb-86e3-3a0fb10d6497.disabled", "widget-data-source": {"type": "static", "options": [{"label": "YES", "value": true}, {"label": "NO", "value": false}]}}, {"widget": "select", "widget-id": "disability_type", "widget-type": "input", "widget-label": "disability_type", "widget-data-path": "b6127ac1-1987-4dcb-86e3-3a0fb10d6497.disability_type", "widget-data-source": {"type": "static", "options": [{"label": "VISION", "value": "VISION"}, {"label": "HEARING", "value": "HEARING"}, {"label": "MOBILITY", "value": "MOBILITY"}, {"label": "COGNITION", "value": "COGNITION"}, {"label": "SELF_CARE", "value": "SELF_CARE"}, {"label": "COMMUNICATION", "value": "COMMUNICATION"}]}}, {"widget": "select", "widget-id": "disability_severity", "widget-type": "input", "widget-label": "disability_severity", "widget-data-path": "b6127ac1-1987-4dcb-86e3-3a0fb10d6497.disability_severity", "widget-data-source": {"type": "static", "options": [{"label": "NO_DIFFICULTY", "value": "NO_DIFFICULTY"}, {"label": "SOME_DIFFICULTY", "value": "SOME_DIFFICULTY"}, {"label": "A_LOT_OF_DIFFICULTY", "value": "A_LOT_OF_DIFFICULTY"}, {"label": "CANNOT_DO_AT_ALL", "value": "CANNOT_DO_AT_ALL"}]}}], "panel-id": "panel_health", "panel-title": "health_details", "panel-orientation": "vertical"}, {"widgets": [{"widget": "select", "widget-id": "education_level", "widget-type": "input", "widget-label": "education_level", "widget-data-path": "b6127ac1-1987-4dcb-86e3-3a0fb10d6497.education_level", "widget-data-source": {"type": "static", "options": [{"label": "ILLITERATE", "value": "ILLITERATE"}, {"label": "CAN_READ_AND_WRITE", "value": "CAN_READ_AND_WRITE"}, {"label": "PRIMARY", "value": "PRIMARY"}, {"label": "SECONDARY", "value": "SECONDARY"}, {"label": "TERTIARY", "value": "TERTIARY"}, {"label": "HIGHER_EDUCATION", "value": "HIGHER_EDUCATION"}]}}, {"widget": "text", "widget-id": "language_spoken", "widget-type": "input", "widget-label": "language_spoken", "widget-data-path": "b6127ac1-1987-4dcb-86e3-3a0fb10d6497.language_spoken"}, {"widget": "boolean", "widget-id": "has_personal_phone", "widget-type": "input", "widget-label": "has_personal_phone", "widget-data-path": "b6127ac1-1987-4dcb-86e3-3a0fb10d6497.has_personal_phone", "widget-data-format": {"booleanRepresentation": "yes-no"}}], "panel-id": "panel_socio", "panel-title": "socio_economic_details", "panel-orientation": "vertical"}], "panel-id": "panel_socio_main", "panel-orientation": "horizontal"}], "section-id": "refugee_socio_economic_and_health", "section-title": "refugee_socio_economic_and_health", "section-editable": true}',
  'FALSE','FALSE','FALSE','FALSE'
),
-- Refugee header
(
  'b6127ac1-1987-4dcb-86e3-3a0fb10d6497',
  'rpcms_refugee_header_00',
  'b6127ac1-1987-4dcb-86e3-3a0fb10d6497',
  'FALSE','rf_header','Refugee record header',
  'FALSE',0,'FALSE',10,
  '{"panels": [{"panels": [{"widgets": [{"widget": "header-section", "widget-id": "registry-header", "widget-type": "group", "widget-data-path": {"name": "b6127ac1-1987-4dcb-86e3-3a0fb10d6497.record_name", "status": "b6127ac1-1987-4dcb-86e3-3a0fb10d6497.record_status", "createdAt": "b6127ac1-1987-4dcb-86e3-3a0fb10d6497.created_at", "createdBy": "b6127ac1-1987-4dcb-86e3-3a0fb10d6497.created_by", "functionalId": "b6127ac1-1987-4dcb-86e3-3a0fb10d6497.functional_record_id", "statusReason": "b6127ac1-1987-4dcb-86e3-3a0fb10d6497.record_status_reason", "lastApprovedAt": "b6127ac1-1987-4dcb-86e3-3a0fb10d6497.last_approved_at", "lastApprovedBy": "b6127ac1-1987-4dcb-86e3-3a0fb10d6497.last_approved_by"}, "widget-data-format": {"nameColor": "#1F2F4A", "statusColors": {"active": "#16A34A", "archived": "#6B7280", "inactive": "#D97706"}}, "widget-field-config": {"status": {"data-source": {"type": "static", "options": [{"label": "ACTIVE", "value": "ACTIVE"}, {"label": "INACTIVE", "value": "INACTIVE"}, {"label": "ARCHIVED", "value": "ARCHIVED"}]}}}}], "panel-id": "refugee_header_inside", "panel-orientation": "vertical"}], "panel-id": "refugee_header_outside", "panel-orientation": "horizontal"}], "section-id": "refugee_header", "section-title": "refugee_header", "section-editable": true}',
  'FALSE','FALSE','FALSE','FALSE'
),
-- Household header
(
  'cc31d36d-8140-4eb5-b041-f1090f3d733b',
  'rpcms_household_header_00',
  'cc31d36d-8140-4eb5-b041-f1090f3d733b',
  'FALSE','hh_header','Household record header',
  'FALSE',0,'FALSE',10,
  '{"panels": [{"panels": [{"widgets": [{"widget": "header-section", "widget-id": "registry-header", "widget-type": "group", "widget-data-path": {"name": "cc31d36d-8140-4eb5-b041-f1090f3d733b.record_name", "status": "cc31d36d-8140-4eb5-b041-f1090f3d733b.record_status", "createdAt": "cc31d36d-8140-4eb5-b041-f1090f3d733b.created_at", "createdBy": "cc31d36d-8140-4eb5-b041-f1090f3d733b.created_by", "functionalId": "cc31d36d-8140-4eb5-b041-f1090f3d733b.functional_record_id", "statusReason": "cc31d36d-8140-4eb5-b041-f1090f3d733b.record_status_reason", "lastApprovedAt": "cc31d36d-8140-4eb5-b041-f1090f3d733b.last_approved_at", "lastApprovedBy": "cc31d36d-8140-4eb5-b041-f1090f3d733b.last_approved_by"}, "widget-data-format": {"nameColor": "#1F2F4A", "statusColors": {"active": "#16A34A", "archived": "#6B7280", "inactive": "#D97706"}}, "widget-field-config": {"status": {"data-source": {"type": "static", "options": [{"label": "ACTIVE", "value": "ACTIVE"}, {"label": "INACTIVE", "value": "INACTIVE"}, {"label": "ARCHIVED", "value": "ARCHIVED"}]}}}}], "panel-id": "household_header_inside", "panel-orientation": "vertical"}], "panel-id": "household_header_outside", "panel-orientation": "horizontal"}], "section-id": "household_header", "section-title": "household_header", "section-editable": true}',
  'FALSE','FALSE','FALSE','FALSE'
)
ON CONFLICT ("section_id") DO UPDATE SET
  "register_id" = EXCLUDED."register_id",
  "section_register_id" = EXCLUDED."section_register_id",
  "is_core_section" = EXCLUDED."is_core_section",
  "section_mnemonic" = EXCLUDED."section_mnemonic",
  "section_description" = EXCLUDED."section_description",
  "documents_required" = EXCLUDED."documents_required",
  "no_of_verifications_required" = EXCLUDED."no_of_verifications_required",
  "is_list" = EXCLUDED."is_list",
  "section_weightage" = EXCLUDED."section_weightage",
  "section_ui_schema" = EXCLUDED."section_ui_schema",
  "cr_auto_approve_for_bene_portal" = EXCLUDED."cr_auto_approve_for_bene_portal",
  "cr_auto_approve_for_agent_portal" = EXCLUDED."cr_auto_approve_for_agent_portal",
  "cr_auto_approve_for_staff_portal" = EXCLUDED."cr_auto_approve_for_staff_portal",
  "cr_auto_approve_for_partner" = EXCLUDED."cr_auto_approve_for_partner";
