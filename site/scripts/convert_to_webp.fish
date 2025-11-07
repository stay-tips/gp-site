#!/usr/bin/env fish

# Script per convertire immagini JPG e PNG in WebP
# Autore: Creato per Green Property

# Ottieni la directory dove si trova lo script
set SCRIPT_DIR (dirname (status --current-filename))

# Chiedi all'utente la cartella di origine/destinazione
echo "==================================="
echo "Convertitore Immagini JPG/PNG → WebP"
echo "==================================="
echo ""
echo "Inserisci il percorso della cartella da processare"
echo "(premi INVIO per usare la cartella corrente: $SCRIPT_DIR)"
read -P "Cartella: " target_dir

# Se l'utente preme solo INVIO, usa la directory dello script
if test -z "$target_dir"
    set target_dir $SCRIPT_DIR
    echo "→ Usando la cartella corrente: $target_dir"
else
    # Espandi il percorso se contiene ~
    set target_dir (eval echo $target_dir)
    echo "→ Usando la cartella: $target_dir"
end

# Verifica che la directory esista
if not test -d "$target_dir"
    echo "❌ ERRORE: La cartella '$target_dir' non esiste!"
    exit 1
end

# Verifica che cwebp sia installato
if not command -v cwebp >/dev/null 2>&1
    echo ""
    echo "❌ ERRORE: cwebp non è installato!"
    echo ""
    echo "Per installare su macOS:"
    echo "  brew install webp"
    echo ""
    echo "Per installare su Linux (Ubuntu/Debian):"
    echo "  sudo apt-get install webp"
    echo ""
    exit 1
end

# Conta i file da convertire
set jpg_count (find "$target_dir" -maxdepth 1 -type f \( -iname "*.jpg" -o -iname "*.jpeg" \) | wc -l | string trim)
set png_count (find "$target_dir" -maxdepth 1 -type f -iname "*.png" | wc -l | string trim)
set total_count (math $jpg_count + $png_count)

echo ""
echo "📊 File trovati:"
echo "   JPG/JPEG: $jpg_count"
echo "   PNG: $png_count"
echo "   TOTALE: $total_count"
echo ""

if test $total_count -eq 0
    echo "⚠️  Nessun file JPG o PNG trovato nella cartella!"
    exit 0
end

# Chiedi conferma
echo "La conversione mantiene i file originali e crea nuovi file .webp"
read -P "Vuoi procedere? (s/N): " confirm

if test "$confirm" != "s" -a "$confirm" != "S"
    echo "❌ Operazione annullata."
    exit 0
end

echo ""
echo "🔄 Inizio conversione..."
echo ""

set converted 0
set errors 0

# Converti file JPG e JPEG
for img in (find "$target_dir" -maxdepth 1 -type f \( -iname "*.jpg" -o -iname "*.jpeg" \))
    set basename (basename "$img")
    set filename (string replace -r '\.(jpg|jpeg)$' '' "$basename")
    set output "$target_dir/$filename.webp"
    
    echo "  → Convertendo: $basename"
    
    if cwebp -q 85 "$img" -o "$output" >/dev/null 2>&1
        set converted (math $converted + 1)
        echo "    ✓ Creato: $filename.webp"
    else
        set errors (math $errors + 1)
        echo "    ✗ Errore nella conversione di $basename"
    end
end

# Converti file PNG
for img in (find "$target_dir" -maxdepth 1 -type f -iname "*.png")
    set basename (basename "$img")
    set filename (string replace -r '\.png$' '' "$basename")
    set output "$target_dir/$filename.webp"
    
    echo "  → Convertendo: $basename"
    
    if cwebp -q 85 "$img" -o "$output" >/dev/null 2>&1
        set converted (math $converted + 1)
        echo "    ✓ Creato: $filename.webp"
    else
        set errors (math $errors + 1)
        echo "    ✗ Errore nella conversione di $basename"
    end
end

echo ""
echo "==================================="
echo "✅ Conversione completata!"
echo "   Convertiti: $converted file"
if test $errors -gt 0
    echo "   Errori: $errors file"
end
echo "==================================="
