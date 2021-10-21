from django.core.management.base import BaseCommand

from isomanager.models import Datastore


class Command(BaseCommand):
    def handle(self, *args, **options):
        obj = Datastore.objects.all()
        for o in obj:
            self.stdout.write(self.style.SUCCESS("Scanning {0}".format(o.location)))
            o.scan()
