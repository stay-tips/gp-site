# Generatore Immagini Appartamenti con Stable Diffusion

Script Python per generare immagini fotorealistiche di appartamenti usando Stable Diffusion via Replicate API.

## 🚀 Setup Iniziale

### 1. Installa Python e dipendenze

```bash
# Assicurati di avere Python 3.7+
python3 --version

# Installa le dipendenze necessarie
pip install replicate requests
```

### 2. Ottieni API Key gratuita da Replicate

1. Vai su [https://replicate.com/](https://replicate.com/)
2. Registrati gratuitamente (include crediti gratuiti)
3. Vai su **Account Settings > API Tokens**
4. Copia il tuo token

r8_K2ckKHy8IQWYggDb3qWdDldUtAs01Kd06V3Zt


### 3. Configura l'API Token

```bash
# Su macOS/Linux (Bash/Zsh)
export REPLICATE_API_TOKEN=r8_K2ckKHy8IQWYggDb3qWdDldUtAs01Kd06V3Zt


# Su macOS/Linux (Fish shell)
set -x REPLICATE_API_TOKEN r8_K2ckKHy8IQWYggDb3qWdDldUtAs01Kd06V3Zt


# Su Windows (PowerShell)
$env:REPLICATE_API_TOKEN="r8_K2ckKHy8IQWYggDb3qWdDldUtAs01Kd06V3Zt"

# Per renderlo permanente:

# Bash: aggiungi al ~/.bashrc
echo 'export REPLICATE_API_TOKEN=r8_K2ckKHy8IQWYggDb3qWdDldUtAs01Kd06V3Zt' >> ~/.bashrc

# Zsh: aggiungi al ~/.zshrc
echo 'export REPLICATE_API_TOKEN=r8_K2ckKHy8IQWYggDb3qWdDldUtAs01Kd06V3Zt' >> ~/.zshrc

# Fish: aggiungi al ~/.config/fish/config.fish
echo 'set -x REPLICATE_API_TOKEN r8_K2ckKHy8IQWYggDb3qWdDldUtAs01Kd06V3Zt' >> ~/.config/fish/config.fish
```

## 📖 Uso dello Script

### Sintassi Base (Fish Shell)

```fish
python generate_apartment_images.py \
    --name "Nome Appartamento" \
    --bedrooms NUMERO \
    --bathrooms NUMERO \
    --guests NUMERO \
    --city "Città" \
    --style "stile arredamento" \
    --num-images 10
```

> **Nota:** Le immagini vengono salvate automaticamente in `site/static/images/apartments/` a meno che non specifichi un percorso diverso con `--output`

### Esempi Pratici (Fish Shell)

#### Esempio 1: Milano Duomo (percorso default)
```fish
python generate_apartment_images.py \
    --name "Milano Duomo" \
    --bedrooms 2 \
    --bathrooms 1 \
    --guests 4 \
    --city "Milano" \
    --style "modern minimalist"
```

#### Esempio 2: Roma Colosseo (percorso default)
```fish
python generate_apartment_images.py \
    --name "Roma Colosseo" \
    --bedrooms 2 \
    --bathrooms 1 \
    --guests 4 \
    --city "Roma" \
    --style "luxury contemporary"
```

#### Esempio 3: Firenze - solo 5 immagini
```fish
python generate_apartment_images.py \
    --name "Firenze Ponte Vecchio" \
    --bedrooms 2 \
    --bathrooms 2 \
    --guests 5 \
    --city "Firenze" \
    --style "classic elegant" \
    --num-images 5
```

#### Esempio 4: Percorso personalizzato
```fish
python generate_apartment_images.py \
    --name "Milano Navigli" \
    --bedrooms 1 \
    --bathrooms 1 \
    --guests 3 \
    --city "Milano" \
    --style "industrial chic" \
    --output /percorso/personalizzato
```

## 🎨 Stili Arredamento Disponibili

- `modern minimalist` - Moderno e minimalista
- `luxury contemporary` - Lusso contemporaneo
- `classic elegant` - Classico elegante
- `industrial chic` - Industrial chic
- `scandinavian cozy` - Scandinavo accogliente
- `italian traditional` - Tradizionale italiano
- `bohemian eclectic` - Bohémien eclèttico
- `mid-century modern` - Modernariato anni '50-'60

## 📁 Tipi di Stanze Generate

Per ogni appartamento, lo script genera immagini di:

1. Living room (soggiorno)
2. Kitchen (cucina)
3. Bedroom (camera da letto)
4. Bathroom (bagno)
5. Dining area (zona pranzo)
6. Entrance hallway (ingresso)
7. Balcony view (vista balcone)
8. Bedroom detail (dettaglio camera)
9. Kitchen detail (dettaglio cucina)
10. Living room from different angle (soggiorno angolo diverso)

## 💰 Costi

Replicate offre:
- **Crediti gratuiti** alla registrazione
- Circa **$0.0023** per immagine (SDXL)
- 10 immagini = circa **$0.023**

Per 9 appartamenti × 10 immagini = **~$2** totale

## ⚙️ Parametri Avanzati

Lo script genera immagini con queste specifiche:
- **Risoluzione**: 1920×1080 (Full HD)
- **Formato**: JPG
- **Qualità**: Alta (50 inference steps)
- **Guidance Scale**: 7.5 (bilanciamento qualità/creatività)

## 🐛 Troubleshooting

### Errore: "REPLICATE_API_TOKEN non trovata"
```fish
# Verifica che il token sia impostato (Fish shell)
echo $REPLICATE_API_TOKEN

# Se vuoto, impostalo di nuovo
set -x REPLICATE_API_TOKEN your_token_here
```

### Errore: "No module named 'replicate'"
```fish
pip install replicate requests
```

### Immagini di bassa qualità
- Prova stili diversi
- Modifica i parametri nel codice (guidance_scale, num_inference_steps)
- Usa prompt più dettagliati

## 📞 Supporto

Per problemi con l'API:
- Documentazione Replicate: https://replicate.com/docs
- Support: https://replicate.com/contact

## 📄 License

Questo script è fornito "as is" per uso personale/commerciale.
Le immagini generate appartengono a chi le crea secondo i termini di Replicate.
