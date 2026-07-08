# Autopilot Asset Contract

Autopilot puo' usare solo asset registrati nella Generative Asset Library.

## Allowed Sources

- `assets/characters/`
- `assets/environments/`
- `assets/vehicles/`
- `assets/props/`
- `assets/brand/`

## Status Rule

Ogni generazione video deve usare solo asset con status:

- `canon`
- `canon_candidate`

Gli asset `deprecated`, `review_needed` o presenti in `archive/` non sono input validi per Autopilot.

## Manifest Rule

Ogni asset usato da Autopilot deve essere semanticamente descritto nel `manifest.yaml` della sua entita':

- ruolo narrativo o produttivo;
- tipo di asset;
- vista, posa, espressione o funzione;
- tag utili alla generazione;
- limiti o note di uso;
- status canonico.

## Episode Rule

Gli episodi non forniscono asset ad Autopilot. Forniscono solo `source_assets.md`, export e note editoriali.
