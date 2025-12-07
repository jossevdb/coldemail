"""
Module voor het extraheren van contactgegevens uit HTML.
"""
import re
import logging
from bs4 import BeautifulSoup
from typing import List, Dict, Optional, Set
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class Contact:
    """Dataklasse voor een contact."""
    name: Optional[str]
    email: str
    department: Optional[str]
    context: str  # Tekst rondom het e-mailadres voor context


class ContactExtractor:
    """Extraheert contactgegevens uit HTML content."""

    # Regex pattern voor e-mailadressen
    EMAIL_PATTERN = re.compile(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    )

    # Pattern voor namen (voor Vlaamse context)
    # Zoekt naar woorden die beginnen met hoofdletter, typisch voor namen
    NAME_PATTERN = re.compile(
        r'\b([A-Z][a-z]+(?:\s+(?:van|de|den|der|de la|von)\s+)?(?:[A-Z][a-z]+)+)\b'
    )

    def __init__(self, department_keywords: Dict[str, List[str]]):
        """
        Initialiseer de extractor.

        Args:
            department_keywords: Dictionary met afdelingen en hun keywords
        """
        self.department_keywords = department_keywords

    def extract_emails(self, html: str) -> List[str]:
        """
        Extraheer alle e-mailadressen uit HTML.

        Args:
            html: HTML content

        Returns:
            Lijst van e-mailadressen
        """
        # Verwijder JavaScript en CSS
        soup = BeautifulSoup(html, 'lxml')
        for script in soup(['script', 'style']):
            script.decompose()

        text = soup.get_text()

        # Vind alle e-mailadressen
        emails = self.EMAIL_PATTERN.findall(text)

        # Filter spam/generic emails
        emails = [
            email for email in emails
            if not self._is_generic_email(email)
        ]

        return list(set(emails))  # Unieke emails

    def _is_generic_email(self, email: str) -> bool:
        """
        Controleer of een e-mail generiek/spam is.

        Args:
            email: E-mailadres

        Returns:
            True als generiek
        """
        generic_patterns = [
            'noreply', 'no-reply', 'mailer', 'postmaster',
            'webmaster', 'admin', 'example.com', 'test@',
            'spam', 'abuse', 'privacy'
        ]

        email_lower = email.lower()
        return any(pattern in email_lower for pattern in generic_patterns)

    def extract_context(self, html: str, email: str, window: int = 200) -> str:
        """
        Extraheer de tekstuele context rondom een e-mailadres.

        Args:
            html: HTML content
            email: E-mailadres om context voor te vinden
            window: Aantal karakters voor en na het e-mailadres

        Returns:
            Context string
        """
        soup = BeautifulSoup(html, 'lxml')
        text = soup.get_text()

        # Vind de positie van het e-mailadres
        pos = text.find(email)
        if pos == -1:
            return ""

        # Extraheer context
        start = max(0, pos - window)
        end = min(len(text), pos + len(email) + window)

        context = text[start:end]

        # Cleanup: vervang multiple whitespaces
        context = re.sub(r'\s+', ' ', context).strip()

        return context

    def extract_name_from_context(self, context: str, email: str) -> Optional[str]:
        """
        Probeer een naam te extraheren uit de context.

        Args:
            context: Context string
            email: E-mailadres (kan hints bevatten)

        Returns:
            Naam of None
        """
        # Zoek naar namen in de context
        names = self.NAME_PATTERN.findall(context)

        if names:
            # Kies de naam die het dichtst bij het e-mailadres staat
            return names[0] if isinstance(names[0], str) else names[0][0]

        # Probeer naam uit e-mailadres te halen
        local_part = email.split('@')[0]

        # Check voor voornaam.achternaam pattern
        if '.' in local_part:
            parts = local_part.split('.')
            if len(parts) == 2:
                firstname = parts[0].capitalize()
                lastname = parts[1].capitalize()
                return f"{firstname} {lastname}"

        return None

    def match_department(self, context: str) -> Optional[str]:
        """
        Match een afdeling op basis van context.

        Args:
            context: Context string

        Returns:
            Afdeling naam of None
        """
        context_lower = context.lower()

        # Score per afdeling
        scores = {}

        for department, keywords in self.department_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword.lower() in context_lower:
                    score += 1

            if score > 0:
                scores[department] = score

        if scores:
            # Retourneer afdeling met hoogste score
            best_department = max(scores, key=scores.get)
            logger.debug(f"Matched department: {best_department} (score: {scores[best_department]})")
            return best_department

        return None

    def extract_contacts(self, html: str, url: str) -> List[Contact]:
        """
        Extraheer alle contacts uit HTML.

        Args:
            html: HTML content
            url: URL van de pagina (voor logging)

        Returns:
            Lijst van Contact objecten
        """
        emails = self.extract_emails(html)
        contacts = []

        for email in emails:
            context = self.extract_context(html, email)
            name = self.extract_name_from_context(context, email)
            department = self.match_department(context)

            # Alleen opslaan als we een afdeling hebben kunnen matchen
            # OF als de context relevant lijkt
            if department or self._context_seems_relevant(context):
                contact = Contact(
                    name=name,
                    email=email,
                    department=department,
                    context=context
                )
                contacts.append(contact)
                logger.debug(f"Contact gevonden: {email} ({department})")

        logger.info(f"Gevonden {len(contacts)} relevante contacts op {url}")
        return contacts

    def _context_seems_relevant(self, context: str) -> bool:
        """
        Controleer of de context relevant lijkt voor onze doelafdelingen.

        Args:
            context: Context string

        Returns:
            True als relevant
        """
        relevant_terms = [
            'dienst', 'afdeling', 'medewerker', 'contactpersoon',
            'coordinator', 'verantwoordelijke', 'schepen', 'ambtenaar'
        ]

        context_lower = context.lower()
        return any(term in context_lower for term in relevant_terms)

    def extract_from_multiple_pages(
        self,
        pages: Dict[str, str]
    ) -> List[Dict]:
        """
        Extraheer contacts van meerdere pagina's.

        Args:
            pages: Dictionary met URL -> HTML content

        Returns:
            Lijst van contact dictionaries
        """
        all_contacts = []
        seen_emails = set()

        for url, html in pages.items():
            contacts = self.extract_contacts(html, url)

            for contact in contacts:
                # Voorkom duplicaten
                if contact.email not in seen_emails:
                    seen_emails.add(contact.email)

                    all_contacts.append({
                        'name': contact.name,
                        'email': contact.email,
                        'department': contact.department,
                        'url': url,
                        'context': contact.context[:100]  # Beperk context lengte
                    })

        return all_contacts
