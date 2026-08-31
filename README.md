# cascade-site

The marketing site for Cascade (routing audit, KYC extraction).

- `docs/` — the built site, production names, ready for any static host.
  `index.html` is the single-screen hero; `method/security/questions/terms/
  privacy/accessibility.html` are the appendices; `contact`, `colophon`,
  `404` are the plumbing.
- `source/` — the full build chain: `batir-hero.py` and `batir-annexe.py`
  generate every page from the JSON content files; `releve.json` declares
  every figure displayed (the provenance gate refuses an undeclared one);
  `etats/` holds the Blender scripts that model and render the 3D objects,
  plus the crop pipeline; `assembler.py` rebuilds `docs/` from all of it.

Publishing is a separate decision: the `cascade-routing` repository's
`docs/` folder is *generated* by `npm run pages` and guarded by fingerprint
tests, so wiring this site into it is an operation inside that repository.
