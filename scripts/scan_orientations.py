import json
import os
import sys
import cv2
import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
JPG_DIR = os.path.join(REPO_ROOT, "jpg")


def analyze_image(path: str) -> dict:
    # Use imdecode with fromfile to handle any Unicode path safely on Windows
    data = np.fromfile(path, dtype=np.uint8)
    img = cv2.imdecode(data, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return {"error": "Cannot decode image"}

    h, w = img.shape[:2]
    # Central 80% crop
    y1, y2 = int(h * 0.1), int(h * 0.9)
    x1, x2 = int(w * 0.1), int(w * 0.9)
    crop = img[y1:y2, x1:x2]

    ch, cw = crop.shape[:2]
    scale = 1000.0 / max(ch, cw)
    if scale < 1.0:
        crop = cv2.resize(crop, (int(cw * scale), int(ch * scale)), interpolation=cv2.INTER_AREA)

    edges = cv2.Canny(crop, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=80, minLineLength=50, maxLineGap=10)

    if lines is None or len(lines) == 0:
        return {"w": w, "h": h, "horiz": 0, "vert": 0, "ratio": 0.0, "flagged": True, "reason": "No lines"}

    horiz = 0
    vert = 0
    for line in lines.reshape(-1, 4):
        lx1, ly1, lx2, ly2 = line
        angle = abs(np.degrees(np.arctan2(ly2 - ly1, lx2 - lx1)))
        if angle < 15.0 or angle > 165.0:
            horiz += 1
        elif 75.0 < angle < 105.0:
            vert += 1

    ratio = (horiz + 1) / (vert + 1)
    flagged = ratio < 1.5
    reason = f"ratio={ratio:.2f} (h={horiz}, v={vert})" if flagged else "ok"
    return {"w": w, "h": h, "horiz": horiz, "vert": vert, "ratio": round(ratio, 2), "flagged": flagged, "reason": reason}


def main():
    files = sorted(f for f in os.listdir(JPG_DIR) if f.lower().endswith(".jpg"))
    print(f"Scanning {len(files)} JPEGs in {JPG_DIR}...")

    flagged = []
    landscape = []
    for fname in files:
        fpath = os.path.join(JPG_DIR, fname)
        res = analyze_image(fpath)
        if res.get("w", 0) > res.get("h", 0):
            landscape.append((fname, res.get("w"), res.get("h"), res.get("ratio")))
        if res.get("flagged"):
            flagged.append((fname, res))

    print(f"Total scanned: {len(files)}")
    print(f"Landscape images (w > h): {len(landscape)}")
    if landscape:
        print("  Sample/all landscape:", [(x[0], f"{x[1]}x{x[2]}", f"ratio={x[3]}") for x in landscape[:20]])
    print(f"Flagged (ratio < 1.5 or No lines): {len(flagged)}")
    for fname, res in flagged:
        print(f"  FLAGGED: {fname} | {res.get('w')}x{res.get('h')} | {res.get('reason')}")

    boundaries = [files[0], files[len(files)//2], files[-1]]
    print("Boundary files:", boundaries)

    out_path = os.path.join(os.path.dirname(__file__), "orientation_report.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"total": len(files), "landscape": landscape, "flagged": flagged}, f, indent=2)
    print(f"Saved report to {out_path}")


if __name__ == "__main__":
    main()
