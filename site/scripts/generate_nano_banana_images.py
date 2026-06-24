#!/usr/bin/env python3
"""Genera le immagini degli appartamenti con Gemini "Nano Banana" (gemini-2.5-flash-image).

Per ogni proprietà crea 5 immagini: ingresso, soggiorno, camera da letto, bagno, cucina.
I nomi dei file corrispondono esattamente ai path nel front matter dei .md in
content/italian/booking/ (es. images/apartments/firenze-centro-ingresso.webp).

Requisiti:
    pip install pillow            # per salvare in formato WebP
    export GEMINI_API_KEY=...     # oppure GOOGLE_API_KEY
    (chiave da https://aistudio.google.com/apikey)

Uso:
    # Solo prompt, NESSUNA chiamata API (genera scripts/property_image_prompts.md):
    python3 generate_nano_banana_images.py --prompts-only

    # Genera tutte le immagini mancanti:
    python3 generate_nano_banana_images.py

    # Solo una proprietà, sovrascrivendo le esistenti:
    python3 generate_nano_banana_images.py --only milano-sempione --force
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path

# --- Configurazione modello -------------------------------------------------

DEFAULT_MODEL = "gemini-2.5-flash-image"
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

# Cartella di output (relativa a questo script: site/assets/images/apartments).
# In assets/ perché Hugo genera da lì le varianti responsive (pipeline immagini).
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "assets" / "images" / "apartments"
PROMPTS_FILE = Path(__file__).resolve().parent / "property_image_prompts.md"


# --- Dati delle proprietà ---------------------------------------------------


@dataclass(frozen=True)
class Property:
    slug: str
    name: str
    style: str  # descrizione di stile/contesto in inglese (migliore resa del modello)


PROPERTIES: tuple[Property, ...] = (
    # Stile comune: Airbnb neutro di fascia media, palette neutra calda, parquet chiaro,
    # ordinato e luminoso, con UN solo accento di design per stanza. Non lussuoso, non spartano.
    Property(
        "firenze-centro",
        "Firenze Centro",
        "a neutral, tastefully furnished mid-range Airbnb apartment in a historic building in the "
        "centre of Florence, clean contemporary look, warm neutral palette, light wood floor, "
        "uncluttered and bright, with a single tasteful design accent as the focal point of the "
        "room (a designer lamp, a framed print or one accent chair); not luxurious, not cheap",
    ),
    Property(
        "firenze-lungarno",
        "Firenze Lungarno",
        "a neutral, tastefully furnished mid-range Airbnb apartment on a high floor overlooking the "
        "Arno river in Florence, clean contemporary look, warm neutral palette, light wood floor, "
        "uncluttered and bright, large windows framing a realistic rooftop view of the Arno and "
        "Florentine terracotta roofs with soft natural daylight, with a single tasteful design "
        "accent as the focal point of the room (a designer lamp, a framed print or one accent "
        "chair); not luxurious, not cheap, photorealistic interior photography",    ),
    Property(
        "bologna-centro",
        "Bologna Centro",
        "a neutral, tastefully furnished mid-range Airbnb apartment in the centre of Bologna, clean "
        "contemporary look, warm neutral palette, light wood floor, uncluttered and bright, with a "
        "single tasteful design accent as the focal point of the room (a designer lamp, a framed "
        "print or one accent chair); not luxurious, not cheap",
    ),
    Property(
        "milano-sempione",
        "Milano Sempione",
        "a neutral, tastefully furnished mid-range Airbnb apartment in Milan, modern and clean style "
        "look, cold neutral, light gres floor, uncluttered and brilliant, with a single "
        "tasteful design accent as the focal point of the room (e.g. a designer lamp, a framed "
        "print or one accent chair); not luxurious, not cheap",
    ),
    Property(
        "milano-stazione-centrale",
        "Milano Stazione Centrale",
        "a modern mid-range Airbnb apartment near Milano Centrale station, contemporary Italian design, "
        "open and airy living space with floor-to-ceiling windows and soft natural daylight, "
        "warm neutral palette (greige, sand, off-white) accented by matte black or brushed-brass details, "
        "light oak engineered flooring, minimalist low-profile furniture with clean lines, "
        "a few architectural plants for warmth, uncluttered surfaces, "
        "a single statement design piece as the focal point of the room (a sculptural designer floor lamp, "
        "a large framed art print, or an accent armchair in a muted bouclé), "
        "cozy yet refined, professionally styled, realistic interior photography, wide-angle, soft shadows; "
        "not luxurious, not cheap, no clutter",
        ),
    Property(
        "milano-corso-lodi",
        "Milano Corso Lodi",
        "a neutral, tastefully furnished mid-range Airbnb apartment in Milan, clean contemporary "
        "look, warm neutral palette, pale microcement or large-format stone-look tile flooring with "
        "just a hint of light wood as a warm accent, uncluttered and bright, with a single tasteful "
        "design accent as the focal point of the room (a designer lamp, a framed print or one accent "
        "chair); not luxurious, not cheap",
    ),
    Property(
        "milano-viale-monza",
        "Milano Viale Monza",
        "a neutral, tastefully furnished mid-range Airbnb apartment in Milan, raw industrial-leaning "
        "contemporary look, warm neutral palette with exposed concrete, bare brick or rough plaster "
        "walls, visible ceiling beams or ductwork, polished concrete or worn wood floor, uncluttered "
        "and bright, with a single tasteful design accent as the focal point of the room (a designer "
        "lamp, a framed print or one accent chair); not luxurious, not cheap, lived-in and authentic",
    ),
    Property(
        "milano-via-palermo",
        "Milano Via Palermo",
        "a neutral, tastefully furnished mid-range Airbnb apartment in the Brera district of Milan, "
        "clean contemporary look with a subtle bohemian touch, warm neutral palette with a few earthy "
        "terracotta or ochre accents, light wood floor, a soft textured rug and a couple of potted "
        "plants, uncluttered and bright, with a single tasteful design accent as the focal point of "
        "the room (a woven pendant lamp, a framed print or one rattan accent chair); not luxurious, "
        "not cheap",
    ),
    Property(
        "milano-via-palestro",
        "Milano Via Palestro",
        "an elegant, tastefully furnished mid-range Airbnb apartment near the public gardens in "
        "Milan, refined contemporary look with a fashion-editorial mood, warm neutral palette with "
        "chic black-and-white accents, light wood floor, uncluttered and bright, framed runway and "
        "fashion photography prints on the walls, a sleek mannequin or a curated rack of designer "
        "garments as a subtle styling detail, with a single tasteful design accent as the focal "
        "point of the room (a sculptural designer lamp, a large fashion print or one velvet accent "
        "chair); not luxurious, not cheap",
    ),
)


@dataclass(frozen=True)
class Room:
    suffix: str  # suffisso del nome file (corrisponde al front matter)
    name_en: str  # nome stanza in inglese per il prompt
    details: str  # dettagli specifici della stanza


ROOMS: tuple[Room, ...] = (
    Room(
        "ingresso",
        "entrance hall",
        "a welcoming entryway with a console table, a large framed mirror, coat hooks, tasteful "
        "decor and warm inviting lighting",
    ),
    Room(
        "soggiorno",
        "living room",
        "a comfortable living room with a stylish sofa, a coffee table, a smart TV, soft lighting "
        "and decorative details",
    ),
    Room(
        "camera",
        "bedroom",
        "a cozy bedroom with a neatly made double bed with quality white linens, bedside tables "
        "with lamps and a wardrobe",
    ),
    Room(
        "bagno",
        "bathroom",
        "a clean modern bathroom with a walk-in glass shower, a vanity with mirror, neatly folded "
        "towels and elegant fixtures",
    ),
    Room(
        "cucina",
        "kitchen",
        "a fully equipped modern kitchen with cabinets, built-in appliances, a clean countertop "
        "and a small dining area",
    ),
)


def build_prompt(prop: Property, room: Room) -> str:
    """Costruisce il prompt fotorealistico per una singola stanza."""
    return (
        f"Professional real estate interior photography of the {room.name_en} of {prop.style}. "
        f"The room features {room.details}. "
        "Photorealistic, realistic and welcoming, bright natural daylight, wide-angle lens, "
        "clean and tidy holiday-rental listing photo, landscape 16:9 composition, "
        "no people, no text, no watermark."
    )


def filename_for(prop: Property, room: Room) -> str:
    return f"{prop.slug}-{room.suffix}.webp"


# --- Generazione prompt (no API) -------------------------------------------


def write_prompts_file() -> None:
    lines: list[str] = [
        "# Prompt immagini proprietà — Gemini Nano Banana",
        "",
        f"Modello consigliato: `{DEFAULT_MODEL}`",
        "",
        "Per ogni proprietà, 5 immagini: ingresso, soggiorno, camera da letto, bagno, cucina.",
        "",
    ]
    for prop in PROPERTIES:
        lines.append(f"## {prop.name} (`{prop.slug}`)")
        lines.append("")
        for room in ROOMS:
            lines.append(f"### {room.suffix} → `{filename_for(prop, room)}`")
            lines.append("")
            lines.append("```")
            lines.append(build_prompt(prop, room))
            lines.append("```")
            lines.append("")
    PROMPTS_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ Prompt scritti in: {PROMPTS_FILE}")
    print(f"   {len(PROPERTIES)} proprietà × {len(ROOMS)} stanze = "
          f"{len(PROPERTIES) * len(ROOMS)} immagini")


# --- Chiamata API Gemini ----------------------------------------------------


def load_env_file() -> None:
    """Carica le variabili da site/.env nell'ambiente (se non già impostate)."""
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if not env_path.exists():
        return
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, _, value = line.partition("=")
        name, value = name.strip(), value.strip().strip('"').strip("'")
        if name and value and name not in os.environ:
            os.environ[name] = value


def get_api_key() -> str:
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        print("❌ ERRORE: GEMINI_API_KEY (o GOOGLE_API_KEY) non impostata.")
        print("   Ottieni una chiave su https://aistudio.google.com/apikey")
        print("   poi: export GEMINI_API_KEY=la_tua_chiave")
        sys.exit(1)
    return key


def call_nano_banana(prompt: str, api_key: str, model: str) -> bytes:
    """Chiama l'API e restituisce i byte PNG dell'immagine generata."""
    url = API_URL.format(model=model)
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["IMAGE"]},
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json", "x-goog-api-key": api_key},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        body = json.loads(resp.read().decode("utf-8"))

    candidates = body.get("candidates") or []
    for cand in candidates:
        for part in cand.get("content", {}).get("parts", []):
            inline = part.get("inlineData") or part.get("inline_data")
            if inline and inline.get("data"):
                return base64.b64decode(inline["data"])
    raise RuntimeError(f"Nessuna immagine nella risposta: {json.dumps(body)[:400]}")


# Le immagini sorgente vengono salvate già ottimizzate per il web.
# Hugo (pipeline in assets/) genera poi le varianti responsive più piccole.
MAX_WIDTH = 1000
WEBP_QUALITY = 80


def save_webp(png_bytes: bytes, dest: Path) -> None:
    try:
        from PIL import Image
    except ImportError:
        print("❌ Pillow non installato. Esegui: pip install pillow")
        sys.exit(1)
    img = Image.open(BytesIO(png_bytes)).convert("RGB")
    if img.width > MAX_WIDTH:
        img = img.resize((MAX_WIDTH, round(img.height * MAX_WIDTH / img.width)), Image.LANCZOS)
    dest.parent.mkdir(parents=True, exist_ok=True)
    img.save(dest, "WEBP", quality=WEBP_QUALITY, method=6)


def generate_images(only: str | None, force: bool, model: str) -> None:
    api_key = get_api_key()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    props = [p for p in PROPERTIES if only is None or p.slug == only]
    if not props:
        print(f"❌ Nessuna proprietà con slug '{only}'.")
        sys.exit(1)

    total = len(props) * len(ROOMS)
    done = 0
    errors = 0
    for prop in props:
        print(f"\n🏠 {prop.name}")
        for room in ROOMS:
            done += 1
            dest = OUTPUT_DIR / filename_for(prop, room)
            if dest.exists() and not force:
                print(f"   [{done}/{total}] ⏭️  esiste già: {dest.name}")
                continue
            prompt = build_prompt(prop, room)
            print(f"   [{done}/{total}] 🎨 {room.suffix} → {dest.name}")
            try:
                png = call_nano_banana(prompt, api_key, model)
                save_webp(png, dest)
                print(f"            ✅ salvata")
                time.sleep(1)  # gentile col rate limit
            except urllib.error.HTTPError as exc:
                errors += 1
                detail = exc.read().decode("utf-8", "replace")[:300]
                print(f"            ❌ HTTP {exc.code}: {detail}")
            except Exception as exc:  # noqa: BLE001 - CLI: vogliamo continuare
                errors += 1
                print(f"            ❌ Errore: {exc}")

    print(f"\n✨ Fatto. Generate/aggiornate: {done - errors}/{total} (errori: {errors})")
    print(f"📁 Output: {OUTPUT_DIR}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--prompts-only", action="store_true",
                        help="Scrive solo il file dei prompt, senza chiamare l'API")
    parser.add_argument("--only", default=None, help="Genera solo lo slug indicato (es. milano-sempione)")
    parser.add_argument("--force", action="store_true", help="Sovrascrive le immagini esistenti")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Modello (default: {DEFAULT_MODEL})")
    args = parser.parse_args()

    if args.prompts_only:
        write_prompts_file()
        return
    load_env_file()
    generate_images(only=args.only, force=args.force, model=args.model)


if __name__ == "__main__":
    main()
