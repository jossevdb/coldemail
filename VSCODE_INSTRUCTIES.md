# Vlaamse Gemeente Scraper - VS Code Instructies

## Stap 1: Clone de repository

Open Terminal (of Command Prompt op Windows) en run:

```bash
git clone https://github.com/jossevdb/coldemail.git
cd coldemail
```

## Stap 2: Open in VS Code

```bash
code .
```

Of open VS Code en ga naar: **File → Open Folder** → Selecteer de `coldemail` folder

## Stap 3: Python Setup

### 3.1 - Check of Python geïnstalleerd is

Open Terminal in VS Code (**Terminal → New Terminal** of `Ctrl+Shift+ù`)

```bash
python --version
# OF
python3 --version
```

Als je Python niet hebt: download van https://www.python.org/downloads/

### 3.2 - Maak virtual environment

In VS Code Terminal:

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

Je ziet nu `(venv)` voor je terminal prompt! ✅

### 3.3 - Installeer dependencies

```bash
pip install -r requirements.txt
```

Wacht tot alles geïnstalleerd is (~1 minuut).

## Stap 4: Run de Scraper! 🎯

### Optie A: Test run (5 gemeentes, ~3 minuten)

```bash
python main.py --test
```

### Optie B: Kleine batch (50 gemeentes, ~45 minuten)

```bash
python main.py --limit 50
```

### Optie C: Volledige run (alle 303 gemeentes, ~3-4 uur)

```bash
python main.py
```

### Optie D: In background laten draaien (Mac/Linux)

```bash
nohup python main.py > scraper.log 2>&1 &

# Monitor voortgang
tail -f scraper.log
```

## Stap 5: Resultaten bekijken

Terwijl de scraper draait zie je:
```
Scraping gemeentes:  34%|████▍        | 102/300 [Contacts: 247, Mislukt: 12]
```

**Checkpoints** worden automatisch opgeslagen elke 10 gemeentes in `output/`:
- `checkpoint_10_YYYYMMDD_HHMMSS.xlsx`
- `checkpoint_20_YYYYMMDD_HHMMSS.xlsx`
- etc.

**Finale output** komt in `output/`:
- `vlaamse_gemeentes_contacts_YYYYMMDD_HHMMSS.xlsx`

## Stap 6: Excel openen

Ga naar de `output/` folder in VS Code en klik op het nieuwste `.xlsx` bestand.
Excel opent automatisch!

## Tips & Tricks

### ✅ Progress monitoren

Open 2de Terminal in VS Code (`Terminal → Split Terminal`):
```bash
# Terminal 1: Scraper draait hier
python main.py

# Terminal 2: Monitor logs
tail -f logs/scraper_*.log
```

### ✅ Onderbroken? Resume!

Als de scraper stopt, herstart vanaf laatste checkpoint:
```bash
# Check laatste checkpoint nummer in output/
# Bijv. checkpoint_30 gevonden? Start vanaf 30:
python main.py --start-from 30
```

### ✅ Sneller maken

Edit `src/config.py` en verlaag `rate_limit_seconds`:
```python
SCRAPER_CONFIG = {
    'rate_limit_seconds': 1,  # Sneller maar meer kans op blokkades
    ...
}
```

### ✅ Langzaam internet?

Verhoog timeouts in `src/config.py`:
```python
SCRAPER_CONFIG = {
    'timeout': 20,  # Was 10
    ...
}
```

## Troubleshooting

### ❌ "python: command not found"
→ Installeer Python: https://www.python.org/downloads/

### ❌ "pip: command not found"
→ Gebruik `python -m pip install -r requirements.txt`

### ❌ Permission denied
→ Run met administrator rechten of gebruik `sudo` (Mac/Linux)

### ❌ Module niet gevonden
→ Activeer virtual environment: `source venv/bin/activate`

### ❌ Excel kan niet openen
→ Installeer Excel of gebruik Google Sheets om `.xlsx` te openen

## Verwachte Output

Bij voltooiing zie je:
```
============================================================
Scraping voltooid!
============================================================

=== STATISTIEKEN ===
Unieke gemeentes: 285

Contacten per afdeling:
  Cultuur: 145
  Jeugd: 128
  Sport: 112
  Toerisme: 98
  Evenementen: 87
  Vrije Tijd: 76

✅ Resultaten opgeslagen in: output/vlaamse_gemeentes_contacts_20241217_143022.xlsx
```

## Klaar! 🎉

Je hebt nu een Excel bestand met alle gevonden contacten:
- Email adressen
- Namen
- Afdelingen (Cultuur, Jeugd, Sport, etc.)
- Gemeente en provincie
- Bron URLs

**Geen OCMW emails, geen spam - alleen relevante contacten!**
