#!/usr/bin/env python3
"""Genera le immagini degli appartamenti con Pollinations.ai (gratuito, senza API key).

Riusa proprietà, stanze e prompt definiti in generate_nano_banana_images.py, così i
nomi file restano identici a quelli referenziati nel front matter dei .md.

Uso:
    python3 generate_pollinations_images.py                       # tutte le mancanti
    python3 generate_pollinations_images.py --only firenze-centro # una sola
    python3 generate_pollinations_images.py --force               # sovrascrive
"""

from __future__ import annotations

import argparse
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

from generate_nano_banana_images import (
    OUTPUT_DIR,
    PROPERTIES,
    ROOMS,
    build_prompt,
    filename_for,
    save_webp,
)

POLLINATIONS_URL = "https://image.pollinations.ai/prompt/{prompt}"
WIDTH, HEIGHT = 1280, 720  # 16:9
MODEL = "flux"


def fetch_image(prompt: str, seed: int) -> bytes:
    params = urllib.parse.urlencode(
        {"width": WIDTH, "height": HEIGHT, "seed": seed, "model": MODEL, "nologo": "true"}
    )
    url = POLLINATIONS_URL.format(prompt=urllib.parse.quote(prompt)) + "?" + params
    req = urllib.request.Request(url, headers={"User-Agent": "greenproperty-imagegen/1.0"})
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = resp.read()
    if not data or len(data) < 1000:
        raise RuntimeError(f"risposta troppo piccola ({len(data)} byte)")
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--only", default=None, help="Genera solo lo slug indicato")
    parser.add_argument("--force", action="store_true", help="Sovrascrive le immagini esistenti")
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    props = [p for p in PROPERTIES if args.only is None or p.slug == args.only]
    if not props:
        print(f"❌ Nessuna proprietà con slug '{args.only}'.")
        sys.exit(1)

    total = len(props) * len(ROOMS)
    done = 0
    errors = 0
    for prop in props:
        print(f"\n🏠 {prop.name}")
        for idx, room in enumerate(ROOMS):
            done += 1
            dest = OUTPUT_DIR / filename_for(prop, room)
            if dest.exists() and not args.force:
                print(f"   [{done}/{total}] ⏭️  esiste già: {dest.name}")
                continue
            print(f"   [{done}/{total}] 🎨 {room.suffix} → {dest.name}")
            try:
                # seed deterministico ma diverso per ogni stanza
                seed = (abs(hash(prop.slug)) % 100000) + idx
                img = fetch_image(build_prompt(prop, room), seed)
                save_webp(img, dest)
                print("            ✅ salvata")
                time.sleep(2)  # gentile col servizio gratuito
            except urllib.error.HTTPError as exc:
                errors += 1
                print(f"            ❌ HTTP {exc.code}: {exc.read().decode('utf-8', 'replace')[:200]}")
            except Exception as exc:  # noqa: BLE001 - CLI: continuare in caso di errore
                errors += 1
                print(f"            ❌ Errore: {exc}")

    print(f"\n✨ Fatto. Generate/aggiornate: {done - errors}/{total} (errori: {errors})")
    print(f"📁 Output: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
