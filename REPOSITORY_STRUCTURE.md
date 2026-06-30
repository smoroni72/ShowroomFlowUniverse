# Repository Structure

ShowroomFlow Universe separa documentazione creativa, dati strutturati, asset, video ed esperimenti.

## Root

- `README.md`: descrizione generale, stato e roadmap.
- `AI_TEAM.md`: ruoli del team creativo e tecnico.
- `CONTRIBUTING.md`: regole di contribuzione.
- `DIRECTOR_GUIDE.md`: guida operativa per Codex.
- `REPOSITORY_STRUCTURE.md`: logica delle cartelle.

## docs/

Contiene la documentazione creativa canonica.

- `00_manifesto/`: manifesto narrativo e visione.
- `01_bible/`: Bible dello ShowroomFlow Universe.
- `02_characters/`: schede personaggi.
- `03_environments/`: ambienti canonici.
- `04_props/`: oggetti narrativi e funzionali.
- `05_storyboards/`: storyboard testuali o visuali.
- `06_episodes/`: documenti di produzione per ogni episodio.
- `07_prompts/`: prompt master e prompt di produzione.
- `08_brand/`: guida stile, tono e regole visuali.
- `09_pipeline/`: pipeline produttiva e workflow di approvazione.

## data/

Contiene dati strutturati in YAML.

Uso previsto:

- personaggi;
- stati canonici;
- metadati utili a generazione, prompt e automazioni future.

## assets/

Contiene asset approvati o candidati all'approvazione.

Struttura:

- `characters/`;
- `environments/`;
- `props/`;
- `brand/`.

Gli asset non approvati o sperimentali non devono stare qui.

## video/

Contiene materiale di produzione video.

Ogni episodio ha:

- `clips/`: clip brevi generate;
- `exports/`: output montati;
- `project_files/`: file progetto di Clipchamp, DaVinci o altri strumenti.

## archive/

Contiene esperimenti, prove scartate e materiale non canonico.

Gli esperimenti vanno in:

- `archive/experiments/`

## Regola Generale

Se un file stabilisce una decisione creativa canonica, va in `docs/`.

Se un file e' dato strutturato, va in `data/`.

Se un file e' un asset approvato, va in `assets/`.

Se un file e' una clip o un progetto video, va in `video/`.

Se un file e' una prova, va in `archive/experiments/`.
