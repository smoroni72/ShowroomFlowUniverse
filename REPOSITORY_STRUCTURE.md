# Repository Structure

ShowroomFlow Universe separa documentazione creativa, dati strutturati, asset, video ed esperimenti.

## Root

- `README.md`: descrizione generale, stato e roadmap.
- `AI_TEAM.md`: ruoli del team creativo e tecnico.
- `CONTRIBUTING.md`: regole di contribuzione.
- `DIRECTOR_GUIDE.md`: guida operativa per Codex.
- `PROJECT_STATUS.md`: stato operativo dello ShowroomFlow Creative Lab.
- `REPOSITORY_STRUCTURE.md`: logica delle cartelle.

## 05_episodes/

Contiene la produzione operativa degli episodi.

Ogni episodio deve essere indipendente e contenere tutto cio' che serve per portarlo da idea a pubblicazione.

Struttura:

- `templates/`: template produttivi per episodi, shot, prompt e director notes;
- `season_01/episode_001/`: Episode 001 in pre production;
- `season_01/episode_002/` - `episode_005/`: placeholder produttivi.

Ogni episodio contiene:

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

## docs/

Contiene la documentazione creativa canonica.

- `00_manifesto/`: manifesto narrativo e visione.
- `01_bible/`: Bible dello ShowroomFlow Universe.
- `02_characters/`: documentazione canonica dei personaggi, con template e cartelle dedicate.
- `03_environments/`: ambienti canonici.
- `04_props/`: oggetti narrativi e funzionali.
- `07_prompts/`: prompt master e prompt di produzione.
- `08_brand/`: guida stile, tono e regole visuali.
- `09_pipeline/`: pipeline produttiva e workflow di approvazione.

### docs/02_characters/

Contiene i template e una cartella dedicata per ogni personaggio canonico.

Struttura consigliata:

- `templates/`: template per core, profilo e sheet;
- `<character_slug>/CORE.md`: elementi immutabili e character lock;
- `<character_slug>/profile.md`: profilo narrativo;
- `<character_slug>/sheet.md`: scheda visuale e produttiva;
- `<character_slug>/bible/`: moduli di continuita' seriale.

## data/

Contiene dati strutturati in YAML.

Uso previsto:

- indici macchina dei personaggi;
- stati canonici;
- metadati utili a generazione, prompt e automazioni future.

I file YAML non devono duplicare la documentazione narrativa completa.

## assets/

Contiene asset approvati o candidati all'approvazione.

Struttura:

- `characters/`;
- `environments/`;
- `props/`;
- `brand/`.

Gli asset non approvati o sperimentali non devono stare qui.

## video/

Contiene materiale video condiviso o storico.

La produzione corrente degli episodi vive in `05_episodes/`.

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
