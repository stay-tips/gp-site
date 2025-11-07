#!/usr/bin/env python3
"""
Script automatico per creare appartamenti completi con immagini AI e file markdown

Funzionalità:
- Chiede numero di appartamenti da creare
- Genera immagini con Stable Diffusion 3.5 Large
- Output diretto in formato WebP
- Crea file markdown nella cartella booking
- Distribuisce geograficamente: 70% città principali, 30% borghi
- Appartamenti luxury: minimo 700€/notte
- Gestione errori: interrompe dopo 3 errori consecutivi

Requisiti:
    pip install replicate requests

Uso:
    python create_apartments.py
"""

import os
import sys
import random
import replicate
from pathlib import Path
import time
import requests

# Città principali (70% degli appartamenti)
MAJOR_CITIES = [
    {"name": "Milano", "lat": 45.464203, "lon": 9.189982, "zones": ["Duomo", "Navigli", "Brera", "Centrale", "Porta Romana", "Isola", "Porta Venezia"]},
    {"name": "Roma", "lat": 41.890221, "lon": 12.492348, "zones": ["Colosseo", "Trastevere", "Prati", "Monti", "Testaccio", "San Lorenzo"]},
    {"name": "Firenze", "lat": 43.773056, "lon": 11.256389, "zones": ["Duomo", "Ponte Vecchio", "Santa Croce", "Santo Spirito", "San Frediano"]},
    {"name": "Bologna", "lat": 44.499291, "lon": 11.335168, "zones": ["Centro", "Santo Stefano", "Saragozza", "Irnerio"]},
    {"name": "Torino", "lat": 45.070312, "lon": 7.686856, "zones": ["Centro", "Quadrilatero", "San Salvario", "Crocetta"]},
    {"name": "Verona", "lat": 45.438384, "lon": 10.991622, "zones": ["Arena", "Centro Storico", "Veronetta"]},
    {"name": "Padova", "lat": 45.406435, "lon": 11.876761, "zones": ["Centro", "Prato della Valle", "Santo"]},
]

# Borghi più belli d'Italia (30% degli appartamenti)
BEAUTIFUL_VILLAGES = [
    {"name": "Como", "region": "Lombardia", "lat": 45.808056, "lon": 9.085278},
    {"name": "Aosta", "region": "Valle d'Aosta", "lat": 45.737222, "lon": 7.315556},
    {"name": "Belluno", "region": "Veneto", "lat": 46.138889, "lon": 12.216667},
    {"name": "Civita di Bagnoregio", "region": "Lazio", "lat": 42.627778, "lon": 12.111944},
    {"name": "Alberobello", "region": "Puglia", "lat": 40.781944, "lon": 17.236944},
    {"name": "Manarola", "region": "Liguria", "lat": 44.107222, "lon": 9.730556},
    {"name": "San Gimignano", "region": "Toscana", "lat": 43.467778, "lon": 11.043056},
    {"name": "Orta San Giulio", "region": "Piemonte", "lat": 45.799167, "lon": 8.411111},
    {"name": "Spello", "region": "Umbria", "lat": 42.994167, "lon": 12.669444},
    {"name": "Castelmezzano", "region": "Basilicata", "lat": 40.526111, "lon": 16.052778},
    {"name": "Portofino", "region": "Liguria", "lat": 44.303056, "lon": 9.210556},
    {"name": "Tropea", "region": "Calabria", "lat": 38.676111, "lon": 15.897778},
    {"name": "Positano", "region": "Campania", "lat": 40.628056, "lon": 14.485},
]

# Stili per appartamenti normali (economici e funzionali)
NORMAL_STYLES = [
    "simple and clean", 
    "budget friendly cozy", 
    "basic modern", 
    "affordable contemporary",
    "simple scandinavian",
    "minimalist budget",
    "functional and practical",
    "economical modern"
]

# Stili per appartamenti di lusso
LUXURY_STYLES = ["medium luxury contemporary", "classic elegant", "high-end modern"]

ROOM_TYPES = [
    "living room",
    "kitchen",
    "bedroom",
    "bathroom",
    "dining area",
    "entrance hallway",
    "balcony view",
    "bedroom detail",
    "kitchen detail",
    "living room from different angle"
]

def sanitize_filename(name):
    """Sanitizza il nome file"""
    return "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in name).strip().lower().replace(' ', '-')

def generate_prompt(city, zone, style, room_type, is_luxury=False):
    """Genera prompt per Stable Diffusion"""
    location = f"{zone}, {city}" if zone else city
    
    if is_luxury:
        # Appartamenti di lusso: eleganti e spaziosi
        base_prompt = f"""Professional interior photography of a {style} {room_type} in a luxury apartment 
in {location}, Italy. High-end furnishings, natural lighting, wide angle shot, 
architectural digest style, ultra realistic, 8k, sharp focus, professional photography"""
    else:
        # Appartamenti normali: economici, piccoli, essenziali
        base_prompt = f"""Interior photo of a {style} {room_type} in a small budget apartment 
in {location}, Italy. Small compact space, simple basic furniture, IKEA-style cheap furnishings, 
no designer items, minimal decoration, compact room, basic essentials only, modest interior, 
affordable simple decor, practical basic setup, realistic budget rental"""
    
    negative_prompt = """blurry, low quality, distorted, ugly, bad anatomy, bad proportions, 
extra limbs, cloned face, disfigured, gross proportions, malformed limbs, 
missing arms, missing legs, extra arms, extra legs, mutated hands, 
fused fingers, too many fingers, long neck, text, watermark, signature, luxury items, 
expensive furniture, designer brands, high-end decor"""
    
    return base_prompt.strip(), negative_prompt.strip()

def generate_images(apartment_name, city, zone, style, output_dir, num_images=10, is_luxury=False):
    """Genera immagini con Stable Diffusion 3.5 Large - output diretto WebP"""
    api_token = os.environ.get('REPLICATE_API_TOKEN')
    if not api_token:
        print("❌ ERRORE: REPLICATE_API_TOKEN non trovata!")
        return []
    
    # Assicura percorso assoluto
    output_path = Path(output_dir).resolve()
    output_path.mkdir(parents=True, exist_ok=True)
    
    safe_name = sanitize_filename(apartment_name)
    rooms_to_generate = ROOM_TYPES[:num_images]
    image_files = []
    
    consecutive_errors = 0
    max_consecutive_errors = 3
    
    for idx, room_type in enumerate(rooms_to_generate, 1):
        print(f"   [{idx}/{num_images}] Generando: {room_type}...")
        
        prompt, negative_prompt = generate_prompt(city, zone, style, room_type, is_luxury)
        
        try:
            output = replicate.run(
                "stability-ai/stable-diffusion-3.5-large",
                input={
                    "prompt": prompt,
                    "negative_prompt": negative_prompt,
                    "aspect_ratio": "16:9",
                    "output_format": "webp",
                    "output_quality": 90,
                    "num_outputs": 1
                }
            )
            
            if output:
                # SD 3.5 Large restituisce direttamente un FileOutput, non una lista
                image_url = output if isinstance(output, str) else (output[0] if isinstance(output, list) else str(output))
                response = requests.get(image_url)
                
                if response.status_code == 200:
                    # Salva direttamente WebP (SD 3.5 Large genera già WebP)
                    webp_filename = f"{safe_name}-{idx}.webp"
                    webp_filepath = output_path / webp_filename
                    
                    with open(webp_filepath, 'wb') as f:
                        f.write(response.content)
                    
                    print(f"      ✅ WebP salvata: {webp_filename}")
                    consecutive_errors = 0  # Reset errori su successo
                    
                    image_files.append({
                        'webp': f"images/apartments/{webp_filename}"
                    })
                else:
                    print(f"      ❌ Errore download: {response.status_code}")
                    consecutive_errors += 1
            else:
                print(f"      ❌ Nessuna immagine generata")
                consecutive_errors += 1
            
            # Verifica errori consecutivi
            if consecutive_errors >= max_consecutive_errors:
                print(f"\n❌ ERRORE CRITICO: {consecutive_errors} errori consecutivi!")
                print(f"   Interrompo l'esecuzione per evitare sprechi.")
                print(f"   Verifica la connessione e il token API.")
                return image_files  # Ritorna quello che abbiamo fino ad ora
            
            if idx < num_images:
                time.sleep(2)
                
        except Exception as e:
            print(f"      ❌ Errore: {str(e)}")
            consecutive_errors += 1
            
            # Verifica errori consecutivi
            if consecutive_errors >= max_consecutive_errors:
                print(f"\n❌ ERRORE CRITICO: {consecutive_errors} errori consecutivi!")
                print(f"   Interrompo l'esecuzione per evitare sprechi.")
                print(f"   Verifica la connessione e il token API.")
                return image_files  # Ritorna quello che abbiamo fino ad ora
    
    return image_files

def create_markdown_file(apartment_data, image_files, project_root):
    """Crea file markdown nella cartella booking"""
    safe_name = sanitize_filename(apartment_data['name'])
    md_path = project_root / "site" / "content" / "italian" / "booking" / f"{safe_name}.md"
    
    # Prepara gallery (tutte le immagini sono già WebP)
    gallery_items = "\n".join([f'  - "{img["webp"]}"' for img in image_files])
    
    # Amenities random
    all_amenities = [
        ('WiFi Fibra', 'fas fa-wifi'),
        ('Aria condizionata', 'fas fa-snowflake'),
        ('Smart TV', 'fas fa-tv'),
        ('Cucina attrezzata', 'fas fa-utensils'),
        ('Lavatrice', 'fas fa-washer'),
        ('Lavastoviglie', 'fas fa-sink'),
        ('Macchina caffè', 'fas fa-mug-hot'),
        ('Riscaldamento', 'fas fa-temperature-high'),
        ('Asciugacapelli', 'fas fa-wind'),
        ('Ferro da stiro', 'fas fa-shirt'),
    ]
    
    selected_amenities = random.sample(all_amenities, random.randint(7, 10))
    amenities_md = "\n".join([f'  - name: "{name}"\n    icon: "{icon}"' for name, icon in selected_amenities])
    
    content = f"""---
title: "{apartment_data['name']}"
layout: "booking/single"
address: "{apartment_data['address']}"
price_per_night: {apartment_data['price']}
cleaning_fee: {apartment_data['cleaning_fee']}
max_guests: {apartment_data['guests']}
bedrooms: {apartment_data['bedrooms']}
bathrooms: {apartment_data['bathrooms']}
square_meters: {apartment_data['square_meters']}
latitude: {apartment_data['lat']}
longitude: {apartment_data['lon']}
main_image: "{image_files[0]['webp']}"
image_webp: "{image_files[0]['webp']}"
image: "{image_files[1]['webp'] if len(image_files) > 1 else image_files[0]['webp']}"
gallery: 
{gallery_items}
  
amenities:
{amenities_md}
draft: false
---
"""
    
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"   ✅ File markdown creato: {md_path.name}")

def generate_apartment_data(city_data, is_village=False, is_luxury=False):
    """Genera dati casuali per un appartamento"""
    if is_village:
        name = city_data['name']
        zone = None
        address = f"Via Centro {random.randint(1, 99)}, {city_data['name']}"
    else:
        zone = random.choice(city_data['zones'])
        name = f"{city_data['name']} {zone}"
        address = f"Via {zone} {random.randint(1, 150)}, {city_data['name']}"
    
    # Identifica città per prezzi di mercato (stima + 30%)
    city_name = city_data['name']
    
    if is_luxury:
        # Appartamenti di lusso: 2-3 camere, metrature più ampie
        bedrooms = random.choice([2, 3])
        bathrooms = 2 if bedrooms == 3 else random.choice([1, 2])
        # Metrature lusso: 90-130 mq (comunque stanze entro 40 mq)
        base_rooms = 4  # soggiorno, cucina, bagno, ingresso
        total_rooms = base_rooms + bedrooms + (bathrooms - 1)
        square_meters = min(130, total_rooms * random.randint(25, 38))
        
        # Prezzi lusso basati su mercato + 30%
        if city_name in ["Milano", "Firenze"]:
            price = random.randint(520, 750)
        elif city_name == "Roma":
            price = random.randint(490, 720)
        elif city_name in ["Bologna", "Verona"]:
            price = random.randint(390, 580)
        elif is_village and city_name in ["Positano", "Portofino", "Manarola"]:
            price = random.randint(450, 650)
        else:
            price = random.randint(325, 520)
        
        cleaning_fee = random.randint(150, 250)  # Pulizie più care per lusso
        style = random.choice(LUXURY_STYLES)
    else:
        # Appartamenti normali: 3 o 5 stanze (camere)
        bedrooms = random.choice([3, 5])
        bathrooms = 2 if bedrooms == 5 else random.choice([1, 2])
        # Calcola metratura: ogni stanza max 40 mq
        # Stanze totali = camere + bagni + soggiorno + cucina + ingresso
        base_rooms = 3  # soggiorno/cucina (open space), bagno, ingresso
        total_rooms = base_rooms + bedrooms + (bathrooms - 1)
        # Ogni stanza tra 20-40 mq
        square_meters = total_rooms * random.randint(20, 35)
        # Limita comunque a max ragionevole
        square_meters = min(square_meters, 200)
        
        # Prezzi normali basati su mercato + 30%
        if city_name == "Milano":
            price = random.randint(230, 320)
        elif city_name in ["Roma", "Firenze"]:
            price = random.randint(220, 310)
        elif city_name in ["Bologna", "Verona"]:
            price = random.randint(175, 260)
        elif city_name in ["Torino", "Padova"]:
            price = random.randint(155, 230)
        elif is_village and city_name in ["Positano", "Portofino", "Manarola", "Tropea"]:
            price = random.randint(190, 280)
        elif is_village:
            price = random.randint(135, 210)
        else:
            price = random.randint(155, 250)
        
        cleaning_fee = random.randint(50, 80)
        style = random.choice(NORMAL_STYLES)
    
    guests = bedrooms * 2
    
    # Variazione coordinate
    lat = city_data['lat'] + random.uniform(-0.01, 0.01)
    lon = city_data['lon'] + random.uniform(-0.01, 0.01)
    
    return {
        'name': name,
        'city': city_data['name'],
        'zone': zone,
        'address': address,
        'bedrooms': bedrooms,
        'bathrooms': bathrooms,
        'guests': guests,
        'square_meters': square_meters,
        'price': price,
        'cleaning_fee': cleaning_fee,
        'lat': lat,
        'lon': lon,
        'style': style,
        'is_luxury': is_luxury
    }

def main():
    # Trova la root del progetto (dove si trova site/)
    script_dir = Path(__file__).parent.resolve()
    project_root = script_dir.parent.parent  # Da scripts/ sali alla root
    
    # Verifica che siamo nella directory giusta
    site_dir = project_root / "site"
    if not site_dir.exists():
        print("❌ ERRORE: Impossibile trovare la directory 'site/'")
        print(f"   Directory corrente: {project_root}")
        sys.exit(1)
    
    print("\n🏠 GENERATORE APPARTAMENTI AUTOMATICO")
    print("=" * 50)
    print(f"📁 Directory progetto: {project_root}")
    
    # Chiedi numero appartamenti
    while True:
        try:
            num_apartments = int(input("\nQuanti appartamenti vuoi creare? "))
            if num_apartments > 0:
                break
            print("❌ Inserisci un numero maggiore di 0")
        except ValueError:
            print("❌ Inserisci un numero valido")
    
    # Chiedi numero appartamenti di lusso
    while True:
        try:
            num_luxury = int(input(f"\nQuanti appartamenti di lusso? (0-{num_apartments}): "))
            if 0 <= num_luxury <= num_apartments:
                break
            print(f"❌ Inserisci un numero tra 0 e {num_apartments}")
        except ValueError:
            print("❌ Inserisci un numero valido")
    
    # Calcola distribuzione
    num_cities = int(num_apartments * 0.7)
    num_villages = num_apartments - num_cities
    num_normal = num_apartments - num_luxury
    
    print(f"\n📊 Distribuzione:")
    print(f"   - Città principali: {num_cities} appartamenti (70%)")
    print(f"   - Borghi: {num_villages} appartamenti (30%)")
    if num_luxury > 0:
        print(f"   - Lusso: {num_luxury} appartamenti (325-750€/notte)")
    if num_normal > 0:
        print(f"   - Normali: {num_normal} appartamenti (135-320€/notte)")
    
    all_apartments = []
    luxury_count = 0
    
    # Genera appartamenti città
    for i in range(num_cities):
        city = random.choice(MAJOR_CITIES)
        is_luxury = luxury_count < num_luxury
        apt_data = generate_apartment_data(city, is_village=False, is_luxury=is_luxury)
        all_apartments.append(apt_data)
        if is_luxury:
            luxury_count += 1
    
    # Genera appartamenti borghi
    for i in range(num_villages):
        village = random.choice(BEAUTIFUL_VILLAGES)
        is_luxury = luxury_count < num_luxury
        apt_data = generate_apartment_data(village, is_village=True, is_luxury=is_luxury)
        all_apartments.append(apt_data)
        if is_luxury:
            luxury_count += 1
    
    print(f"\n🎨 Inizio generazione di {num_apartments} appartamenti...\n")
    
    successful_count = 0
    for idx, apt_data in enumerate(all_apartments, 1):
        apt_type = "🌟 LUSSO" if apt_data.get('is_luxury') else "🏠 NORMALE"
        print(f"\n{'='*60}")
        print(f"📍 [{idx}/{num_apartments}] {apt_type} | {apt_data['name']}")
        print(f"   {apt_data['bedrooms']} camere | {apt_data['square_meters']}mq | €{apt_data['price']}/notte")
        print(f"{'='*60}")
        
        # Genera immagini
        print(f"🖼️  Generazione immagini ({apt_data['style']})...")
        images_dir = project_root / "site" / "static" / "images" / "apartments"
        image_files = generate_images(
            apt_data['name'],
            apt_data['city'],
            apt_data['zone'],
            apt_data['style'],
            str(images_dir),
            num_images=10,
            is_luxury=apt_data.get('is_luxury', False)
        )
        
        if image_files and len(image_files) >= 2:  # Almeno 2 immagini per creare markdown
            # Crea file markdown
            print(f"📝 Creazione file markdown...")
            create_markdown_file(apt_data, image_files, project_root)
            print(f"✅ Appartamento '{apt_data['name']}' completato!")
            successful_count += 1
        else:
            print(f"❌ Errore nella generazione dell'appartamento (immagini insufficienti)")
            # Se ci sono stati troppi errori, generate_images ha già interrotto
            if len(image_files) == 0:
                print(f"\n⚠️  Interrompo la generazione di nuovi appartamenti")
                break
    
    print(f"\n{'='*60}")
    print(f"✨ COMPLETATO!")
    print(f"📊 Appartamenti creati con successo: {successful_count}/{num_apartments}")
    if successful_count > 0:
        print(f"📁 File markdown: {project_root}/site/content/italian/booking/")
        print(f"🖼️  Immagini: {project_root}/site/static/images/apartments/")
    print(f"{'='*60}\n")

if __name__ == '__main__':
    main()
