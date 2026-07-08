# ShowroomFlow Autopilot v1

Autopilot v1 genera un Reel verticale `1080x1920` usando asset locali canonici o `canon_candidate`.

Output giornaliero:

```text
outputs/autopilot/daily/YYYY-MM-DD/reel.mp4
outputs/autopilot/daily/YYYY-MM-DD/cover.png
outputs/autopilot/daily/YYYY-MM-DD/caption.md
outputs/autopilot/daily/YYYY-MM-DD/hashtags.md
```

## Requisiti

1. Python 3.
2. FFmpeg installato e disponibile nel terminale.

Verifica FFmpeg:

```powershell
ffmpeg -version
```

Se il comando non funziona, installare FFmpeg e aggiungerlo al `PATH`.

## Asset Usati

Autopilot legge questi asset:

```text
assets/environments/boutique_laura_fashion/reference/
assets/props/app_screens/
assets/brand/end_cards/
assets/brand/backgrounds/
```

La musica e' opzionale. Se vuoi una musica di background, metti un file `.mp3`, `.wav`, `.m4a` o `.aac` in:

```text
assets/brand/music/
```

## Comando Rapido

Dalla root del repository:

```powershell
python autopilot/scripts/autopilot.py
```

Per generare un giorno specifico:

```powershell
python autopilot/scripts/autopilot.py --date 2026-07-08
```

Per controllare il piano senza creare il video:

```powershell
python autopilot/scripts/autopilot.py --dry-run --date 2026-07-08
```

## Template

Il template principale e':

```text
autopilot/templates/daily_reel_v1.yaml
```

Da qui puoi cambiare:

- durata delle clip;
- testi overlay;
- caption;
- hashtag;
- volume musica;
- ordine degli asset;
- zoom e pan automatici sulle immagini.

La durata totale del Reel deve restare tra 12 e 18 secondi.

## Regole Pratiche

- I video riutilizzabili vanno in `assets/`.
- Le schermate app vanno in `assets/props/app_screens/`.
- Le end card ufficiali vanno in `assets/brand/end_cards/`.
- Gli sfondi ufficiali vanno in `assets/brand/backgrounds/`.
- Non serve CapCut.
- Non serve internet.
- FFmpeg crea direttamente il file `reel.mp4`.

## Output Finale

Dopo il comando, apri la cartella del giorno:

```text
outputs/autopilot/daily/YYYY-MM-DD/
```

Troverai:

- `reel.mp4`: video verticale pronto per social;
- `cover.png`: immagine copertina;
- `caption.md`: testo descrizione;
- `hashtags.md`: hashtag pronti.
