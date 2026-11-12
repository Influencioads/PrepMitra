"""Lists the finished question files for viewer/index.html.

Merged batches are listed as merged; finished subject parts and package fragments of later batches as "not merged
yet". Parts already inside a merged batch, and package fragments whose package has not finished, are left out.

    python tools/build_viewer_index.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# package fragments whose package finished and passed validation; others may still be partial
FINISHED_PACKAGES = []  # every finished package is joined into its part file


def main():
    batches = ROOT / "batches"
    merged = sorted(p for p in batches.glob("BATCH_0*.json"))
    merged_ids = {p.stem[:9] for p in merged}
    files = [{"path": f"../batches/{p.name}", "label": p.stem.replace("_", " "), "status": "merged"} for p in merged]
    for p in sorted((batches / "parts").glob("BATCH_0*_*.json")):
        if p.stem[:9] not in merged_ids:
            files.append({"path": f"../batches/parts/{p.name}", "label": p.stem.replace("_", " "),
                          "status": "not merged yet"})
    for pkg in FINISHED_PACKAGES:
        for p in sorted((batches / "parts" / "frag").glob(f"*_{pkg}.json")):
            files.append({"path": f"../batches/parts/frag/{p.name}", "label": p.stem.replace("_", " "),
                          "status": "not merged yet"})
    out = ROOT / "viewer" / "index.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps({"files": files}, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {out} ({len(files)} files)")


if __name__ == "__main__":
    main()
