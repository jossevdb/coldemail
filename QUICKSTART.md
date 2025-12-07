# Quick Start Guide

Kom snel aan de slag met de Vlaamse Gemeente Contact Scraper!

## Stap 1: Installatie

```bash
# Installeer dependencies
pip install -r requirements.txt
```

## Stap 2: Test run

Test eerst met 5 gemeentes om te verifiëren dat alles werkt:

```bash
python main.py --test
```

Dit zal:
- ✅ De eerste 5 gemeentes scrapen
- ✅ Een test Excel bestand maken in `output/`
- ✅ Logs genereren in `logs/`

**Verwachte output:**
```
VLAAMSE GEMEENTE CONTACT SCRAPER
============================================================
Totaal aantal Vlaamse gemeentes: 300+
Limiet ingesteld: 5 gemeentes
============================================================

Scraping gemeentes: 100%|████████████| 5/5 [00:30<00:00]
```

## Stap 3: Controleer de resultaten

1. **Open Excel bestand:**
   - Ga naar `output/`
   - Open het nieuwste `.xlsx` bestand
   - Controleer de gevonden contacten

2. **Bekijk de logs:**
   - Ga naar `logs/`
   - Open het nieuwste `.log` bestand
   - Controleer op errors of waarschuwingen

## Stap 4: Volledige run

Als de test succesvol was, start de volledige scraping:

```bash
# Scrape alle 300+ gemeentes
python main.py
```

⏱️ **Geschatte tijd:** 2-4 uur (afhankelijk van internet snelheid)

## Stap 5: Monitor de voortgang

Tijdens het scrapen zie je:

```
Scraping gemeentes:  34%|███████▋              | 102/300
[Contacts: 247, Mislukt: 12]

============================================================
Scraping: Antwerpen (Antwerpen)
============================================================
Website gevonden voor Antwerpen: https://www.antwerpen.be
Gescraped 15 pagina's van https://www.antwerpen.be
✓ 8 contacts gevonden voor Antwerpen
```

## Automatische checkpoints

Elke 10 gemeentes wordt automatisch een checkpoint opgeslagen:

```
📝 Checkpoint opslaan (na 10 gemeentes)...
Checkpoint opgeslagen: output/checkpoint_10_20241207_143022.xlsx
```

## Bij onderbreking

Als het script onderbroken wordt (Ctrl+C of crash):

1. **Zoek laatste checkpoint:**
   ```bash
   ls -lht output/checkpoint_*.xlsx | head -1
   ```

2. **Resume vanaf checkpoint:**
   ```bash
   # Als checkpoint was bij gemeente 50:
   python main.py --start-from 50
   ```

## Tips voor optimale resultaten

### 🚀 Sneller scrapen

```bash
# Verhoog checkpoint interval (minder I/O)
python main.py --checkpoint-interval 25
```

### 🐌 Langzamer scrapen (voor langzame sites)

Pas aan in `src/config.py`:
```python
SCRAPER_CONFIG = {
    'rate_limit_seconds': 5,  # Verhoog van 3 naar 5
}
```

### 🔍 Debug problemen

```bash
# Meer details in logs
python main.py --log-level DEBUG --limit 10
```

### 📊 Specifieke provincies

Pas aan in `src/config.py`, comment provincies uit die je niet wilt:

```python
MUNICIPALITIES = {
    'Antwerpen': [...],  # Scrape deze
    # 'Limburg': [...],  # Skip deze
    'Oost-Vlaanderen': [...],
    # 'Vlaams-Brabant': [...],
    # 'West-Vlaanderen': [...]
}
```

## Verwachte resultaten

Per gemeente verwacht je:

- ✅ **Goede gemeente websites:** 3-15 contacten
- ⚠️ **Kleine gemeentes:** 0-5 contacten
- ❌ **Geen website/moderne site:** 0 contacten

Typische success rate: **60-80%** van gemeentes leveren data op.

## Meest voorkomende issues

### Issue: "Geen website gevonden"

**Oplossing:** Normaal! ~20% van gemeentes hebben geen standaard URL patroon.
Check `logs/failed_municipalities_*.txt` voor lijst.

### Issue: "robots.txt blokkeert toegang"

**Oplossing:** Respecteer de blokkade. Sommige sites willen niet gescraped worden.
Deze gemeentes worden automatisch overgeslagen.

### Issue: Script lijkt vast te zitten

**Oorzaak:** Rate limiting in actie (wacht 3 sec tussen requests).
**Oplossing:** Gewoon wachten, dit is normaal en gewenst gedrag.

## Resultaat analyse

Na afloop, bekijk de statistieken in het log:

```
=== STATISTIEKEN ===
Unieke gemeentes: 285

Contacten per afdeling:
  Cultuur: 145
  Jeugd: 128
  Sport: 112
  Toerisme: 98
  Evenementen: 87
  Vrije Tijd: 76

Contacten per provincie:
  Antwerpen: 178
  Oost-Vlaanderen: 165
  West-Vlaanderen: 142
  Vlaams-Brabant: 121
  Limburg: 98
```

## Next steps

1. **Open het Excel bestand** in `output/`
2. **Filter op afdeling** die je nodig hebt
3. **Verifieer e-mailadressen** (dubbelcheck een paar manueel)
4. **Gebruik verantwoordelijk** volgens GDPR

## Hulp nodig?

- 📖 Lees de volledige [README.md](README.md)
- 📝 Check de logs in `logs/`
- 🐛 Open een GitHub issue

---

**Veel succes met het scrapen! 🚀**
