"""
Configuratie voor de Vlaamse gemeente scraper.
"""

# Doelafdelingen om te zoeken
TARGET_DEPARTMENTS = [
    'cultuurdienst', 'cultuur',
    'jeugddienst', 'jeugd',
    'evenementen',
    'toerisme',
    'vrije tijd', 'vrijetijd',
    'sport', 'sportdienst',
    'provinciale domeinen', 'domeinen',
    'provinciale parken', 'parken'
]

# Keywords voor verschillende afdelingen (voor betere matching)
DEPARTMENT_KEYWORDS = {
    'Cultuur': ['cultuur', 'cultuurdienst', 'cultureel', 'cc ', 'cultuurcentrum'],
    'Jeugd': ['jeugd', 'jeugddienst', 'jongeren', 'jongerenwelzijn'],
    'Evenementen': ['evenement', 'event', 'feest', 'festiv'],
    'Toerisme': ['toerisme', 'toerist', 'vvv', 'bezoek'],
    'Vrije Tijd': ['vrije tijd', 'vrijetijd', 'recreatie', 'ontspanning'],
    'Sport': ['sport', 'sportdienst', 'sporthal', 'atletiek', 'zwembad'],
    'Domeinen': ['domein', 'provinciaal domein', 'park'],
    'Parken': ['park', 'groen', 'natuur']
}

# Mogelijke URL paden om te doorzoeken
SEARCH_PATHS = [
    '/contact',
    '/contacteer-ons',
    '/personeel',
    '/medewerkers',
    '/organisatie',
    '/diensten',
    '/bestuur',
    '/cultuur',
    '/jeugd',
    '/sport',
    '/toerisme',
    '/vrije-tijd',
    '/vrijetijd',
    '/evenementen',
    '/over-ons',
    '/cultuurcentrum',
    '/sportdienst',
    '/jeugddienst',
]

# Scraper instellingen
SCRAPER_CONFIG = {
    'rate_limit_seconds': 2,  # Verlaagd naar 2 voor snelheid (was 5)
    'timeout': 10,  # Verlaagd naar 10 (was 15)
    'max_retries': 2,  # Verlaagd naar 2 (was 3)
    'user_agent': 'Mozilla/5.0 (compatible; VlaamseGemeenteBot/1.0; +https://example.com/bot)',
    'respect_robots_txt': True,
    'max_pages_per_site': 15,  # Verlaagd naar 15 (was 20) voor snelheid
}

# Vlaamse gemeentes per provincie (volledige lijst)
# Bron: officiële lijst Vlaamse gemeentes 2024
MUNICIPALITIES = {
    'Antwerpen': [
        'Aartselaar', 'Antwerpen', 'Arendonk', 'Baarle-Hertog', 'Balen', 'Beerse',
        'Berlaar', 'Boechout', 'Bonheiden', 'Boom', 'Bornem', 'Borsbeek', 'Brasschaat',
        'Brecht', 'Dessel', 'Deurne', 'Duffel', 'Edegem', 'Essen', 'Geel', 'Grobbendonk',
        'Heist-op-den-Berg', 'Hemiksem', 'Herentals', 'Herenthout', 'Herselt', 'Hoogstraten',
        'Hove', 'Hulshout', 'Kalmthout', 'Kapellen', 'Kasterlee', 'Kontich', 'Laakdal',
        'Lier', 'Lille', 'Lint', 'Malle', 'Mechelen', 'Meerhout', 'Merksplas', 'Mol',
        'Mortsel', 'Niel', 'Nijlen', 'Olen', 'Oud-Turnhout', 'Putte', 'Puurs-Sint-Amands',
        'Ranst', 'Ravels', 'Retie', 'Rijkevorsel', 'Rumst', 'Schelle', 'Schilde', 'Schoten',
        'Sint-Katelijne-Waver', 'Stabroek', 'Turnhout', 'Vorselaar', 'Vosselaar', 'Westerlo',
        'Wijnegem', 'Willebroek', 'Wommelgem', 'Wuustwezel', 'Zandhoven', 'Zoersel', 'Zwijndrecht'
    ],
    'Limburg': [
        'Alken', 'As', 'Beringen', 'Bilzen', 'Bocholt', 'Borgloon', 'Bree', 'Diepenbeek',
        'Dilsen-Stokkem', 'Genk', 'Gingelom', 'Halen', 'Ham', 'Hamont-Achel', 'Hasselt',
        'Hechtel-Eksel', 'Heers', 'Herk-de-Stad', 'Herstappe', 'Heusden-Zolder', 'Hoeselt',
        'Houthalen-Helchteren', 'Kinrooi', 'Kortessem', 'Lanaken', 'Leopoldsburg', 'Lommel',
        'Lummen', 'Maaseik', 'Maasmechelen', 'Meeuwen-Gruitrode', 'Neerpelt', 'Nieuwerkerken',
        'Opglabbeek', 'Oudsbergen', 'Peer', 'Pelt', 'Riemst', 'Sint-Truiden', 'Tessenderlo',
        'Tongeren', 'Voeren', 'Wellen', 'Zonhoven', 'Zutendaal'
    ],
    'Oost-Vlaanderen': [
        'Aalst', 'Aalter', 'Assenede', 'Berlare', 'Beveren', 'Brakel', 'Buggenhout',
        'De Pinte', 'Deinze', 'Denderleeuw', 'Dendermonde', 'Destelbergen', 'Eeklo',
        'Erpe-Mere', 'Evergem', 'Gavere', 'Gent', 'Geraardsbergen', 'Haaltert', 'Hamme',
        'Herzele', 'Horebeke', 'Kaprijke', 'Kluisbergen', 'Knesselare', 'Kortrijk', 'Kruibeke',
        'Kruisem', 'Laarne', 'Lebbeke', 'Lede', 'Lierde', 'Lochristi', 'Lokeren', 'Maarkedal',
        'Maldegem', 'Melle', 'Merelbeke', 'Moerbeke', 'Nazareth', 'Ninove', 'Oosterzele',
        'Oudenaarde', 'Ronse', 'Sint-Gillis-Waas', 'Sint-Laureins', 'Sint-Lievens-Houtem',
        'Sint-Martens-Latem', 'Sint-Niklaas', 'Stekene', 'Temse', 'Waasmunster', 'Wachtebeke',
        'Wetteren', 'Wichelen', 'Wortegem-Petegem', 'Zele', 'Zelzate', 'Zingem', 'Zottegem',
        'Zulte', 'Zwalm'
    ],
    'Vlaams-Brabant': [
        'Aarschot', 'Affligem', 'Beersel', 'Begijnendijk', 'Bekkevoort', 'Bertem', 'Bever',
        'Bierbeek', 'Boortmeerbeek', 'Boutersem', 'Dilbeek', 'Drogenbos', 'Galmaarden',
        'Geetbets', 'Glabbeek', 'Gooik', 'Grimbergen', 'Haacht', 'Halle', 'Herent', 'Herne',
        'Hoegaarden', 'Hoeilaart', 'Holsbeek', 'Huldenberg', 'Kampenhout', 'Kapelle-op-den-Bos',
        'Keerbergen', 'Kortenaken', 'Kortenberg', 'Kraainem', 'Landen', 'Lennik', 'Leuven',
        'Liedekerke', 'Linkebeek', 'Linter', 'Londerzeel', 'Lubbeek', 'Machelen', 'Meise',
        'Merchtem', 'Opwijk', 'Oud-Heverlee', 'Overijse', 'Pepingen', 'Roosdaal', 'Rotselaar',
        'Scherpenheuvel-Zichem', 'Sint-Genesius-Rode', 'Sint-Pieters-Leeuw', 'Steenokkerzeel',
        'Ternat', 'Tervuren', 'Tielt-Winge', 'Tienen', 'Tremelo', 'Vilvoorde', 'Wemmel',
        'Wezembeek-Oppem', 'Zaventem', 'Zemst', 'Zoutleeuw'
    ],
    'West-Vlaanderen': [
        'Alveringem', 'Anzegem', 'Ardooie', 'Avelgem', 'Blankenberge', 'Bredene', 'Brugge',
        'Damme', 'De Haan', 'De Panne', 'Deerlijk', 'Dentergem', 'Diksmuide', 'Gistel',
        'Harelbeke', 'Heuvelland', 'Hooglede', 'Houthulst', 'Ichtegem', 'Ieper', 'Ingelmunster',
        'Izegem', 'Jabbeke', 'Knokke-Heist', 'Koekelare', 'Koksijde', 'Kortemark', 'Kortrijk',
        'Kuurne', 'Langemark-Poelkapelle', 'Ledegem', 'Lendelede', 'Lichtervelde', 'Lo-Reninge',
        'Menen', 'Mesen', 'Meulebeke', 'Middelkerke', 'Moorslede', 'Nieuwpoort', 'Oostende',
        'Oostkamp', 'Oostrozebeke', 'Oudenburg', 'Pittem', 'Poperinge', 'Roeselare', 'Ruiselede',
        'Spiere-Helkijn', 'Staden', 'Tielt', 'Torhout', 'Veurne', 'Vleteren', 'Waregem',
        'Wervik', 'Wevelgem', 'Wielsbeke', 'Wingene', 'Zedelgem', 'Zonnebeke', 'Zuienkerke',
        'Zwevegem'
    ]
}

def get_all_municipalities():
    """Retourneer een platte lijst van alle gemeentes."""
    all_munis = []
    for province, cities in MUNICIPALITIES.items():
        for city in cities:
            all_munis.append({'name': city, 'province': province})
    return all_munis

def get_municipality_count():
    """Tel het totaal aantal gemeentes."""
    return sum(len(cities) for cities in MUNICIPALITIES.values())
