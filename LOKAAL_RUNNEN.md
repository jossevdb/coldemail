# Lokaal Runnen - Instructies

## Stap 1: Download de code

```bash
git clone <jouw-repository-url>
cd coldemail
```

## Stap 2: Setup Python omgeving

```bash
# Maak virtual environment
python3 -m venv venv

# Activeer (Mac/Linux)
source venv/bin/activate

# OF Windows
venv\Scripts\activate

# Installeer dependencies
pip install -r requirements.txt
```

## Stap 3: Run de scraper

```bash
# Volledige run (alle 303 gemeentes)
python main.py

# Of start met een kleinere batch
python main.py --limit 50

# In background met nohup (blijft draaien)
nohup python main.py > scraper.log 2>&1 &

# Monitor voortgang
tail -f scraper.log
```

## Voordelen lokaal:
- ✅ Geen automatische stops
- ✅ Kan uren/dagen doorlopen
- ✅ Automatische checkpoints elke 10 gemeentes
- ✅ Bij crash: herstart vanaf laatste checkpoint

## Tips:
- Laat je computer aanstaan tijdens scraping
- Check periodiek de logs: `tail -f logs/scraper_*.log`
- Checkpoints worden automatisch opgeslagen in `output/`
- Finale Excel bestand komt in `output/` wanneer klaar
