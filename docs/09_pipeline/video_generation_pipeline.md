# Video Generation Pipeline

## Principio

Le IA video devono generare clip brevi da 3-5 secondi.

Ogni clip deve corrispondere a uno shot preciso della shot list.

## Workflow

1. Scegliere una clip dalla shot list.
2. Preparare keyframe o immagine di riferimento.
3. Scrivere prompt video specifico.
4. Generare clip breve.
5. Valutare:
   - continuita' personaggio;
   - coerenza outfit;
   - ambiente;
   - gesto;
   - camera;
   - assenza di errori evidenti.
6. Salvare clip candidate.
7. Spostare clip approvate in `video/episode_XXX/clips/`.
8. Montare.

## Regole Prompt Video

- Uno shot per prompt.
- Una sola azione principale.
- Camera chiara.
- Durata breve.
- Nessun cambio drastico di ambiente.
- Nessun cambio outfit non richiesto.
- Nessun gesto aggressivo.

## Controllo

Ogni clip deve passare dalla checklist di continuita' dell'episodio.
