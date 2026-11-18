import json
import re
from decimal import Decimal, InvalidOperation
from pathlib import Path
from urllib.parse import urlparse

import requests
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError

from api.models import Brand, Category, Product, ProductImage, Species


def get_repr_field(value, name):
    if not isinstance(value, str):
        return None
    match = re.search(rf"\b{name}=([\"'])(.*?)\1", value)
    return match.group(2) if match else None


def get_named_record(model, name, max_length=50):
    name = str(name or "").strip()[:max_length]
    if not name:
        return None
    record = model.objects.filter(name__iexact=name).first()
    return record or model.objects.create(name=name)


def get_category_name(category):
    if isinstance(category, dict):
        return category.get("title") or category.get("name")
    return get_repr_field(category, "title")


def get_brands(raw_brands):
    brands = []
    for raw_brand in raw_brands or []:
        name = raw_brand.get("name") if isinstance(raw_brand, dict) else get_repr_field(raw_brand, "name")
        brand = get_named_record(Brand, name)
        if brand:
            brands.append(brand)
    return brands


def get_species(product, category_name):
    text = " ".join(
        str(part or "")
        for part in (
            product.get("title"),
            product.get("description"),
            category_name,
            json.dumps(product.get("structured_attributes") or {}, ensure_ascii=False),
        )
    ).lower()

    matches = (
        ("Cat", r"\bcat(s)?\b|feline"),
        ("Dog", r"\bdog(s)?\b|canine|puppy|puppies"),
        ("Bird", r"\bbird(s)?\b|parrot"),
        ("Fish", r"\bfish\b|aquarium"),
        ("Reptile", r"\breptile(s)?\b|amphibian"),
        ("Small animal", r"rabbit|hamster|guinea pig|small animal"),
    )
    for species_name, pattern in matches:
        if re.search(pattern, text):
            return get_named_record(Species, species_name)
    return None


def normalize_offer(raw_offer):
    if isinstance(raw_offer, dict):
        price_data = raw_offer.get("price") or {}
        amount = price_data.get("price", price_data.get("amount")) if isinstance(price_data, dict) else price_data
        compare_at = price_data.get("compare_at_price") if isinstance(price_data, dict) else None
        currency = price_data.get("currency", "USD") if isinstance(price_data, dict) else "USD"
        availability = raw_offer.get("availability")
        condition = raw_offer.get("condition")
    else:
        price_match = re.search(
            r"price=Price\(price=([^,]+), compare_at_price=([^,]+), currency=([^)]*)\)",
            str(raw_offer),
        )
        if not price_match:
            return None
        amount, compare_at, currency = price_match.groups()
        availability = get_repr_field(raw_offer, "availability")
        condition = get_repr_field(raw_offer, "condition")

    try:
        amount = Decimal(str(amount))
        compare_at = Decimal(str(compare_at)) if compare_at not in (None, "None", "") else None
    except (InvalidOperation, TypeError):
        return None

    if amount <= 0:
        return None

    return {
        "amount": amount,
        "compare_at": compare_at,
        "currency": str(currency or "USD").upper()[:3],
        "availability": availability,
        "condition": condition,
    }


def choose_offer(raw_offers):
    offers = [offer for item in raw_offers or [] if (offer := normalize_offer(item))]
    if not offers:
        return None

    in_stock_new = [
        offer for offer in offers
        if offer["availability"] == "InStock" and offer["condition"] in (None, "new")
    ]
    in_stock = [offer for offer in offers if offer["availability"] == "InStock"]
    candidates = in_stock_new or in_stock or offers
    return min(candidates, key=lambda offer: offer["amount"])


def get_main_image(raw_images):
    images = []
    for raw_image in raw_images or []:
        if isinstance(raw_image, dict):
            image = raw_image
        elif isinstance(raw_image, str):
            image = {
                "url": get_repr_field(raw_image, "url"),
                "cleaned_url": get_repr_field(raw_image, "cleaned_url"),
                "is_main_image": "is_main_image=True" in raw_image,
                "alt_text": get_repr_field(raw_image, "alt_text"),
            }
        else:
            continue
        url = image.get("cleaned_url") or image.get("url")
        if url:
            images.append((not image.get("is_main_image", False), url, image.get("alt_text") or ""))
    return min(images, default=None, key=lambda item: item[0])


class Command(BaseCommand):
    help = "Seed the local catalog from parser/products_buffer.json"

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=None)
        parser.add_argument("--skip-images", action="store_true")

    def handle(self, *args, **options):
        data_path = Path(settings.BASE_DIR) / "parser" / "products_buffer.json"
        if not data_path.exists():
            raise CommandError(f"Product data file was not found: {data_path}")

        try:
            products_data = json.loads(data_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise CommandError(f"Could not read product data: {error}") from error

        if not isinstance(products_data, list):
            raise CommandError("Expected products_buffer.json to contain a JSON array")

        if options["limit"] is not None:
            products_data = products_data[: max(options["limit"], 0)]

        created = updated = skipped = images_added = 0
        for raw_product in products_data:
            if not isinstance(raw_product, dict):
                skipped += 1
                continue

            channel3_id = str(raw_product.get("id") or "").strip()
            title = str(raw_product.get("title") or "").strip()[:70]
            offer = choose_offer(raw_product.get("offers"))
            if not channel3_id or not title or not offer:
                skipped += 1
                continue

            category = get_named_record(Category, get_category_name(raw_product.get("category")))
            brand = next(iter(get_brands(raw_product.get("brands"))), None)
            species = get_species(raw_product, category.name if category else "")
            compare_at = offer["compare_at"]
            product_values = {
                "title": title,
                "description": str(raw_product.get("description") or ""),
                "price": compare_at if compare_at and compare_at > offer["amount"] else offer["amount"],
                "discount": compare_at - offer["amount"] if compare_at and compare_at > offer["amount"] else Decimal("0"),
                "currency": offer["currency"],
                "is_available": offer["availability"] == "InStock",
                "species": species,
                "category": category,
                "brand": brand,
            }
            product, was_created = Product.objects.update_or_create(
                channel3_id=channel3_id,
                defaults=product_values,
            )
            created += int(was_created)
            updated += int(not was_created)

            if not options["skip_images"] and not product.images.exists():
                main_image = get_main_image(raw_product.get("images"))
                if main_image:
                    _, image_url, alt_text = main_image
                    try:
                        response = requests.get(image_url, timeout=20)
                        response.raise_for_status()
                        content_type = response.headers.get("Content-Type", "image/jpeg").split(";")[0]
                        extension = {
                            "image/jpeg": ".jpg",
                            "image/png": ".png",
                            "image/webp": ".webp",
                        }.get(content_type, Path(urlparse(image_url).path).suffix or ".jpg")
                        image = ProductImage(product=product, alt=alt_text[:255], is_main=True)
                        image.image.save(
                            f"channel3_{channel3_id}{extension}",
                            ContentFile(response.content),
                            save=True,
                        )
                        images_added += 1
                    except (requests.RequestException, OSError, ValueError) as error:
                        self.stderr.write(f"Could not import image for {channel3_id}: {error}")

        self.stdout.write(
            self.style.SUCCESS(
                f"Channel3 seed finished: {created} created, {updated} updated, "
                f"{skipped} skipped, {images_added} main images added."
            )
        )
