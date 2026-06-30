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
- `episode_001`
- `S001_esterno_boutique.md`
- `marco_rinaldi_master_prompt.md`
- `clip_S001_esterno_boutique.webm`

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

- documentazione Markdown canonica in `docs/02_characters/<character_slug>/`;
- dati YAML in `data/characters/`;
- cartella asset in `assets/characters/`.

## Episodi

Ogni episodio deve avere:

- `README.md`;
- `storyboard.md`;
- `director_notes.md`;
- `shotlist.md`;
- `assets.md`;
- `prompts/images/`;
- `prompts/videos/`;
- `clips/`;
- `audio/`;
- `thumbnails/`;
- `final/`;
- `checklist.md`.

Ogni episodio deve essere indipendente.

Ogni prompt deve essere indipendente.

Ogni asset deve essere collegato ai riferimenti canonici.

`director_notes.md` e' riservato al Creative Director e non viene compilato automaticamente.

## Approvazione

Nessun asset o episodio va considerato finale senza approvazione di Stefano.

Le decisioni canoniche devono essere riflesse nei file Markdown e YAML pertinenti.
