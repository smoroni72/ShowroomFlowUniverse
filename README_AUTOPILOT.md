# ShowroomFlow Autopilot v1

Autopilot v1 genera un Reel verticale `1080x1920` usando asset locali del repository.

Output giornaliero:

```text
video/autopilot/daily/YYYY-MM-DD/reel.mp4
video/autopilot/daily/YYYY-MM-DD/cover.png
video/autopilot/daily/YYYY-MM-DD/caption.md
video/autopilot/daily/YYYY-MM-DD/hashtags.md
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
video/episode_001/assets/video/
video/episode_001/assets/app/
assets/brand/end_cards/
assets/brand/backgrounds/
```

La musica e' opzionale. Se vuoi una musica di background, metti un file `.mp3`, `.wav`, `.m4a` o `.aac` in:

```text
video/episode_001/assets/music/
```

Nota: per compatibilita' con gli asset gia' presenti, la end card puo' essere presa anche da:

```text
video/episode_001/assets/brand/end_cards/
```

## Comando Rapido

Dalla root del repository:

```powershell
python tools/autopilot/autopilot.py
```

Per generare un giorno specifico:

```powershell
python tools/autopilot/autopilot.py --date 2026-07-08
```

Per controllare il piano senza creare il video:

```powershell
python tools/autopilot/autopilot.py --dry-run
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

- I video vanno in `video/episode_001/assets/video/`.
- Le schermate app vanno in `video/episode_001/assets/app/`.
- Le end card ufficiali vanno in `assets/brand/end_cards/`.
- Gli sfondi ufficiali vanno in `assets/brand/backgrounds/`.
- Non serve CapCut.
- Non serve internet.
- FFmpeg crea direttamente il file `reel.mp4`.

## Output Finale

Dopo il comando, apri la cartella del giorno:

```text
video/autopilot/daily/YYYY-MM-DD/
```

Troverai:

- `reel.mp4`: video verticale pronto per social;
- `cover.png`: immagine copertina;
- `caption.md`: testo descrizione;
- `hashtags.md`: hashtag pronti.
