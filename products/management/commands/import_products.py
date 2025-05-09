import os
import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.conf import settings
from products.models import Product

# products/management/commands/import_products.py
class Command(BaseCommand):
    help = 'Import laptops data from eBay'

    def handle(self, *args, **options):
        # Construct the CSV file path
        path = os.path.join(
            settings.BASE_DIR,
            'data',
            'EbayPcLaptopsAndNetbooksClean.csv'
        )

        # Read Error Catcher
        try:
            # Read up to 5,000 rows, dropping any rows missing Brand or Price
            df = (pd.read_csv(path)
                    .dropna(subset=['Brand', 'Price'])
                    .head(5000))
        except FileNotFoundError:
            raise CommandError(f'CSV file not found: {path}')
        except Exception as e:
            raise CommandError(f'Error reading CSV: {e}')

        # Collect Product instances for bulk insertion
        products_to_create = []
        for row in df.itertuples():
            # Construct product name from Brand and Type
            name = f"{row.Brand} {row.Type}"[:200]
            # Use Features as description if available, otherwise use Condition
            description = row.Features if pd.notna(row.Features) else row.Condition

            products_to_create.append(
                Product(
                    name        = name,
                    description = description,
                    price       = row.Price,
                    stock       = 50
                )
            )

        # Bulk insert all products in a single transaction
        with transaction.atomic():
            Product.objects.bulk_create(products_to_create, ignore_conflicts=True)

        # Print completion message
        self.stdout.write(
            self.style.SUCCESS(f'Imported {len(products_to_create)} laptops into stock')
        )
