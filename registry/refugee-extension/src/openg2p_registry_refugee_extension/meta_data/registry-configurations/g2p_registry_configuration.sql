INSERT INTO "public"."g2p_registry_configuration" (
  "configuration_id",
  "registry_name",
  "registry_logo",
  "registry_favicon",
  "registry_theme_id",
  "registry_language_id"
) VALUES (
  '844ec986-6ee0-4355-af13-8d0922a642be',
  'Refugee Registry (Uganda RPCMS)',
  NULL,
  NULL,
  NULL,
  'a0b1c2d3-e4f5-4678-9012-3456789abcde'
)
ON CONFLICT ("configuration_id") DO UPDATE SET
  "registry_name" = EXCLUDED."registry_name",
  "registry_logo" = EXCLUDED."registry_logo",
  "registry_favicon" = EXCLUDED."registry_favicon",
  "registry_theme_id" = EXCLUDED."registry_theme_id",
  "registry_language_id" = EXCLUDED."registry_language_id";
