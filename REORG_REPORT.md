# Reorg Report

Date: 2026-07-08

## Objective

Riorganizzare ShowroomFlowUniverse come Generative Asset Library + Autopilot Lab.

## Structural Changes

- Creato `assets/` come centro canonico degli asset condivisi.
- Creato `episodes/season_01/episode_001/` con soli file ammessi: script, timeline, caption, hashtags, source assets, lessons learned, export.
- Spostato il codice Autopilot in `autopilot/scripts/`.
- Spostati i render Autopilot in `outputs/autopilot/daily/`.
- Spostate le vecchie strutture produttive in `archive/deprecated/`.
- Spostati i file dubbi in `archive/review_queue/`.
- Spostata la documentazione canonica in `docs/creative_bible/`, `docs/production_pipeline/`, `docs/prompts/`.

## Files Moved

### Autopilot

- `tools/autopilot/autopilot.py` -> `autopilot/scripts/autopilot.py`
- `README_AUTOPILOT.md` -> `autopilot/README.md`
- `video/autopilot/daily/2026-07-08/*` -> `outputs/autopilot/daily/2026-07-08/*`

### Brand Assets

- `video/episode_001/assets/brand/end_cards/final_slide.png` -> `assets/brand/end_cards/showroomflow_end_card_experience_v1.png`
- `video/episode_001/assets/app/sfondo_nero.png` -> `assets/brand/backgrounds/showroomflow_black_background_v1.png`

### App Screens

- `video/episode_001/assets/app/Immagine 2026-07-03 103927.jpg` -> `assets/props/app_screens/showroomflow_brand_list_v1.jpg`
- `video/episode_001/assets/app/Immagine 2026-07-03 104031.jpg` -> `assets/props/app_screens/showroomflow_categories_oblo_v1.jpg`
- `video/episode_001/assets/app/Immagine 2026-07-03 105739.jpg` -> `assets/props/app_screens/showroomflow_look_sculpted_brutalism_v1.jpg`
- `video/episode_001/assets/app/Immagine 2026-07-03 105807.jpg` -> `assets/props/app_screens/showroomflow_mix_match_look_items_v1.jpg`
- `video/episode_001/assets/app/vetrina1.jpg` -> `assets/props/app_screens/showroomflow_vetrina_outfit_mode_v1.jpg`
- `video/episode_001/assets/app/vetrina2.jpg` -> `assets/props/app_screens/showroomflow_vetrina_editorial_mode_v1.jpg`

### Environment Assets

- `docs/03_environments/environment_001_laura_fashion/assets/images/exterior/environment_001_exterior_canon_v1.png` -> `assets/environments/boutique_laura_fashion/exterior/environment_exterior_canon_v1.png`
- `docs/03_environments/environment_001_laura_fashion/assets/images/exterior/environment_001_exterior_canon_v2.png` -> `assets/environments/boutique_laura_fashion/exterior/environment_exterior_canon_v2.png`
- `docs/03_environments/environment_001_laura_fashion/overview/concept_board_v1.png` -> `assets/environments/boutique_laura_fashion/reference/concept_board_v1.png`
- `video/episode_001/environment_tests/env001_laura_fashion_motion_test_001_kling_v1.mp4` -> `assets/environments/boutique_laura_fashion/reference/laura_fashion_motion_test_kling_v1.mp4`
- `video/episode_001/environment_tests/kling_20260702_VIDEO_Use_this_e_6096_0.mp4` -> `assets/environments/boutique_laura_fashion/deprecated/laura_fashion_motion_test_kling_raw_20260702_v1.mp4`

### Marco Rinaldi Assets

- `assets/characters/marco_rinaldi/poses/front.png` -> `assets/characters/marco_rinaldi/turnaround/front_000.png`
- `assets/characters/marco_rinaldi/poses/side.png` -> `assets/characters/marco_rinaldi/turnaround/side_090.png`
- `assets/characters/marco_rinaldi/poses/back.png` -> `assets/characters/marco_rinaldi/turnaround/back_180.png`
- `assets/characters/marco_rinaldi/poses/3_4_view.png` -> `assets/characters/marco_rinaldi/turnaround/three_quarter_045.png`
- `assets/characters/marco_rinaldi/poses/entra_nella_boutiche.png` -> `assets/characters/marco_rinaldi/poses/entra_nella_boutique.png`
- `assets/characters/marco_rinaldi/poses/esce_con_discrzione.png` -> `assets/characters/marco_rinaldi/poses/esce_con_discrezione.png`
- `assets/characters/marco_rinaldi/poses/esce_con_discrzione2.png` -> `assets/characters/marco_rinaldi/poses/esce_con_discrezione_02.png`
- `assets/characters/marco_rinaldi/poses/parla_con_garbo2.png` -> `assets/characters/marco_rinaldi/poses/parla_con_garbo_02.png`
- `assets/characters/marco_rinaldi/poses/marco.png` -> `assets/characters/marco_rinaldi/poses/standing_with_ipad_and_bag.png`
- Marco reference files renamed to descriptive `marco_*_reference_*` names.

### Episode Export

- `video/episode_001/exports/Episode_001_Reel_MVP.mp4` -> `episodes/season_01/episode_001/export/episode_001_reel_mvp_v1.mp4`

### Documentation

- `docs/00_manifesto/` -> `docs/creative_bible/manifesto/`
- `docs/01_bible/` -> `docs/creative_bible/bible/`
- `docs/02_characters/` -> `docs/creative_bible/characters/`
- `docs/03_environments/` -> `docs/creative_bible/environments/`
- `docs/04_props/` -> `docs/creative_bible/props/`
- `docs/07_prompts/` -> `docs/prompts/`
- `docs/08_brand/` -> `docs/creative_bible/brand/`
- `docs/09_pipeline/` -> `docs/production_pipeline/`

## Duplicates Consolidated

| Removed duplicate | Canonical file | SHA256 |
| --- | --- | --- |
| `video/episode_001/assets/video/env001_laura_fashion_motion_test_001_kling_v1.mp4` | `assets/environments/boutique_laura_fashion/reference/laura_fashion_motion_test_kling_v1.mp4` | `F803A1FABAFD83250FBE9E7C068F484FF7D0F994EBFD91C9846AF60C7B960844` |
| `05_episodes/season_01/episode_001/sequences/sequence_a_il_momento_giusto/poster_frames/s01e01_seqA_clip001_boutique_respira_poster_v1.png` | `assets/environments/boutique_laura_fashion/exterior/environment_exterior_canon_v2.png` | `6FD481B2F91C868DBF96A3CE9DFC43EA6B5D6A7550A79B1A790C0CC6C8282625` |

## Review Queue

- `archive/review_queue/chatgpt_image_2026_07_02_164830.png`

Reason: source name was generic and context was not sufficient to classify it as a canon asset.

## Problems Remaining

- No standalone logo asset was found for `assets/brand/logos/`.
- No dedicated visual asset was found for `assets/props/kit_prospezione/`.
- No QR code asset was found for `assets/props/qr_codes/`.
- Laura has no dedicated visual asset set yet.
- Vehicle folders are prepared but do not contain assets.
- Marco turnaround is incomplete against the required 8-view set.
- The raw Kling environment motion test remains `review_needed` and is kept out of the Autopilot input path.

## Next Steps

- Add standalone ShowroomFlow logo files to `assets/brand/logos/`.
- Create or import official QR assets.
- Produce canonical Laura reference assets and update `assets/characters/laura/manifest.yaml`.
- Complete Marco turnaround views.
- Review `archive/review_queue/chatgpt_image_2026_07_02_164830.png` and either classify it or deprecate it.
