"""
Text generators for SynGen.

This module provides generators for various text data types
such as emails, phone numbers, addresses, and names.
"""

import numpy as np
import random
import string
from typing import Dict, Any, List


class TextGenerator:
    """Generator for text data types."""

    def __init__(self):
        """Initialize the text generator."""
        self.first_names = [
            "James",
            "Mary",
            "John",
            "Patricia",
            "Robert",
            "Jennifer",
            "Michael",
            "Linda",
            "William",
            "Elizabeth",
            "David",
            "Barbara",
            "Richard",
            "Susan",
            "Joseph",
            "Jessica",
            "Thomas",
            "Sarah",
            "Christopher",
            "Karen",
            "Charles",
            "Nancy",
            "Daniel",
            "Lisa",
            "Matthew",
            "Betty",
            "Anthony",
            "Helen",
            "Mark",
            "Sandra",
            "Donald",
            "Donna",
            "Steven",
            "Carol",
            "Paul",
            "Ruth",
            "Andrew",
            "Sharon",
            "Joshua",
            "Michelle",
        ]

        self.last_names = [
            "Smith",
            "Johnson",
            "Williams",
            "Brown",
            "Jones",
            "Garcia",
            "Miller",
            "Davis",
            "Rodriguez",
            "Martinez",
            "Hernandez",
            "Lopez",
            "Gonzalez",
            "Wilson",
            "Anderson",
            "Thomas",
            "Taylor",
            "Moore",
            "Jackson",
            "Martin",
            "Lee",
            "Perez",
            "Thompson",
            "White",
            "Harris",
            "Sanchez",
            "Clark",
            "Ramirez",
            "Lewis",
            "Robinson",
            "Walker",
            "Young",
            "Allen",
            "King",
            "Wright",
            "Scott",
            "Torres",
            "Nguyen",
            "Hill",
            "Flores",
        ]

        self.domains = [
            "gmail.com",
            "yahoo.com",
            "hotmail.com",
            "outlook.com",
            "aol.com",
            "icloud.com",
            "protonmail.com",
            "mail.com",
            "yandex.com",
            "zoho.com",
        ]

        self.street_names = [
            "Main",
            "Oak",
            "Pine",
            "Elm",
            "Cedar",
            "Maple",
            "Washington",
            "Lake",
            "Hill",
            "Park",
            "Spring",
            "North",
            "South",
            "East",
            "West",
            "River",
            "Forest",
            "Meadow",
            "Sunset",
            "Sunrise",
            "Valley",
            "Mountain",
            "Ocean",
            "Beach",
            "Garden",
            "Plaza",
        ]

        self.street_types = [
            "Street",
            "Avenue",
            "Road",
            "Boulevard",
            "Drive",
            "Lane",
            "Court",
            "Place",
            "Way",
            "Circle",
            "Terrace",
            "Highway",
            "Expressway",
            "Freeway",
        ]

        self.cities = [
            "New York",
            "Los Angeles",
            "Chicago",
            "Houston",
            "Phoenix",
            "Philadelphia",
            "San Antonio",
            "San Diego",
            "Dallas",
            "San Jose",
            "Austin",
            "Jacksonville",
            "Fort Worth",
            "Columbus",
            "Charlotte",
            "San Francisco",
            "Indianapolis",
            "Seattle",
            "Denver",
            "Washington",
            "Boston",
            "El Paso",
            "Nashville",
            "Detroit",
        ]

        self.states = [
            "AL",
            "AK",
            "AZ",
            "AR",
            "CA",
            "CO",
            "CT",
            "DE",
            "FL",
            "GA",
            "HI",
            "ID",
            "IL",
            "IN",
            "IA",
            "KS",
            "KY",
            "LA",
            "ME",
            "MD",
            "MA",
            "MI",
            "MN",
            "MS",
            "MO",
            "MT",
            "NE",
            "NV",
            "NH",
            "NJ",
            "NM",
            "NY",
            "NC",
            "ND",
            "OH",
            "OK",
            "OR",
            "PA",
            "RI",
            "SC",
            "SD",
            "TN",
            "TX",
            "UT",
            "VT",
            "VA",
            "WA",
            "WV",
            "WI",
            "WY",
        ]

    def generate_emails(self, parameters: Dict[str, Any], n_samples: int) -> np.ndarray:
        """Generate email addresses."""
        emails = []

        # Check if categories are provided (for categorical distribution)
        if "categories" in parameters and parameters["categories"]:
            # Use provided categories
            categories = parameters["categories"]
            if isinstance(categories, str):
                categories = [
                    cat.strip() for cat in categories.split(",") if cat.strip()
                ]

            # Sample from provided categories
            return np.random.choice(categories, size=n_samples, replace=True)

        # Get parameters with defaults
        format_type = parameters.get("format", "first.last")
        add_numbers = parameters.get("add_numbers", False)
        # Accept multiple possible keys for domains coming from different UIs
        custom_domains = (
            parameters.get("custom_domains")
            or parameters.get("domains")
            or parameters.get("domain")
            or ""
        )

        # Use custom domains if provided, otherwise use defaults
        if custom_domains and str(custom_domains).strip():
            # Support both string (comma-separated) and list inputs
            if isinstance(custom_domains, (list, tuple)):
                domains = [str(d).strip() for d in custom_domains if str(d).strip()]
            else:
                domains = [
                    d.strip() for d in str(custom_domains).split(",") if d.strip()
                ]
        else:
            # Provide special domains for 'business' format when none specified
            if format_type == "business":
                domains = [
                    "company.com",
                    "business.com",
                    "enterprise.com",
                    "corporate.com",
                    "example.com",
                ]
            else:
                domains = self.domains

        for _ in range(n_samples):
            # Generate name
            first_name = random.choice(self.first_names).lower()
            last_name = random.choice(self.last_names).lower()

            # Normalize high-level format keywords to concrete patterns
            normalized_format = format_type
            if format_type == "simple":
                normalized_format = "first"
            elif format_type == "realistic":
                normalized_format = "first.last"
            elif format_type == "business":
                normalized_format = "first.last"

            # Generate email format
            if normalized_format == "first.last":
                email = f"{first_name}.{last_name}"
            elif normalized_format == "firstlast":
                email = f"{first_name}{last_name}"
            elif normalized_format == "first_last":
                email = f"{first_name}_{last_name}"
            elif normalized_format == "first":
                email = first_name
            else:
                email = f"{first_name}.{last_name}"

            # Add random numbers if requested
            if add_numbers:
                email += str(random.randint(1, 999))

            # Add domain
            domain = random.choice(domains)
            email = f"{email}@{domain}"

            emails.append(email)

        return np.array(emails)

    def generate_phones(self, parameters: Dict[str, Any], n_samples: int) -> np.array:
        """Generate phone numbers."""
        phones = []

        # Check if categories are provided (for categorical distribution)
        if "categories" in parameters and parameters["categories"]:
            # Use provided categories
            categories = parameters["categories"]
            if isinstance(categories, str):
                categories = [
                    cat.strip() for cat in categories.split(",") if cat.strip()
                ]

            # Sample from provided categories
            return np.random.choice(categories, size=n_samples, replace=True)

        format_type = parameters.get("format", "us")
        country_code = parameters.get("country_code", "1")
        include_extensions = parameters.get("include_extensions", False)

        for _ in range(n_samples):
            if format_type == "us":
                # US format: (XXX) XXX-XXXX
                area_code = random.randint(200, 999)
                prefix = random.randint(200, 999)
                line_number = random.randint(1000, 9999)
                phone = f"({area_code}) {prefix}-{line_number}"
            elif format_type == "international":
                # International format: +X-XXX-XXX-XXXX
                area_code = random.randint(10, 999)
                prefix = random.randint(100, 999)
                line_number = random.randint(1000, 9999)
                phone = f"+{country_code}-{area_code}-{prefix}-{line_number}"
            else:
                # Simple format: XXX-XXX-XXXX
                area_code = random.randint(100, 999)
                prefix = random.randint(100, 999)
                line_number = random.randint(1000, 9999)
                phone = f"{area_code}-{prefix}-{line_number}"

            # Add extension if requested
            if include_extensions:
                extension = random.randint(100, 999)
                phone += f" x{extension}"

            phones.append(phone)

        return np.array(phones)

    def generate_addresses(
        self, parameters: Dict[str, Any], n_samples: int
    ) -> np.array:
        """Generate street addresses."""
        addresses = []

        # Check if categories are provided (for categorical distribution)
        if "categories" in parameters and parameters["categories"]:
            # Use provided categories
            categories = parameters["categories"]
            if isinstance(categories, str):
                categories = [
                    cat.strip() for cat in categories.split(",") if cat.strip()
                ]

            # Sample from provided categories
            return np.random.choice(categories, size=n_samples, replace=True)

        country = parameters.get("country", "US")
        include_zip = parameters.get("include_zip", True)
        street_format = parameters.get("street_format", "number_name_type")

        # Country-specific configurations
        country_configs = {
            "US": {
                "cities": self.cities,
                "states": self.states,
                "zip_format": lambda: str(random.randint(10000, 99999)),
            },
            "CA": {
                "cities": [
                    "Toronto",
                    "Montreal",
                    "Vancouver",
                    "Calgary",
                    "Edmonton",
                    "Ottawa",
                ],
                "states": ["ON", "QC", "BC", "AB", "SK", "MB"],
                "zip_format": lambda: f"{random.choice('ABCEGHJKLMNPRSTVWXYZ')}{random.randint(0,9)} {random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)} {random.choice('ABCEGHJKLMNPRSTVWXYZ')}{random.choice('ABCEGHJKLMNPRSTVWXYZ')}",
            },
            "UK": {
                "cities": [
                    "London",
                    "Birmingham",
                    "Manchester",
                    "Liverpool",
                    "Leeds",
                    "Sheffield",
                ],
                "states": ["England", "Scotland", "Wales", "Northern Ireland"],
                "zip_format": lambda: f"{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.randint(0,9)} {random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)} {random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}",
            },
        }

        config = country_configs.get(country, country_configs["US"])

        for _ in range(n_samples):
            # Generate house number
            house_number = random.randint(1, 9999)

            # Generate street name
            street_name = random.choice(self.street_names)
            street_type = random.choice(self.street_types)

            # Generate city and state
            city = random.choice(config["cities"])
            state = random.choice(config["states"])

            # Generate zip/postal code
            zip_code = config["zip_format"]() if include_zip else ""

            # Format address based on preference
            if street_format == "number_name_type":
                address = f"{house_number} {street_name} {street_type}, {city}, {state}"
            else:  # name_type_number
                address = f"{street_name} {street_type} {house_number}, {city}, {state}"

            # Add zip code if requested
            if include_zip and zip_code:
                address += f" {zip_code}"

            addresses.append(address)

        return np.array(addresses)

    def generate_names(self, parameters: Dict[str, Any], n_samples: int) -> np.array:
        """Generate full names."""
        names = []

        # Check if categories are provided (for categorical distribution)
        if "categories" in parameters and parameters["categories"]:
            # Use provided categories
            categories = parameters["categories"]
            if isinstance(categories, str):
                categories = [
                    cat.strip() for cat in categories.split(",") if cat.strip()
                ]

            # Sample from provided categories
            return np.random.choice(categories, size=n_samples, replace=True)

        format_type = parameters.get("format", "first_last")
        gender_specific = parameters.get("gender_specific", True)
        include_titles = parameters.get("include_titles", False)

        # Define gender-specific name lists
        male_names = [
            "James",
            "John",
            "Robert",
            "Michael",
            "William",
            "David",
            "Richard",
            "Joseph",
            "Thomas",
            "Christopher",
        ]
        female_names = [
            "Mary",
            "Patricia",
            "Jennifer",
            "Linda",
            "Elizabeth",
            "Barbara",
            "Susan",
            "Jessica",
            "Sarah",
            "Karen",
        ]

        for _ in range(n_samples):
            if gender_specific:
                # Use gender-appropriate names
                if random.choice([True, False]):  # Randomly choose gender
                    first_name = random.choice(male_names)
                else:
                    first_name = random.choice(female_names)
            else:
                # Use any name regardless of gender
                first_name = random.choice(self.first_names)

            last_name = random.choice(self.last_names)

            if format_type == "first_last":
                name = f"{first_name} {last_name}"
            elif format_type == "last_first":
                name = f"{last_name}, {first_name}"
            elif format_type == "first_middle_last":
                middle_name = random.choice(self.first_names)
                name = f"{first_name} {middle_name} {last_name}"
            elif format_type == "first_last_initial":
                name = f"{first_name} {last_name[0]}."
            else:
                name = f"{first_name} {last_name}"

            # Add title if requested
            if include_titles:
                titles = ["Mr.", "Ms.", "Dr.", "Prof.", "Rev."]
                title = random.choice(titles)
                name = f"{title} {name}"

            names.append(name)

        return np.array(names)

    def generate_strings(self, parameters: Dict[str, Any], n_samples: int) -> np.array:
        """Generate random strings."""
        strings = []

        min_length = parameters.get("min_length", 5)
        max_length = parameters.get("max_length", 15)
        use_letters = parameters.get("use_letters", True)
        use_numbers = parameters.get("use_numbers", True)
        use_special = parameters.get("use_special", False)

        # Build character set
        chars = ""
        if use_letters:
            chars += string.ascii_letters
        if use_numbers:
            chars += string.digits
        if use_special:
            chars += string.punctuation

        if not chars:
            chars = string.ascii_letters

        for _ in range(n_samples):
            length = random.randint(min_length, max_length)
            string_value = "".join(random.choice(chars) for _ in range(length))
            strings.append(string_value)

        return np.array(strings)
