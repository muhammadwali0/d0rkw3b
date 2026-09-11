# Investigations and recipes

```sh
d0rkw3b investigate example.com
d0rkw3b investigate alice --type username
d0rkw3b investigate alice@example.com --format json
d0rkw3b recipes list
d0rkw3b recipes info domain-footprint
d0rkw3b investigate example.com --recipe domain-footprint
d0rkw3b dev validate-recipes
```

Investigations normalize an entity, rank relevant provider queries, group paths
from actual categories or recipe stages, and attach observations/provenance.
No connector runs and no case is created. The default shows five queries per
stage; `--all` expands every matching enabled path. JSON carries the full plan
schema; CSV and Markdown project the generated queries to the existing row format.
Text and all projections identify paths as generated queries, not findings.
Use `--network tor` or `all` explicitly for Tor paths; no Tor connection is made.

Recipes are JSON data in `src/d0rkw3b/recipes/`. Fields: `id`, `name`, `description`,
`target_types`, `stages`. Each stage contains `name`, `description`, and exact
`providers` IDs. Unknown fields/providers, incompatible types, empty stages and
duplicate IDs/names are rejected. Additional files use repeated `--recipe-file`;
invalid entries get diagnostics without executing any code. Recipes reference
available providers only, with no implicit collection or speculative enrichment.

Current recipes: domain-footprint, username-footprint, email-footprint,
repository-investigation, document-provenance, image-provenance, and
organization-research. Image-provenance takes a public image **URL**, not a local
file; opening the resulting link would share that URL with the chosen service.
Document-provenance is indexed-document research, not local file analysis.
Organization research uses the existing company-name LinkedIn paths and can
require a login. None of these descriptions imply actual provider availability.

Interactive mode accepts these same commands and routes them through the same
API as the direct CLI. Legacy numbered query menus remain available.
