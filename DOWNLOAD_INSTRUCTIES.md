# Code Downloaden

## Optie 1: Download via Git (als je toegang hebt tot de repository)

```bash
git clone https://github.com/jossevdb/coldemail.git
cd coldemail
```

## Optie 2: Download als ZIP

1. Ga naar de GitHub repository
2. Klik op groene **Code** knop
3. Klik **Download ZIP**
4. Unzip het bestand
5. Open de folder in VS Code

## Optie 3: Handmatig (als bovenstaande niet werkt)

Vraag Claude Code om een tar.gz of zip te maken van alle bestanden.

## Na downloaden:

```bash
cd coldemail
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
python main.py --test
```
