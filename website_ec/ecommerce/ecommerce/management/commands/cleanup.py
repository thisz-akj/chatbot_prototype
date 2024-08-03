# your_app/management/commands/cleanup_unknown_products.py
from django.core.management.base import BaseCommand
from ecommerce.store.models import Product

class Command(BaseCommand):
    help = 'Delete products with unknown names'

    def handle(self, *args, **kwargs):
        deleted_count, _ = Product.objects.filter(name='Unknown').delete()
        self.stdout.write(f"Deleted {deleted_count} products with name 'Unknown'.")
