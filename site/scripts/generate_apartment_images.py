#!/usr/bin/env python3
"""
Script per generare immagini di appartamenti usando Stable Diffusion via Replicate API

Requisiti:
    pip install replicate pillow requests

Uso:
    python generate_apartment_images.py --name "Milano Duomo" --bedrooms 2 --bathrooms 1 \\
        --guests 4 --city "Milano" --style "modern minimalist" --output ./output

Per ottenere API key gratuita:
    1. Vai su https://replicate.com/
    2. Registrati gratuitamente
    3. Vai su Account Settings > API Tokens
    4. Copia il token e impostalo: export REPLICATE_API_TOKEN=your_token_here
"""

import os
import sys
import argparse
import replicate
from pathlib import Path
import time

# Lista dei locali da fotografare per un appartamento
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
    """Sanitizza il nome file rimuovendo caratteri non validi"""
    return "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in name).strip()

def generate_prompt(apartment_name, city, style, room_type, bedrooms, bathrooms):
    """Genera un prompt ottimizzato per Stable Diffusion"""
    
    base_prompt = f"""Professional interior photography of a {style} {room_type} in a luxury apartment 
in {city}, Italy. High-end furnishings, natural lighting, wide angle shot, 
architectural digest style, ultra realistic, 8k, sharp focus, professional photography"""
    
    # Prompt negativi per migliorare la qualità
    negative_prompt = """blurry, low quality, distorted, ugly, bad anatomy, bad proportions, 
extra limbs, cloned face, disfigured, gross proportions, malformed limbs, 
missing arms, missing legs, extra arms, extra legs, mutated hands, 
fused fingers, too many fingers, long neck, text, watermark, signature"""
    
    return base_prompt.strip(), negative_prompt.strip()

def generate_images(apartment_name, bedrooms, bathrooms, guests, city, style, output_dir, num_images=10):
    """
    Genera immagini per l'appartamento usando Stable Diffusion
    
    Args:
        apartment_name: Nome dell'appartamento
        bedrooms: Numero di camere da letto
        bathrooms: Numero di bagni
        guests: Numero di posti letto
        city: Città dell'appartamento
        style: Stile dell'arredamento
        output_dir: Directory di output
        num_images: Numero di immagini da generare (default 10)
    """
    
    # Verifica API token
    api_token = os.environ.get('REPLICATE_API_TOKEN')
    if not api_token:
        print("❌ ERRORE: Variabile d'ambiente REPLICATE_API_TOKEN non trovata!")
        print("\nPer ottenere un token gratuito:")
        print("1. Vai su https://replicate.com/")
        print("2. Registrati gratuitamente")
        print("3. Vai su Account Settings > API Tokens")
        print("4. Esegui: export REPLICATE_API_TOKEN=your_token_here")
        sys.exit(1)
    
    # Crea directory di output
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Sanitizza nome appartamento per nome file
    safe_name = sanitize_filename(apartment_name.lower().replace(' ', '-'))
    
    print(f"\n🏠 Generazione immagini per: {apartment_name}")
    print(f"📍 Città: {city}")
    print(f"🎨 Stile: {style}")
    print(f"🛏️  Camere: {bedrooms} | 🚿 Bagni: {bathrooms} | 👥 Posti letto: {guests}")
    print(f"📁 Output: {output_path}")
    print(f"🖼️  Immagini da generare: {num_images}\n")
    
    # Seleziona i locali da fotografare basandosi sul numero di immagini richieste
    rooms_to_generate = ROOM_TYPES[:num_images]
    
    consecutive_errors = 0
    max_consecutive_errors = 3
    
    for idx, room_type in enumerate(rooms_to_generate, 1):
        print(f"[{idx}/{num_images}] Generando immagine di: {room_type}...")
        
        # Genera prompt
        prompt, negative_prompt = generate_prompt(
            apartment_name, city, style, room_type, bedrooms, bathrooms
        )
        
        try:
            # Chiama API Stable Diffusion via Replicate
            # Usando il modello Stable Diffusion 3.5 Large di Stability AI
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
            
            # Salva l'immagine
            if output:
                # SD 3.5 Large restituisce direttamente un FileOutput, non una lista
                image_url = output if isinstance(output, str) else (output[0] if isinstance(output, list) else str(output))
                
                # Download immagine
                import requests
                response = requests.get(image_url)
                
                if response.status_code == 200:
                    # Nome file: appartamento-1.webp, appartamento-2.webp, etc.
                    filename = f"{safe_name}-{idx}.webp"
                    filepath = output_path / filename
                    
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    
                    print(f"   ✅ Salvata: {filename}")
                    consecutive_errors = 0  # Reset errori consecutivi su successo
                else:
                    print(f"   ❌ Errore download: {response.status_code}")
                    consecutive_errors += 1
            else:
                print(f"   ❌ Nessuna immagine generata")
                consecutive_errors += 1
            
            # Verifica errori consecutivi
            if consecutive_errors >= max_consecutive_errors:
                print(f"\n❌ ERRORE CRITICO: {consecutive_errors} errori consecutivi!")
                print(f"   Interrompo l'esecuzione per evitare sprechi.")
                print(f"   Verifica la connessione e il token API.")
                sys.exit(1)
            
            # Pausa per evitare rate limiting
            if idx < num_images:
                time.sleep(2)
                
        except Exception as e:
            print(f"   ❌ Errore: {str(e)}")
            consecutive_errors += 1
            
            # Verifica errori consecutivi
            if consecutive_errors >= max_consecutive_errors:
                print(f"\n❌ ERRORE CRITICO: {consecutive_errors} errori consecutivi!")
                print(f"   Interrompo l'esecuzione per evitare sprechi.")
                print(f"   Verifica la connessione e il token API.")
                sys.exit(1)
            
            continue
    
    print(f"\n✨ Completato! Immagini salvate in: {output_path}")
    print(f"📊 Immagini generate: {idx}/{num_images}")

def main():
    parser = argparse.ArgumentParser(
        description='Genera immagini di appartamenti usando Stable Diffusion',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi d'uso:

  # Esempio base
  python generate_apartment_images.py --name "Milano Duomo" --bedrooms 2 --bathrooms 1 \\
      --guests 4 --city "Milano" --style "modern minimalist"

  # Con directory output personalizzata
  python generate_apartment_images.py --name "Roma Colosseo" --bedrooms 2 --bathrooms 1 \\
      --guests 4 --city "Roma" --style "luxury contemporary" --output /path/to/images

  # Generare 5 immagini invece di 10
  python generate_apartment_images.py --name "Firenze Duomo" --bedrooms 1 --bathrooms 1 \\
      --guests 2 --city "Firenze" --style "classic elegant" --num-images 5

Stili arredamento suggeriti:
  - modern minimalist
  - luxury contemporary
  - classic elegant
  - industrial chic
  - scandinavian cozy
  - italian traditional
        """
    )
    
    parser.add_argument('--name', required=True, help='Nome dell\'appartamento')
    parser.add_argument('--bedrooms', type=int, required=True, help='Numero di camere da letto')
    parser.add_argument('--bathrooms', type=int, required=True, help='Numero di bagni')
    parser.add_argument('--guests', type=int, required=True, help='Numero di posti letto')
    parser.add_argument('--city', required=True, help='Città dell\'appartamento')
    parser.add_argument('--style', required=True, help='Stile dell\'arredamento')
    parser.add_argument('--output', default='../static/images/apartments', help='Directory di output (default: site/static/images/apartments)')
    parser.add_argument('--num-images', type=int, default=10, help='Numero di immagini da generare (default: 10)')
    
    args = parser.parse_args()
    
    # Genera le immagini
    generate_images(
        apartment_name=args.name,
        bedrooms=args.bedrooms,
        bathrooms=args.bathrooms,
        guests=args.guests,
        city=args.city,
        style=args.style,
        output_dir=args.output,
        num_images=args.num_images
    )

if __name__ == '__main__':
    main()
