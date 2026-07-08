# Repository Structure

ShowroomFlow Universe e' organizzato come Generative Asset Library + Autopilot Lab.

## Root

- `README.md`: descrizione generale.
- `AI_TEAM.md`: ruoli del team creativo e tecnico.
- `CONTRIBUTING.md`: regole di contribuzione.
- `DIRECTOR_GUIDE.md`: guida operativa per Codex.
- `PROJECT_STATUS.md`: stato operativo dello ShowroomFlow Creative Lab.
- `REORG_REPORT.md`: report dell'ultima riorganizzazione.
- `REPOSITORY_STRUCTURE.md`: logica delle cartelle.

## assets/

Centro canonico degli asset condivisi.

Ogni asset condiviso deve avere un solo posto ufficiale e deve essere descritto dal `manifest.yaml` della sua entita'.

Struttura:

- `brand/`: loghi, end card, backgrounds, colori e musica.
- `characters/`: personaggi, pose, espressioni, outfit, turnaround e reference.
- `environments/`: ambienti, exterior, interior, angles e reference.
- `vehicles/`: veicoli.
- `props/`: app screens, QR codes e Kit di Prospezione.
- `ASSET_INDEX.md`: indice umano della libreria.

## autopilot/

Contiene codice, template e configurazioni Autopilot.

Struttura:

- `scripts/`: script Python.
- `templates/`: template YAML.
- `configs/`: configurazioni opzionali.
- `README.md`: istruzioni operative.

Il codice Autopilot non deve contenere render o asset condivisi.

## outputs/

Contiene output generati.

Struttura:

- `autopilot/daily/YYYY-MM-DD/`: output giornalieri Autopilot.

## episodes/

Contiene solo documenti editoriali e export finali.

Ogni episodio puo' contenere solo:

- `script.md`;
- `timeline.md`;
- `caption.md`;
- `hashtags.md`;
- `source_assets.md`;
- `lessons_learned.md`;
- `export/`.

Gli episodi non devono contenere copie di asset condivisi.

## docs/

Contiene documentazione creativa e operativa.

- `creative_bible/`: manifesto, bible, personaggi, ambienti, props e brand.
- `production_pipeline/`: workflow, budget e pipeline.
- `prompts/`: prompt master e prompt di produzione.
- `agent_instructions/`: regole operative per agenti.


## data/

Contiene dati strutturati in YAML.

Uso previsto:

- indici macchina dei personaggi;
- stati canonici;
- metadati utili a generazione, prompt e automazioni future.

I file YAML non devono duplicare la documentazione narrativa completa.

## archive/

Contiene materiale non canonico o non piu' operativo.

Struttura:

- `experiments/`: esperimenti.
- `deprecated/`: vecchie strutture o asset deprecati.
- `review_queue/`: file dubbi da classificare.

## Regola Generale

Se un file e' un asset condiviso, va in `assets/`.

Se un file e' codice o template Autopilot, va in `autopilot/`.

Se un file e' output generato, va in `outputs/`.

Se un file e' parte editoriale di un episodio, va in `episodes/`.

Se un file e' documentazione creativa o operativa, va in `docs/`.

Se un file e' dato strutturato, va in `data/`.

Se un file e' dubbio, storico o sperimentale, va in `archive/`.
