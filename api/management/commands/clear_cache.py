from django.core.management.base import BaseCommand

from api.cache import invalidate_schedule_cache


class Command(BaseCommand):
    help = "Clears the schedule cache"

    def handle(self, *args, **kwargs):
        self.stdout.write("Clearing schedule cache...")
        invalidate_schedule_cache()
        self.stdout.write(self.style.SUCCESS("Successfully cleared schedule cache!"))
