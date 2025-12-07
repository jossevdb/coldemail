"""
Module voor het vinden van officiële gemeente websites.
"""
import logging
import time
import requests
from urllib.parse import urlparse
from typing import Optional

logger = logging.getLogger(__name__)


class WebsiteFinder:
    """Vindt de officiële website van een gemeente."""

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; VlaamseGemeenteBot/1.0)'
        })

    def find_municipality_website(self, municipality: str, province: str) -> Optional[str]:
        """
        Probeer de officiële website van een gemeente te vinden.

        Args:
            municipality: Naam van de gemeente
            province: Naam van de provincie

        Returns:
            URL van de website of None als niet gevonden
        """
        # Standaard patronen voor Vlaamse gemeente websites
        patterns = self._generate_url_patterns(municipality)

        for url in patterns:
            try:
                logger.debug(f"Probeer URL: {url}")
                response = self.session.head(url, timeout=self.timeout, allow_redirects=True)

                if response.status_code == 200:
                    final_url = response.url
                    logger.info(f"Website gevonden voor {municipality}: {final_url}")
                    return final_url

            except requests.RequestException as e:
                logger.debug(f"Fout bij {url}: {str(e)}")
                continue

            # Rate limiting
            time.sleep(0.5)

        logger.warning(f"Geen website gevonden voor {municipality}")
        return None

    def _generate_url_patterns(self, municipality: str) -> list:
        """
        Genereer mogelijke URL patronen voor een gemeente.

        Args:
            municipality: Naam van de gemeente

        Returns:
            Lijst van mogelijke URLs
        """
        # Normaliseer gemeente naam (lowercase, vervang spaties en speciale tekens)
        normalized = municipality.lower()
        normalized = normalized.replace(' ', '-')
        normalized = normalized.replace("'", '')

        # Speciale gevallen
        special_cases = {
            'sint-': 'sint',
            'st-': 'sint',
            'ste-': 'sint',
        }

        for old, new in special_cases.items():
            if normalized.startswith(old):
                normalized_alt = normalized.replace(old, new, 1)
                break
        else:
            normalized_alt = normalized

        # Genereer patronen
        patterns = [
            f"https://www.{normalized}.be",
            f"https://{normalized}.be",
            f"https://www.{normalized_alt}.be",
            f"https://{normalized_alt}.be",
            f"https://www.gemeente{normalized}.be",
            f"https://gemeente{normalized}.be",
            f"https://www.stad{normalized}.be",
            f"https://stad{normalized}.be",
        ]

        return patterns

    def verify_website(self, url: str) -> bool:
        """
        Verifieer of een website bereikbaar is.

        Args:
            url: URL om te verifiëren

        Returns:
            True als website bereikbaar is
        """
        try:
            response = self.session.head(url, timeout=self.timeout, allow_redirects=True)
            return response.status_code == 200
        except requests.RequestException:
            return False
