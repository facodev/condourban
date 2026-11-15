"""Re-download real Play Store screenshots via google-play-scraper."""
from __future__ import annotations

import json
import time
import urllib.request
from pathlib import Path

from google_play_scraper import app as play_app
from google_play_scraper import search as play_search

ROOT = Path(__file__).resolve().parent
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36"

PACKAGES: dict[str, str] = {
    "Superlogica": "com.condor.superlogica",
    "TownSq": "br.socialcondo.app",
    "Group-Software": "br.com.comunidadesmobile_1",  # Group Com
    "uCondo": "br.com.ucondo.android",
    "Condomob": "agile.ti.mobile.condomob",
    "Residente-Online": "online.residente",
    "MyCond": "br.com.iplanner.mycondapp",
    "Winker": "br.com.winker",
    "Wecondo": "com.wecondo",
    "Seu-Condominio": "br.com.seucondominio",
    "Condfy": "br.com.condfy",
    "Condofy": "br.com.condofy",
    "Morador-Online": "br.app.mo.novomo",
    "Condominio-Dedicado": "br.com.condominiodedicado",
    # Condominizando / wCond — resolve via search
}


def download(url: str, dest: Path) -> Path:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = resp.read()
        ctype = (resp.headers.get("Content-Type") or "").lower()
    if "jpeg" in ctype or "jpg" in ctype or data[:3] == b"\xff\xd8\xff":
        dest = dest.with_suffix(".jpg")
    elif "webp" in ctype or data[:4] == b"RIFF":
        dest = dest.with_suffix(".webp")
    else:
        dest = dest.with_suffix(".png")
    dest.write_bytes(data)
    return dest


def clear_old(folder: Path) -> None:
    for p in folder.glob("02-app-*"):
        p.unlink()


def fetch_one(folder: str, package_id: str, max_shots: int = 6) -> dict:
    dest = ROOT / folder
    dest.mkdir(parents=True, exist_ok=True)
    clear_old(dest)
    info = play_app(package_id, lang="pt", country="br")
    shots = info.get("screenshots") or []
    icon = info.get("icon")
    saved = []
    # Prefer screenshots; if empty, skip (don't save icon as "app UI")
    for i, url in enumerate(shots[:max_shots], start=1):
        out = dest / f"02-app-{i:02d}.png"
        try:
            saved_path = download(url, out)
            saved.append(saved_path.name)
            print(f"  {folder}: {saved_path.name} ({saved_path.stat().st_size} bytes)")
        except Exception as e:
            print(f"  {folder}: FAIL {i}: {e}")
    meta = {
        "package_id": package_id,
        "title": info.get("title"),
        "developer": info.get("developer"),
        "play_url": f"https://play.google.com/store/apps/details?id={package_id}&hl=pt_BR",
        "screenshot_count_available": len(shots),
        "files": saved,
        "icon": icon,
        "source": "google-play-scraper",
    }
    (dest / "02-app-meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return meta


def resolve_wcond() -> str | None:
    for q in ["wCond Meu Condomínio", "wCond Novitatus", "Novitatus condomínio"]:
        try:
            hits = play_search(q, lang="pt", country="br", n_hits=5)
            print(f"wCond search {q!r}:")
            for h in hits:
                print(f"  - {h.get('appId')} | {h.get('title')} | {h.get('developer')}")
            if hits:
                # Prefer title containing wCond
                for h in hits:
                    title = (h.get("title") or "").lower()
                    if "wcond" in title or "novitatus" in (h.get("developer") or "").lower():
                        return h["appId"]
        except Exception as e:
            print(f"search fail: {e}")
    return None


def main() -> None:
    wcond = resolve_wcond()
    if wcond:
        PACKAGES["Condominizando"] = wcond
        print(f"Condominizando package: {wcond}")
    else:
        print("Condominizando: no Play package found — will note in README")

    results = {}
    for folder, pid in PACKAGES.items():
        print(f"\n=== {folder} ({pid}) ===")
        try:
            results[folder] = fetch_one(folder, pid)
            time.sleep(0.6)
        except Exception as e:
            print(f"  ERROR: {e}")
            results[folder] = {"error": str(e), "package_id": pid}

    if "Condominizando" not in PACKAGES:
        results["Condominizando"] = {
            "error": "no_play_listing",
            "note": "Usar mockups da landing / andro.io",
        }

    (ROOT / "_fetch_app_shots_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("\nDone.")


if __name__ == "__main__":
    main()
