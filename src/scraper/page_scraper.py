"""
Module voor het scrapen van webpagina's met respect voor robots.txt.
"""
import logging
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser
from typing import List, Set, Optional, Dict
import re

logger = logging.getLogger(__name__)


class PageScraper:
    """Scrapt webpagina's met rate limiting en robots.txt respect."""

    def __init__(
        self,
        rate_limit: float = 3.0,
        timeout: int = 15,
        max_retries: int = 3,
        respect_robots: bool = True,
        user_agent: str = 'Mozilla/5.0 (compatible; VlaamseGemeenteBot/1.0)',
        max_pages: int = 20
    ):
        """
        Initialiseer de scraper.

        Args:
            rate_limit: Seconden te wachten tussen requests
            timeout: Request timeout in seconden
            max_retries: Maximum aantal retries
            respect_robots: Of robots.txt gerespecteerd moet worden
            user_agent: User agent string
            max_pages: Maximum aantal pagina's per site
        """
        self.rate_limit = rate_limit
        self.timeout = timeout
        self.max_retries = max_retries
        self.respect_robots = respect_robots
        self.user_agent = user_agent
        self.max_pages = max_pages

        self.session = requests.Session()
        self.session.headers.update({'User-Agent': user_agent})

        self.robots_cache: Dict[str, RobotFileParser] = {}
        self.last_request_time = 0

    def can_fetch(self, url: str) -> bool:
        """
        Controleer of we de URL mogen fetchen volgens robots.txt.

        Args:
            url: URL om te controleren

        Returns:
            True als fetch toegestaan is
        """
        if not self.respect_robots:
            return True

        parsed = urlparse(url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"

        # Check cache
        if base_url not in self.robots_cache:
            robots_url = urljoin(base_url, '/robots.txt')
            rp = RobotFileParser()
            rp.set_url(robots_url)

            try:
                rp.read()
                self.robots_cache[base_url] = rp
                logger.debug(f"Robots.txt geladen voor {base_url}")
            except Exception as e:
                logger.warning(f"Kan robots.txt niet laden voor {base_url}: {e}")
                # Als robots.txt niet bestaat, sta alles toe
                self.robots_cache[base_url] = None

        rp = self.robots_cache[base_url]
        if rp is None:
            return True

        can_fetch = rp.can_fetch(self.user_agent, url)
        if not can_fetch:
            logger.info(f"URL geblokkeerd door robots.txt: {url}")

        return can_fetch

    def _apply_rate_limit(self):
        """Pas rate limiting toe."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time

        if time_since_last < self.rate_limit:
            sleep_time = self.rate_limit - time_since_last
            logger.debug(f"Rate limiting: wacht {sleep_time:.2f}s")
            time.sleep(sleep_time)

        self.last_request_time = time.time()

    def fetch_page(self, url: str) -> Optional[str]:
        """
        Haal een pagina op met retries en error handling.

        Args:
            url: URL om op te halen

        Returns:
            HTML content of None bij falen
        """
        if not self.can_fetch(url):
            return None

        self._apply_rate_limit()

        for attempt in range(self.max_retries):
            try:
                logger.debug(f"Fetching {url} (poging {attempt + 1}/{self.max_retries})")
                response = self.session.get(url, timeout=self.timeout, allow_redirects=True)

                if response.status_code == 200:
                    return response.text
                else:
                    logger.warning(f"Status {response.status_code} voor {url}")

            except requests.Timeout:
                logger.warning(f"Timeout voor {url}")
            except requests.RequestException as e:
                logger.warning(f"Request fout voor {url}: {str(e)}")

            if attempt < self.max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff

        logger.error(f"Gefaald om {url} op te halen na {self.max_retries} pogingen")
        return None

    def extract_links(self, html: str, base_url: str, search_paths: List[str]) -> Set[str]:
        """
        Extraheer relevante links van een pagina.

        Args:
            html: HTML content
            base_url: Base URL van de pagina
            search_paths: Lijst van relevante paden om te zoeken

        Returns:
            Set van relevante URLs
        """
        soup = BeautifulSoup(html, 'lxml')
        links = set()

        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            full_url = urljoin(base_url, href)

            # Controleer of URL relevant is
            parsed = urlparse(full_url)

            # Alleen links van dezelfde site
            if not full_url.startswith(base_url):
                continue

            # Check of pad relevant is
            path_lower = parsed.path.lower()
            if any(search_path in path_lower for search_path in search_paths):
                links.add(full_url)

        logger.debug(f"Gevonden {len(links)} relevante links op {base_url}")
        return links

    def scrape_site(
        self,
        base_url: str,
        search_paths: List[str]
    ) -> Dict[str, str]:
        """
        Scrape een hele site voor relevante pagina's.

        Args:
            base_url: Base URL van de site
            search_paths: Lijst van relevante paden

        Returns:
            Dictionary met URL -> HTML content
        """
        results = {}
        visited = set()
        to_visit = {base_url}

        # Voeg directe pad combinaties toe
        for path in search_paths:
            to_visit.add(urljoin(base_url, path))

        page_count = 0

        while to_visit and page_count < self.max_pages:
            url = to_visit.pop()

            if url in visited:
                continue

            visited.add(url)
            html = self.fetch_page(url)

            if html:
                results[url] = html
                page_count += 1

                # Extraheer nieuwe links (alleen van homepage)
                if url == base_url:
                    new_links = self.extract_links(html, base_url, search_paths)
                    to_visit.update(new_links - visited)

        logger.info(f"Gescraped {len(results)} pagina's van {base_url}")
        return results
