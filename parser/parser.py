import json
from pathlib import Path

import environ
from channel3_sdk import Channel3

BASE_DIR = Path(__file__).resolve().parent

env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")

client = Channel3(api_key=f"{env("SECRET_KEY")}")

SEARCH_QUERIES = [
    # Food
    "Royal Canin cat food",
    "Royal Canin dog food",
    "Purina cat food",
    "Purina dog food",
    "Whiskas cat food",
    "Pedigree dog food",
    "Acana cat food",
    "Acana dog food",

    # Toys
    "Trixie cat toys",
    "Trixie dog toys",
    "Pet toys for cats and dogs",

    # Accessories
    "Trixie pet accessories",
    "Pet bowls collars leashes carriers",

    # Health & Wellness
    "Pet health and wellness products",
    "Pet vitamins and supplements",

    # Grooming
    "Pet grooming products shampoos brushes",

    # Beds & Furniture
    "Cat beds scratching posts",
    "Dog beds and furniture",

    # Other species
    "Bird food toys and accessories",
    "Fish food aquarium accessories",
    "Rabbit hamster guinea pig food and accessories",
    "Reptile food and accessories",
]

all_products = {}

for query in SEARCH_QUERIES:
    print(f"Searching: {query}")

    response = client.products.search(
        query=query,
        limit=5,
    )

    for product in response.items:
        all_products[product.id] = product

print(f"Found {len(all_products)} unique products")


with open("products_buffer.json", "w", encoding="utf-8") as file:
    json.dump(
        [product.__dict__ for product in all_products.values()],
        file,
        ensure_ascii=False,
        indent=4,
        default=str,
    )

