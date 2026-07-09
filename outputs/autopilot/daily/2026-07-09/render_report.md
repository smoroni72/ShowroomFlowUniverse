# Render Report

episode: episode_002
validation_result: passed
missing_assets: none
planned_duration_seconds: 20
render_elapsed_seconds: 17.30
output_reel: outputs/autopilot/daily/2026-07-09/reel.mp4
output_cover: outputs/autopilot/daily/2026-07-09/cover.png

## Assets Used
- environment: boutique_laura_fashion -> assets/environments/boutique_laura_fashion/exterior/environment_exterior_canon_v1.png
- environment: boutique_laura_fashion -> assets/environments/boutique_laura_fashion/interior/interior_entrance.png
- actor: marco_rinaldi -> assets/characters/marco_rinaldi/turnaround/front_000.png
- environment: boutique_laura_fashion -> assets/environments/boutique_laura_fashion/interior/interior_central_area_1.png
- actor: laura -> assets/characters/laura/expressions/01_sorriso_leggero.png
- actor: marco_rinaldi -> assets/characters/marco_rinaldi/expressions/01_sorriso_leggero.png
- actor: marco_rinaldi -> assets/characters/marco_rinaldi/poses/leave_kit_on_desk.png
- actor: laura -> assets/characters/laura/expressions/05_curiosita.png
- prop: kit_prospezione -> assets/characters/marco_rinaldi/poses/leave_kit_on_desk.png
- prop: showroomflow_end_card -> assets/brand/end_cards/showroomflow_end_card_experience_v1.png

## Warnings
- kit_prospezione manifest has no dedicated visual asset; S007 uses the explicit render-plan asset path already present in assets/.
- Laura manifest has empty expression metadata, but the explicit Laura expression image paths exist in assets/.
- Temporary render work directory cleanup reported access denied after output generation: outputs/autopilot/daily/2026-07-09/.work_episode_002

## FFprobe
```json
{
  "programs": [],
  "stream_groups": [],
  "streams": [
    {
      "width": 1080,
      "height": 1920,
      "r_frame_rate": "30/1"
    }
  ],
  "format": {
    "duration": "20.000000"
  }
}
```
