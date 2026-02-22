from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.apps import apps
import json


class Command(BaseCommand):
    args = "<filename>"
    help = "Loads the initial data in to database"

    def handle(self, *args, **options):
        # Temporarily disconnect Haystack signals to avoid Elasticsearch dependency
        signal_processor = apps.get_app_config("haystack").signal_processor
        signal_processor.teardown()

        try:
            call_command("loaddata", "countries", verbosity=0)
            call_command("loaddata", "states", verbosity=0)
            call_command("loaddata", "cities", verbosity=0)
            call_command("loaddata", "skills", verbosity=0)
            call_command("loaddata", "industries", verbosity=0)
            call_command("loaddata", "qualification", verbosity=0)
            call_command("loaddata", "functionalarea", verbosity=0)
            call_command("loaddata", "languages", verbosity=0)
            self.stdout.write(self.style.SUCCESS("Successfully loaded initial data"))
        finally:
            signal_processor.setup()

        result = {"message": "Successfully loaded initial data"}
        return json.dumps(result)
