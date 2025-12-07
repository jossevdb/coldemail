# Vlaamse Gemeente Contact Scraper

Een professionele Python web scraper voor het verzamelen van publieke contactgegevens van Vlaamse gemeentewebsites.

## Doel

Dit tool verzamelt e-mailadressen en namen van medewerkers die werken bij specifieke afdelingen in alle 300+ Vlaamse gemeentes in België.

### Doelafdelingen

- Cultuurdienst / Cultuur
- Jeugddienst / Jeugd
- Dienst evenementen / Evenementen
- Dienst toerisme / Toerisme
- Dienst vrije tijd / Vrije tijd
- Dienst sport / Sport
- Provinciale domeinen
- Provinciale parken

## Features

✅ **Automatische website detectie** - Vindt automatisch officiële gemeente websites
✅ **Robots.txt respect** - Respecteert robots.txt van elke website
✅ **Rate limiting** - 3 seconden tussen requests om servers niet te overbelasten
✅ **Smart extractie** - Intelligente matching van e-mails met afdelingen
✅ **Excel export** - Geformatteerde Excel output met statistieken
✅ **Progress tracking** - Real-time voortgang met tqdm
✅ **Checkpoint systeem** - Automatische tussentijdse opslag
✅ **Error handling** - Robuuste foutafhandeling en retry mechanisme
✅ **Gedetailleerde logging** - Volledige logs van alle acties

## Vereisten

- Python 3.8 of hoger
- Internet connectie

## Installatie

1. Clone deze repository:
```bash
git clone <repository-url>
cd coldemail
```

2. Installeer dependencies:
```bash
pip install -r requirements.txt
```

## Gebruik

### Basis gebruik

Scrape alle 300+ Vlaamse gemeentes:

```bash
python main.py
```

### Test mode

Test eerst met 5 gemeentes:

```bash
python main.py --test
```

### Geavanceerde opties

```bash
# Scrape alleen de eerste 20 gemeentes
python main.py --limit 20

# Start vanaf gemeente 50 (voor resume)
python main.py --start-from 50

# Pas checkpoint interval aan (default: 10)
python main.py --checkpoint-interval 25

# Debug mode met gedetailleerde logging
python main.py --log-level DEBUG

# Combineer opties
python main.py --limit 50 --checkpoint-interval 5 --log-level DEBUG
```

## Output

### Excel bestanden

Resultaten worden opgeslagen in de `output/` directory:

- **Hoofdbestand**: `vlaamse_gemeentes_contacts_YYYYMMDD_HHMMSS.xlsx`
- **Checkpoints**: `checkpoint_N_YYYYMMDD_HHMMSS.xlsx` (elke N gemeentes)

#### Excel kolommen:

| Kolom | Beschrijving |
|-------|-------------|
| Gemeente | Naam van de gemeente |
| Provincie | Provincie (Antwerpen, Limburg, etc.) |
| Afdeling | Gematchte afdeling (Cultuur, Jeugd, etc.) |
| Naam | Naam van de contactpersoon |
| E-mailadres | E-mailadres |
| Bron URL | URL waar de info gevonden werd |
| Datum verzameld | Datum van scraping |
| Context | Tekstuele context rond het e-mailadres |

### Logbestanden

Logs worden opgeslagen in de `logs/` directory:

- **Scraper log**: `scraper_YYYYMMDD_HHMMSS.log` - Volledige log van alle acties
- **Failed log**: `failed_municipalities_YYYYMMDD_HHMMSS.txt` - Lijst van mislukte gemeentes

## Projectstructuur

```
coldemail/
├── main.py                      # Hoofdscript
├── requirements.txt             # Python dependencies
├── README.md                    # Deze file
├── .gitignore                   # Git ignore configuratie
├── src/
│   ├── config.py               # Configuratie en gemeente lijst
│   ├── excel_exporter.py       # Excel export functionaliteit
│   └── scraper/
│       ├── __init__.py
│       ├── website_finder.py   # Website detectie
│       ├── page_scraper.py     # Pagina scraping met robots.txt
│       └── contact_extractor.py # Contact extractie logica
├── data/                        # (wordt aangemaakt)
├── logs/                        # Log bestanden
└── output/                      # Excel exports
```

## Configuratie

Pas instellingen aan in `src/config.py`:

### Scraper instellingen

```python
SCRAPER_CONFIG = {
    'rate_limit_seconds': 3,      # Wacht tijd tussen requests
    'timeout': 15,                 # Request timeout
    'max_retries': 3,              # Max retries bij falen
    'respect_robots_txt': True,    # Respecteer robots.txt
    'max_pages_per_site': 20,      # Max pagina's per gemeente
}
```

### URL paden

Voeg extra zoekpaden toe in `SEARCH_PATHS`:

```python
SEARCH_PATHS = [
    '/contact',
    '/personeel',
    '/organisatie',
    # ... voeg meer paden toe
]
```

### Afdeling keywords

Pas keywords aan in `DEPARTMENT_KEYWORDS` voor betere matching.

## Ethische web scraping

Deze tool volgt best practices voor ethische web scraping:

✅ **Respecteert robots.txt** - Blokkeert toegang tot verboden URLs
✅ **Rate limiting** - Voorkomt server overbelasting
✅ **User-agent** - Identificeert zich duidelijk
✅ **Publieke data** - Verzamelt alleen publiek beschikbare informatie
✅ **Timeout handling** - Respecteert server response tijden
✅ **Error recovery** - Graceful degradation bij fouten

## Troubleshooting

### Geen resultaten voor bepaalde gemeentes

Sommige gemeentes hebben:
- Geen officiële website
- Contactgegevens achter login/forms
- JavaScript-heavy websites (niet ondersteund)
- Ongebruikelijke URL structuren

Check de `failed_municipalities_*.txt` log voor details.

### Script crasht

Bij een crash:
1. Check de laatste checkpoint in `output/`
2. Resume met: `python main.py --start-from N` (N = laatste checkpoint nummer)
3. Check de log bestanden voor error details

### Rate limiting errors

Als je 429 (Too Many Requests) errors krijgt:
1. Verhoog `rate_limit_seconds` in config.py
2. Verlaag `max_pages_per_site`

### Memory issues

Bij grote scrapting runs:
1. Verlaag `checkpoint_interval` (sla vaker op)
2. Verhoog `rate_limit_seconds` (langzamer scrapen)

## Privacy & Legal

⚠️ **Belangrijke opmerkingen:**

- Deze tool verzamelt alleen **publiek beschikbare** informatie
- Gebruik de data **verantwoordelijk** en volgens GDPR richtlijnen
- Respecteer de privacy van individuen
- Gebruik voor legitieme doeleinden (onderzoek, netwerken, etc.)
- Niet voor spam of ongewenste marketing

## Licentie

Dit project is ontwikkeld voor educatieve en onderzoeksdoeleinden.

## Contributing

Suggesties en verbeteringen zijn welkom! Open een issue of pull request.

## Support

Bij problemen of vragen:
1. Check de logs in `logs/`
2. Lees deze README grondig
3. Open een GitHub issue met details

## Changelog

### v1.0.0 (2024-12-07)
- Initiële release
- Support voor alle 300+ Vlaamse gemeentes
- Automatische website detectie
- Smart contact extractie
- Excel export met styling
- Checkpoint systeem
- Gedetailleerde logging

---

**Ontwikkeld met ❤️ voor transparante overheid en open data**
