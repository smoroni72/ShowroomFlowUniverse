# Contributing

Questo repository e' gestito come fonte della verita' dello ShowroomFlow Creative Lab.

## Principi

- Non aggiungere materiale casuale.
- Non modificare la direzione creativa senza richiesta.
- Separare sempre materiale canonico, asset candidati ed esperimenti.
- Scrivere file chiari, leggibili e versionabili.
- Evitare nomi ambigui come `final_finale_v2`.

## Formati

- Documentazione: Markdown.
- Dati strutturati: YAML.
- Asset visivi: PNG, JPG, SVG o formati nativi dello strumento.
- Video: clip brevi e versioni exportate in cartelle dedicate.

## Naming

Usare nomi stabili, leggibili e in snake case:

- `marco_rinaldi.md`
- `episode_001_storyboard.md`
- `marco_rinaldi_master_prompt.md`
- `clip_01_boutique_exterior.webm`

## Stato Dei Materiali

Gli stati consigliati sono:

- `draft`;
- `in_review`;
- `approved`;
- `archived`.

Gli esperimenti vanno in:

- `archive/experiments/`

Gli asset approvati vanno in:

- `assets/`

## Personaggi

Ogni personaggio canonico deve avere:

- scheda Markdown in `docs/02_characters/`;
- dati YAML in `data/characters/`;
- cartella asset in `assets/characters/`.

## Episodi

Ogni episodio deve avere:

- `script.md`;
- `shot_list.md`;
- `prompts.md`;
- `continuity_checklist.md`.

## Approvazione

Nessun asset o episodio va considerato finale senza approvazione di Stefano.

Le decisioni canoniche devono essere riflesse nei file Markdown e YAML pertinenti.
