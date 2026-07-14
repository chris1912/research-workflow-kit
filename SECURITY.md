# Security

Codex annotation: Created by Codex on 2026-07-15.

Never commit API keys, private manuscripts, patient data, unpublished results,
local model caches, or generated Word/PDF artifacts. Use environment variables
for provider credentials and review every evidence export before sharing it.

The adapters execute configured local commands without shell expansion. Keep
backend commands trusted and use a dedicated workspace for untrusted documents.
Report suspected credential exposure or provenance errors privately before
opening a public issue.

