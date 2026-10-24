#!/usr/bin/env bash
# Rebuild the whole JOMO 3D character set from scratch, stage by stage, then export and render checks.
# Usage: bash blender/scripts/build_all.sh [--no-previews]
set -euo pipefail
cd "$(dirname "$0")/../.."
for s in s1_mesh s2_rig s3_skin s4_materials s5_animations s6_export; do
  echo "== $s"; python3 "blender/scripts/$s.py" > /dev/null
done
python3 blender/scripts/uv_check.py blender/work/stage4.blend stage4 | grep -v " 0 overlapping" || true
python3 blender/scripts/verify_export.py | grep -E "bones|actions"
if [ "${1:-}" != "--no-previews" ]; then
  python3 blender/scripts/preview_anim.py blender/work/stage5.blend sheet > /dev/null
  python3 blender/scripts/preview_anim.py blender/work/stage5.blend mp4 > /dev/null
fi
echo "done"
