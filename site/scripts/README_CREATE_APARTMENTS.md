# Generatore Automatico Appartamenti Completi

Script Python all-in-one per creare appartamenti completi e pronti all'uso con un solo comando.

## 🎯 Cosa fa questo script

1. **Chiede** quanti appartamenti creare
2. **Distribuisce** geograficamente secondo la regola 70/30:
   - 70% nelle città principali (Milano, Roma, Firenze, Bologna, Torino, Venezia, Verona, Padova)
   - 30% nei borghi più belli d'Italia
3. **Genera** 10 immagini AI per ogni appartamento con Stable Diffusion
4. **Converte** automaticamente ogni immagine in formato WebP
5. **Crea** file markdown completo nella cartella `booking/`

## 🚀 Setup Veloce

```fish
# 1. Installa dipendenze
pip install replicate requests pillow

# 2. Configura API token (se non l'hai già fatto)
set -x REPLICATE_API_TOKEN your_token_here

# 3. Esegui lo script
cd site/scripts
python create_apartments.py
```

## 📖 Esempio d'uso

```fish
$ python create_apartments.py

🏠 GENERATORE APPARTAMENTI AUTOMATICO
==================================================

Quanti appartamenti vuoi creare? 10

📊 Distribuzione:
   - Città principali: 7 appartamenti (70%)
   - Borghi: 3 appartamenti (30%)

🎨 Inizio generazione di 10 appartamenti...

============================================================
📍 [1/10] Milano Navigli
============================================================
🖼️  Generazione immagini (modern minimalist)...
   [1/10] Generando: living room...
      ✅ JPG salvata: milano-navigli-1.jpg
      ✅ Convertita in WebP: milano-navigli-1.webp
   [2/10] Generando: kitchen...
      ✅ JPG salvata: milano-navigli-2.jpg
      ✅ Convertita in WebP: milano-navigli-2.webp
   ...
📝 Creazione file markdown...
   ✅ File markdown creato: milano-navigli.md
✅ Appartamento 'Milano Navigli' completato!

[continua per tutti gli appartamenti...]

============================================================
✨ COMPLETATO!
📊 Appartamenti creati: 10
📁 File markdown: site/content/italian/booking/
🖼️  Immagini: site/static/images/apartments/
============================================================
```

## 🏙️ Città Principali (70%)

Lo script sceglie casualmente tra queste città:
- **Milano** (Duomo, Navigli, Brera, Centrale, Porta Romana, Isola, Porta Venezia)
- **Roma** (Colosseo, Trastevere, Prati, Monti, Testaccio, San Lorenzo)
- **Firenze** (Duomo, Ponte Vecchio, Santa Croce, Santo Spirito, San Frediano)
- **Bologna** (Centro, Santo Stefano, Saragozza, Irnerio)
- **Torino** (Centro, Quadrilatero, San Salvario, Crocetta)
- **Venezia** (San Marco, Cannaregio, Dorsoduro, Castello)
- **Verona** (Arena, Centro Storico, Veronetta)
- **Padova** (Centro, Prato della Valle, Santo)

## 🏘️ Borghi d'Italia (30%)

Lo script sceglie casualmente tra questi borghi storici:
- Civita di Bagnoregio (Lazio)
- Alberobello (Puglia)
- Manarola (Liguria - Cinque Terre)
- San Gimignano (Toscana)
- Orta San Giulio (Piemonte)
- Spello (Umbria)
- Castelmezzano (Basilicata)
- Portofino (Liguria)
- Tropea (Calabria)
- Positano (Campania)

## 🎨 Stili Arredamento

Lo script assegna casualmente uno di questi stili:
- Modern minimalist
- Luxury contemporary
- Classic elegant
- Industrial chic
- Scandinavian cozy
- Italian traditional

## 📁 Output Generato

Per ogni appartamento viene creato:

### 1. File Markdown
```
site/content/italian/booking/nome-appartamento.md
```

Contiene:
- Titolo e indirizzo
- Prezzo per notte e pulizie
- Numero ospiti, camere, bagni
- Coordinate GPS
- Gallery di 10 immagini
- 7-10 amenities casuali

### 2. Immagini (JPG + WebP)
```
site/static/images/apartments/nome-appartamento-1.jpg
site/static/images/apartments/nome-appartamento-1.webp
site/static/images/apartments/nome-appartamento-2.jpg
site/static/images/apartments/nome-appartamento-2.webp
...fino a 10...
```

## 📊 Caratteristiche Generate

Per ogni appartamento vengono generate casualmente:
- **Camere:** 1-3
- **Bagni:** 1-2
- **Ospiti:** 2-6 (doppio delle camere)
- **Metratura:** 55-130 mq
- **Prezzo:** €150-350 /notte
- **Pulizie:** €60-100
- **Amenities:** 7-10 servizi tra WiFi, TV, cucina, lavatrice, etc.

## 💰 Costi Stimati

Con Replicate API:
- **1 appartamento** = 10 immagini = ~€0.023
- **10 appartamenti** = 100 immagini = ~€0.23
- **50 appartamenti** = 500 immagini = ~€1.15
- **100 appartamenti** = 1000 immagini = ~€2.30

> I costi sono basati su SDXL (~$0.0023 per immagine)

## ⏱️ Tempi di Generazione

Tempo approssimativo per appartamento:
- Generazione 10 immagini: ~3-4 minuti
- Conversione WebP: ~10 secondi
- Creazione markdown: istantaneo

**Totale per appartamento:** ~4 minuti

Esempi:
- 10 appartamenti: ~40 minuti
- 25 appartamenti: ~100 minuti (~1h 40min)
- 50 appartamenti: ~200 minuti (~3h 20min)

## 🐛 Troubleshooting

### Lo script si interrompe durante la generazione
- Controlla la connessione internet
- Verifica i crediti Replicate rimanenti
- Riavvia lo script: continuerà dagli appartamenti mancanti

### Errore: "REPLICATE_API_TOKEN non trovata"
```fish
set -x REPLICATE_API_TOKEN your_token_here
```

### Errore: "No module named 'PIL'"
```fish
pip install pillow
```

### Le immagini non vengono convertite in WebP
- Verifica che Pillow sia installato correttamente
- Le immagini JPG vengono comunque salvate e sono utilizzabili

## 💡 Consigli

1. **Inizia con pochi appartamenti** (5-10) per testare
2. **Monitora i crediti** Replicate
3. **Backup delle immagini** prima di rigenerare
4. **Personalizza gli amenities** nel codice se necessario

## 🔄 Workflow Consigliato

```fish
# 1. Test con 3 appartamenti
python create_apartments.py
# Inserisci: 3

# 2. Verifica risultati
ls ../content/italian/booking/
ls ../static/images/apartments/

# 3. Se tutto ok, genera il batch completo
python create_apartments.py
# Inserisci: 50
```

## 🎯 Pro Tips

- **Batch piccoli:** Meglio 50 appartamenti in 2 sessioni da 25 che 50 in una volta
- **Backup continuo:** Fai backup delle immagini periodicamente
- **Varietà:** Lo script crea automaticamente varietà di stili e location
- **Coordinate GPS:** Le coordinate sono reali con piccole variazioni per simulare indirizzi diversi

## 📞 Supporto

Per problemi:
- Documentazione Replicate: https://replicate.com/docs
- Issues API: https://replicate.com/contact

---

**Script creato per Green Property - Gestione appartamenti automatizzata** 🏠✨
