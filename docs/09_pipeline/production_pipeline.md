# Production Pipeline

## Pipeline Generale

1. Definizione episodio.
2. Script.
3. Shot list.
4. Prompt immagini.
5. Keyframe e storyboard visivo.
6. Prompt video per clip brevi.
7. Generazione clip.
8. Montaggio.
9. Voice-over, musica e sound design.
10. Controllo continuita'.
11. Approvazione Stefano.
12. Export.
13. Archiviazione asset approvati.

## Regola Principale

Non generare mai un episodio completo in un solo prompt video.

Ogni clip deve essere breve, controllabile e coerente.

## Stati

- `draft`: bozza iniziale;
- `in_review`: da controllare;
- `approved`: approvato;
- `archived`: superato o scartato.

## Cartelle

- Documenti episodio: `docs/06_episodes/episode_XXX/`
- Prompt: `docs/07_prompts/`
- Asset approvati: `assets/`
- Clip e export: `video/episode_XXX/`
- Esperimenti: `archive/experiments/`
