INSERT INTO "public"."g2p_register_schemas" ("register_id","deduplicate_schema","search_result_schema","filter_schema") VALUES
(
  'cc31d36d-8140-4eb5-b041-f1090f3d733b',
  '[{"field_name": "household_head", "match_type": "fuzzy", "weight": 0.5}, {"field_name": "settlement_code", "match_type": "exact", "weight": 0.25}, {"field_name": "zone_code", "match_type": "exact", "weight": 0.25}]',
  '[{"field_name": "functional_record_id", "display_label": "Household ID", "order": 1}, {"field_name": "household_head", "display_label": "Household Head", "order": 2}, {"field_name": "size_of_group", "display_label": "Group Size", "order": 3}, {"field_name": "settlement_code", "display_label": "Settlement", "order": 4}, {"field_name": "zone_code", "display_label": "Zone", "order": 5}]',
  '[{"field_name": "household_head", "display_label": "Household Head", "filter_type": "text", "order": 1, "allowed_operators": ["eq", "contains"]}, {"field_name": "settlement_code", "display_label": "Settlement", "filter_type": "text", "order": 2, "allowed_operators": ["eq", "contains"]}, {"field_name": "zone_code", "display_label": "Zone", "filter_type": "text", "order": 3, "allowed_operators": ["eq", "contains"]}]'
),
(
  'b6127ac1-1987-4dcb-86e3-3a0fb10d6497',
  '[{"field_name": "progres_id", "match_type": "exact", "weight": 0.5}, {"field_name": "first_name", "match_type": "fuzzy", "weight": 0.25}, {"field_name": "last_name", "match_type": "fuzzy", "weight": 0.25}]',
  '[{"field_name": "functional_record_id", "display_label": "Refugee ID", "order": 1}, {"field_name": "progres_id", "display_label": "ProGres ID", "order": 2}, {"field_name": "first_name", "display_label": "First Name", "order": 3}, {"field_name": "last_name", "display_label": "Last Name", "order": 4}, {"field_name": "gender", "display_label": "Gender", "order": 5}, {"field_name": "settlement_code", "display_label": "Settlement", "order": 6}, {"field_name": "zone_code", "display_label": "Zone", "order": 7}]',
  '[{"field_name": "progres_id", "display_label": "ProGres ID", "filter_type": "text", "order": 1, "allowed_operators": ["eq", "contains"]}, {"field_name": "first_name", "display_label": "First Name", "filter_type": "text", "order": 2, "allowed_operators": ["eq", "contains"]}, {"field_name": "last_name", "display_label": "Last Name", "filter_type": "text", "order": 3, "allowed_operators": ["eq", "contains"]}, {"field_name": "gender", "display_label": "Gender", "filter_type": "dropdown", "order": 4, "allowed_operators": ["eq", "in"], "options_source": [{"value": "MALE", "label": "MALE"}, {"value": "FEMALE", "label": "FEMALE"}, {"value": "OTHER", "label": "OTHER"}, {"value": "UNKNOWN", "label": "UNKNOWN"}]}, {"field_name": "settlement_code", "display_label": "Settlement", "filter_type": "text", "order": 5, "allowed_operators": ["eq", "contains"]}, {"field_name": "record_status", "display_label": "Record Status", "filter_type": "dropdown", "order": 6, "allowed_operators": ["eq", "in"], "options_source": [{"value": "ACTIVE", "label": "ACTIVE"}, {"value": "INACTIVE", "label": "INACTIVE"}, {"value": "ARCHIVED", "label": "ARCHIVED"}]}]'
),
(
  '1cdc9f46-34bf-46f1-ba24-e6c992e44e8d',
  '[{"field_name": "first_name", "match_type": "fuzzy", "weight": 0.35}, {"field_name": "last_name", "match_type": "fuzzy", "weight": 0.35}, {"field_name": "progres_id", "match_type": "exact", "weight": 0.3}]',
  '[{"field_name": "functional_record_id", "display_label": "Member ID", "order": 1}, {"field_name": "progres_id", "display_label": "ProGres ID", "order": 2}, {"field_name": "first_name", "display_label": "First Name", "order": 3}, {"field_name": "last_name", "display_label": "Last Name", "order": 4}, {"field_name": "is_head", "display_label": "Is Head", "order": 5}, {"field_name": "relationship_to_the_head", "display_label": "Relationship", "order": 6}, {"field_name": "gender", "display_label": "Gender", "order": 7}]',
  '[{"field_name": "progres_id", "display_label": "ProGres ID", "filter_type": "text", "order": 1, "allowed_operators": ["eq", "contains"]}, {"field_name": "first_name", "display_label": "First Name", "filter_type": "text", "order": 2, "allowed_operators": ["eq", "contains"]}, {"field_name": "is_head", "display_label": "Is Head", "filter_type": "boolean", "order": 3, "allowed_operators": ["eq"]}]'
),
(
  'f54fc2f1-de59-430e-86f7-e0edfaa9cce6',
  '[{"field_name": "survey_round", "match_type": "exact", "weight": 0.6}, {"field_name": "survey_date", "match_type": "exact", "weight": 0.4}]',
  '[{"field_name": "functional_record_id", "display_label": "Survey ID", "order": 1}, {"field_name": "survey_round", "display_label": "Round", "order": 2}, {"field_name": "survey_date", "display_label": "Date", "order": 3}, {"field_name": "main_food_source", "display_label": "Main Food Source", "order": 4}, {"field_name": "self_reliance_index", "display_label": "Index", "order": 5}]',
  '[{"field_name": "survey_round", "display_label": "Round", "filter_type": "text", "order": 1, "allowed_operators": ["eq", "contains"]}, {"field_name": "earns_income", "display_label": "Earns Income", "filter_type": "boolean", "order": 2, "allowed_operators": ["eq"]}]'
)
ON CONFLICT ("register_id") DO UPDATE SET
  "deduplicate_schema" = EXCLUDED."deduplicate_schema",
  "search_result_schema" = EXCLUDED."search_result_schema",
  "filter_schema" = EXCLUDED."filter_schema";
