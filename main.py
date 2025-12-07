#!/usr/bin/env python3
"""
Vlaamse Gemeente Contact Scraper

Dit script scrapt publieke contactgegevens van Vlaamse gemeentewebsites.
"""
import logging
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from tqdm import tqdm

# Voeg src directory toe aan path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from config import (
    get_all_municipalities,
    get_municipality_count,
    DEPARTMENT_KEYWORDS,
    SEARCH_PATHS,
    SCRAPER_CONFIG
)
from scraper import WebsiteFinder, PageScraper, ContactExtractor
from excel_exporter import ExcelExporter


def setup_logging(log_level: str = 'INFO', log_file: str = None):
    """
    Configureer logging.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Optioneel log bestand
    """
    # Maak logs directory
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)

    # Default log bestand met timestamp
    if not log_file:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = log_dir / f'scraper_{timestamp}.log'

    # Configureer formattering
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # File handler
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    logging.info(f"Logging gestart. Log bestand: {log_file}")


class MunicipalityScraper:
    """Hoofdklasse voor het scrapen van gemeentes."""

    def __init__(
        self,
        checkpoint_interval: int = 10,
        resume_from: str = None
    ):
        """
        Initialiseer de scraper.

        Args:
            checkpoint_interval: Aantal gemeentes tussen checkpoints
            resume_from: Optioneel checkpoint bestand om te resumeren
        """
        self.checkpoint_interval = checkpoint_interval
        self.resume_from = resume_from

        # Initialiseer componenten
        self.website_finder = WebsiteFinder(timeout=SCRAPER_CONFIG['timeout'])
        self.page_scraper = PageScraper(
            rate_limit=SCRAPER_CONFIG['rate_limit_seconds'],
            timeout=SCRAPER_CONFIG['timeout'],
            max_retries=SCRAPER_CONFIG['max_retries'],
            respect_robots=SCRAPER_CONFIG['respect_robots_txt'],
            user_agent=SCRAPER_CONFIG['user_agent'],
            max_pages=SCRAPER_CONFIG['max_pages_per_site']
        )
        self.contact_extractor = ContactExtractor(DEPARTMENT_KEYWORDS)
        self.exporter = ExcelExporter()

        # Resultaten
        self.all_results = []
        self.failed_municipalities = []

    def scrape_municipality(
        self,
        municipality: Dict
    ) -> List[Dict]:
        """
        Scrape een enkele gemeente.

        Args:
            municipality: Dictionary met 'name' en 'province'

        Returns:
            Lijst van gevonden contacts
        """
        name = municipality['name']
        province = municipality['province']

        logging.info(f"\n{'='*60}")
        logging.info(f"Scraping: {name} ({province})")
        logging.info(f"{'='*60}")

        # Stap 1: Vind website
        website = self.website_finder.find_municipality_website(name, province)

        if not website:
            logging.warning(f"Geen website gevonden voor {name}")
            self.failed_municipalities.append({
                'municipality': name,
                'province': province,
                'reason': 'Website niet gevonden'
            })
            return []

        # Stap 2: Scrape pagina's
        try:
            pages = self.page_scraper.scrape_site(website, SEARCH_PATHS)

            if not pages:
                logging.warning(f"Geen pagina's kunnen scrapen voor {name}")
                self.failed_municipalities.append({
                    'municipality': name,
                    'province': province,
                    'reason': 'Geen pagina\'s beschikbaar'
                })
                return []

        except Exception as e:
            logging.error(f"Fout bij scrapen van {name}: {e}")
            self.failed_municipalities.append({
                'municipality': name,
                'province': province,
                'reason': f'Scraping fout: {str(e)}'
            })
            return []

        # Stap 3: Extraheer contacts
        try:
            contacts = self.contact_extractor.extract_from_multiple_pages(pages)

            # Voeg gemeente en provincie toe
            for contact in contacts:
                contact['municipality'] = name
                contact['province'] = province

            logging.info(f"✓ {len(contacts)} contacts gevonden voor {name}")
            return contacts

        except Exception as e:
            logging.error(f"Fout bij extractie van {name}: {e}")
            self.failed_municipalities.append({
                'municipality': name,
                'province': province,
                'reason': f'Extractie fout: {str(e)}'
            })
            return []

    def run(self, limit: int = None, start_from: int = 0):
        """
        Voer de volledige scraping uit.

        Args:
            limit: Optioneel maximum aantal gemeentes
            start_from: Start vanaf gemeente index (voor resume)
        """
        municipalities = get_all_municipalities()

        if limit:
            municipalities = municipalities[:limit]

        if start_from > 0:
            logging.info(f"Resuming vanaf gemeente {start_from}")
            municipalities = municipalities[start_from:]

        total = len(municipalities)
        logging.info(f"\nStart scraping van {total} gemeentes...")
        logging.info(f"Checkpoint interval: elke {self.checkpoint_interval} gemeentes\n")

        # Progress bar
        with tqdm(total=total, desc="Scraping gemeentes", unit="gemeente") as pbar:
            for idx, municipality in enumerate(municipalities):
                # Scrape gemeente
                contacts = self.scrape_municipality(municipality)
                self.all_results.extend(contacts)

                # Update progress
                pbar.update(1)
                pbar.set_postfix({
                    'Contacts': len(self.all_results),
                    'Mislukt': len(self.failed_municipalities)
                })

                # Checkpoint
                if (idx + 1) % self.checkpoint_interval == 0:
                    self._save_checkpoint(idx + 1 + start_from)

        # Finale export
        logging.info("\n" + "="*60)
        logging.info("Scraping voltooid!")
        logging.info("="*60)

        self._save_final_results()
        self._save_failed_log()

    def _save_checkpoint(self, index: int):
        """Sla een checkpoint op."""
        logging.info(f"\n📝 Checkpoint opslaan (na {index} gemeentes)...")
        self.exporter.save_checkpoint(
            self.all_results,
            checkpoint_name=f'checkpoint_{index}'
        )

    def _save_final_results(self):
        """Sla de finale resultaten op."""
        if not self.all_results:
            logging.warning("Geen resultaten om op te slaan!")
            return

        logging.info("\n💾 Finale resultaten opslaan...")
        filepath = self.exporter.export_results(self.all_results)
        logging.info(f"\n✅ Resultaten opgeslagen in: {filepath}")

    def _save_failed_log(self):
        """Sla log van mislukte gemeentes op."""
        if not self.failed_municipalities:
            logging.info("\n✅ Alle gemeentes succesvol gescraped!")
            return

        log_dir = Path('logs')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        failed_log = log_dir / f'failed_municipalities_{timestamp}.txt'

        with open(failed_log, 'w', encoding='utf-8') as f:
            f.write("Mislukte Gemeentes\n")
            f.write("=" * 60 + "\n\n")

            for item in self.failed_municipalities:
                f.write(f"Gemeente: {item['municipality']}\n")
                f.write(f"Provincie: {item['province']}\n")
                f.write(f"Reden: {item['reason']}\n")
                f.write("-" * 60 + "\n")

        logging.warning(f"\n⚠️  {len(self.failed_municipalities)} gemeentes mislukt")
        logging.info(f"Details opgeslagen in: {failed_log}")


def main():
    """Hoofdfunctie."""
    parser = argparse.ArgumentParser(
        description='Scrape contactgegevens van Vlaamse gemeentes'
    )
    parser.add_argument(
        '--limit',
        type=int,
        help='Maximum aantal gemeentes om te scrapen (voor testen)'
    )
    parser.add_argument(
        '--start-from',
        type=int,
        default=0,
        help='Start vanaf gemeente index (voor resume)'
    )
    parser.add_argument(
        '--checkpoint-interval',
        type=int,
        default=10,
        help='Aantal gemeentes tussen checkpoints (default: 10)'
    )
    parser.add_argument(
        '--log-level',
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        help='Logging level (default: INFO)'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Test mode: scrape alleen eerste 5 gemeentes'
    )

    args = parser.parse_args()

    # Setup logging
    setup_logging(log_level=args.log_level)

    # Test mode
    if args.test:
        logging.info("🧪 TEST MODE - Scraping eerste 5 gemeentes")
        args.limit = 5

    # Print configuratie
    total_count = get_municipality_count()
    logging.info("\n" + "="*60)
    logging.info("VLAAMSE GEMEENTE CONTACT SCRAPER")
    logging.info("="*60)
    logging.info(f"Totaal aantal Vlaamse gemeentes: {total_count}")
    if args.limit:
        logging.info(f"Limiet ingesteld: {args.limit} gemeentes")
    logging.info("="*60 + "\n")

    # Start scraper
    scraper = MunicipalityScraper(
        checkpoint_interval=args.checkpoint_interval
    )

    try:
        scraper.run(limit=args.limit, start_from=args.start_from)
    except KeyboardInterrupt:
        logging.info("\n\n⚠️  Scraping onderbroken door gebruiker")
        logging.info("Tussentijdse resultaten worden opgeslagen...")
        scraper._save_checkpoint('interrupted')
        scraper._save_failed_log()
        sys.exit(0)
    except Exception as e:
        logging.error(f"\n❌ Fatale fout: {e}", exc_info=True)
        logging.info("Tussentijdse resultaten worden opgeslagen...")
        scraper._save_checkpoint('error')
        scraper._save_failed_log()
        sys.exit(1)


if __name__ == '__main__':
    main()
