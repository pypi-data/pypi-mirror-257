from django.core import management


class Command(management.BaseCommand):
    def handle(self, *args, **options):
        management.call_command(
            "bulk_import_translations_from_csv", "translate/service/import_spreadsheets/translations.csv"
        )
