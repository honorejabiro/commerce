from django.core.management.base import BaseCommand
from auctions.models import Listing

class Command(BaseCommand):
    help = 'Deletes all listings from the Listing table'

    def handle(self, *args, **kwargs):
        Listing.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all listings'))