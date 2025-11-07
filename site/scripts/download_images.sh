#!/bin/bash

# Script per scaricare immagini placeholder da Unsplash per gli appartamenti
# Le immagini sono gratuite e possono essere utilizzate per scopi di test

# Directory di destinazione
DEST_DIR="/Users/work/Progetti/greenproperty/website/gp-site/site/static/images/apartments"

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

# Query di ricerca per tipo di immagini
queries=(
    "modern+apartment+interior"
    "luxury+apartment"
    "apartment+living+room"
    "apartment+bedroom"
    "apartment+kitchen"
)

echo "📥 Inizio download immagini per gli appartamenti..."
echo "Destinazione: $DEST_DIR"
echo ""

# Per ogni appartamento
for apt in "${apartments[@]}"; do
    echo "🏠 Scaricando immagini per: $apt"
    
    # Scarica 5 immagini per appartamento
    for i in {1..5}; do
        # Seleziona una query diversa per varietà
        query_index=$((i % ${#queries[@]}))
        query="${queries[$query_index]}"
        
        # URL Unsplash Source (immagini random 1920x1080)
        url="https://source.unsplash.com/1920x1080/?${query}"
        
        # Nome file
        filename="${apt}-${i}.jpg"
        filepath="${DEST_DIR}/${filename}"
        
        echo "  📷 Scaricando ${filename}..."
        
        # Scarica l'immagine con curl
        curl -L -o "$filepath" "$url" --silent --show-error
        
        if [ $? -eq 0 ]; then
            echo "  ✅ ${filename} scaricata con successo"
        else
            echo "  ❌ Errore nel download di ${filename}"
        fi
        
        # Piccola pausa per evitare rate limiting
        sleep 1
    done
    
    echo ""
done

echo "✨ Download completato!"
echo ""
echo "📝 NOTA: Le immagini scaricate sono in formato JPG."
echo "Se vuoi convertirle in WebP, esegui lo script convert_to_webp.fish"
echo ""
echo "🔄 Per convertire in WebP esegui:"
echo "   cd $DEST_DIR"
echo "   ./convert_to_webp.fish"
