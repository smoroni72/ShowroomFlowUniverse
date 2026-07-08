# ShowroomFlow Universe

Repository ufficiale dello **ShowroomFlow Creative Lab**.

Questo repository non e' un normale progetto software. E' la fonte della verita' produttiva per l'universo narrativo, gli asset generativi, l'Autopilot Lab e i video della campagna di comunicazione di ShowroomFlow.

## Obiettivo

Costruire un universo narrativo seriale chiamato **ShowroomFlow Universe**.

L'obiettivo non e' produrre un singolo video pubblicitario, ma una campagna coerente di piccoli episodi animati, cartoon o cinematici, in cui gli stessi personaggi raccontano il valore di ShowroomFlow attraverso situazioni realistiche del mondo della rappresentanza moda.

ShowroomFlow e' una piattaforma digitale B2B per agenti di moda, showroom e boutique.

## Principio Fondamentale

Lo ShowroomFlow Creative Lab non produce documentazione.

Produce contenuti.

La documentazione esiste soltanto per rendere piu' veloce la produzione degli episodi.

## Filosofia Narrativa

Le storie migliori non iniziano con una vendita. Iniziano con il rispetto del tempo di una persona.

Payoff provvisorio:

> Lascia il tempo alla moda.

## Ruoli

- **Stefano Moroni**: Founder, Executive Producer, Product Owner.
- **ChatGPT**: Creative Director, Story Architect, Continuity Manager.
- **Codex**: Technical Director, Repository Engineer.
- **IA immagini**: Concept Artist, Character Designer.
- **IA video**: Video Department.
- **Montaggio**: Clipchamp per montaggi rapidi, DaVinci Resolve per output professionali.

## Stato Attuale

Stato: **Sprint 1 avviato**.

Focus dello Sprint 1:

- consolidare la Generative Asset Library;
- mantenere un solo posto ufficiale per ogni asset;
- rendere Autopilot v1 capace di generare Reel verticali da asset locali;
- preparare Episode 001 per la pubblicazione usando solo riferimenti ad asset condivisi.

## Struttura

La struttura del repository e' descritta in:

- `REPOSITORY_STRUCTURE.md`

Cartelle principali:

- `assets/`: Generative Asset Library centrale;
- `autopilot/`: codice, template e configurazioni Autopilot;
- `outputs/`: render Autopilot e altri output generati;
- `episodes/`: script, timeline, caption, hashtag, source assets, lessons learned ed export finali;
- `docs/`: creative bible, pipeline, prompt e istruzioni agenti;
- `data/`: dati strutturati in YAML;
- `archive/`: esperimenti, materiale deprecato e file in review.

## Production Pipeline

Ogni episodio segue sempre questo flusso:

Idea

Story

Storyboard

Director Notes

Shot List

Production Prompts

Image Assets

Video Clips

Editing

Published Episode

## Season 01

- [Episode 001 - Il momento giusto](episodes/season_01/episode_001/script.md): `Pre Production`
- Episode 002: `Reserved`
- Episode 003: `Reserved`
- Episode 004: `Reserved`
- Episode 005: `Reserved`

## Struttura Character Canon

Ogni personaggio puo' avere documentazione creativa in `docs/creative_bible/characters/` e asset generativi in `assets/characters/`.

Per Marco Rinaldi `CHR-001` la documentazione creativa e':

- `CORE.md`: protegge Marco e contiene solo elementi immutabili;
- `profile.md`: racconta Marco dal punto di vista narrativo;
- `sheet.md`: rende Marco producibile per immagini, storyboard e video;
- `bible/`: rende Marco seriale attraverso moduli di continuita';
- `assets/characters/marco_rinaldi/manifest.yaml`: descrive semanticamente gli asset;
- `data/characters/marco_rinaldi.yaml`: resta un indice macchina, non un doppione narrativo.

## Roadmap Sprint 1

Deliverable:

- repository ordinato;
- `AI_TEAM.md`;
- `README.md`;
- manifesto narrativo;
- Bible iniziale;
- Marco Rinaldi structured character canon;
- Marco Rinaldi YAML machine index;
- Episode 001 canonical folder;
- Episode 001 shot list;
- Episode 001 continuity checklist;
- prompt master iniziale per Marco Rinaldi.

## Regole Base

- Questo repository e' la fonte della verita'.
- Le decisioni creative canoniche arrivano dal Creative Director e da Stefano.
- Codex organizza, versiona e rende operative le specifiche.
- Gli esperimenti vanno in `archive/experiments/`.
- Gli asset approvati o candidati vanno in `assets/`.
- Ogni episodio deve essere indipendente.
- Ogni prompt deve essere indipendente.
- Ogni asset deve essere collegato ai riferimenti canonici.
- Ogni episodio deve contenere solo script, timeline, caption, hashtags, source assets, lessons learned ed export.
- Ogni asset condiviso deve avere un solo posto ufficiale.
- Lo stato canonico degli asset vive nei `manifest.yaml`.
