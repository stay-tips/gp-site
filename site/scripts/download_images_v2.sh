#!/bin/bash

# Script aggiornato per scaricare immagini placeholder da Lorem Picsum
# Lorem Picsum è più affidabile e stabile per immagini placeholder

# Directory di destinazione
DEST_DIR="/Users/work/Progetti/greenproperty/website/gp-site/site/static/images/apartments"

# Rimuovi i vecchi file HTML scaricati
echo "🗑️  Rimuovendo i file HTML errati..."
rm -f "$DEST_DIR"/milano-duomo-*.jpg
rm -f "$DEST_DIR"/milano-navigli-*.jpg
rm -f "$DEST_DIR"/milano-brera-*.jpg
rm -f "$DEST_DIR"/milano-centrale-*.jpg
rm -f "$DEST_DIR"/milano-porta-romana-*.jpg
rm -f "$DEST_DIR"/roma-colosseo-*.jpg
rm -f "$DEST_DIR"/roma-trastevere-*.jpg
rm -f "$DEST_DIR"/firenze-duomo-*.jpg
rm -f "$DEST_DIR"/firenze-ponte-vecchio-*.jpg

# Array degli appartamenti
apartments=(
    "milano-duomo"
    "milano-navigli"
    "milano-brera"
    "milano-centrale"
    "milano-porta-romana"
    "roma-colosseo"
    "roma-trastevere"
    "firenze-duomo"
    "firenze-ponte-vecchio"
)

echo ""
echo "📥 Inizio download immagini da Lorem Picsum..."
echo "Destinazione: $DEST_DIR"
echo ""

# ID seed per garantire immagini diverse ma consistenti
base_seed=1000

# Per ogni appartamento
for apt in "${apartments[@]}"; do
    echo "🏠 Scaricando immagini per: $apt"
    
    # Scarica 5 immagini per appartamento
    for i in {1..5}; do
        # Calcola un seed unico per ogni immagine
        seed=$((base_seed + i))
        
        # URL Lorem Picsum con seed per immagini consistenti (1920x1080)
        url="https://picsum.photos/seed/${apt}-${seed}/1920/1080.jpg"
        
        # Nome file
        filename="${apt}-${i}.jpg"
        filepath="${DEST_DIR}/${filename}"
        
        echo "  📷 Scaricando ${filename}..."
        
        # Scarica l'immagine con curl, seguendo i redirect
        curl -L -o "$filepath" "$url" --silent --show-error
        
        if [ $? -eq 0 ] && [ -s "$filepath" ]; then
            # Verifica che sia un'immagine JPEG valida
            file_type=$(file -b --mime-type "$filepath")
            if [[ $file_type == image/* ]]; then
                echo "  ✅ ${filename} scaricata con successo"
            else
                echo "  ⚠️  ${filename} non è un'immagine valida (${file_type})"
                rm -f "$filepath"
            fi
        else
            echo "  ❌ Errore nel download di ${filename}"
        fi
        
        # Piccola pausa per evitare rate limiting
        sleep 0.5
    done
    
    base_seed=$((base_seed + 100))
    echo ""
done

echo "✨ Download completato!"
echo ""
echo "📝 Verifico i file scaricati..."
image_count=$(find "$DEST_DIR" -name "*.jpg" -type f | wc -l)
echo "✅ Totale immagini scaricate: $image_count"
echo ""
echo "Se vuoi convertirle in WebP, esegui:"
echo "   cd $DEST_DIR"
echo "   ./convert_to_webp.fish"
