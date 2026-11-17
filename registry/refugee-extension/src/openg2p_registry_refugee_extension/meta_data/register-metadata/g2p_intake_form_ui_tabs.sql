INSERT INTO "public"."g2p_intake_form_ui_tabs" ("tab_id","form_id","tab_label","tab_order") VALUES
('c703f74f-0e66-4784-8cba-505c318265b5','4f0ea4b6-246e-4b72-b8c6-ac5dbc4a5501','refugee_intake_tab',10),
('1e1ee059-55f6-4658-83e2-145a699d0a79','e1a01aff-ae7f-4672-b748-05138f7e341d','household_intake_tab',10)
ON CONFLICT ("tab_id") DO UPDATE SET
  "form_id" = EXCLUDED."form_id",
  "tab_label" = EXCLUDED."tab_label",
  "tab_order" = EXCLUDED."tab_order";
