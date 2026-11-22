import csv
from decimal import Decimal, InvalidOperation
from django.core.management.base import BaseCommand, CommandError
from products.models import Product

class Command(BaseCommand):
    help = "Import product records from a CSV file."

    def add_arguments(self, parser):
        parser.add_argument("csv_path", type=str)
        parser.add_argument("--replace", action="store_true",
                            help="Delete existing products before importing.")

    def handle(self, *args, **options):
        path = options["csv_path"]
        if options["replace"]:
            Product.objects.all().delete()
        created = 0
        try:
            with open(path, newline="", encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)
                required = {"name", "category", "price", "rating", "review_count", "product_url"}
                if not reader.fieldnames or not required.issubset(set(reader.fieldnames)):
                    raise CommandError("CSV must contain: " + ", ".join(sorted(required)))
                for row in reader:
                    rating_text = (row.get("rating") or "").strip()
                    Product.objects.create(
                        name=row["name"].strip(),
                        category=row["category"].strip(),
                        price=Decimal(row["price"]),
                        rating=Decimal(rating_text) if rating_text else None,
                        review_count=int(row["review_count"] or 0),
                        product_url=(row.get("product_url") or "").strip(),
                        source=(row.get("source") or "CSV import").strip(),
                    )
                    created += 1
        except (OSError, ValueError, InvalidOperation) as exc:
            raise CommandError(f"Could not import CSV: {exc}")
        self.stdout.write(self.style.SUCCESS(f"Imported {created} products."))