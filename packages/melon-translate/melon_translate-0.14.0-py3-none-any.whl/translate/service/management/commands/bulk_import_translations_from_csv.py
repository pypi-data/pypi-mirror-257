import csv
from pathlib import Path

from django.core.management.base import BaseCommand

from translate.core.utils.logger import log
from translate.service.models import Language, Translation, TranslationKey


class Command(BaseCommand):
    """
    Creates or updates translation keys in database from CSV file.
    Languages need to be created before usage of the command.
    Following format of CSV file is accepted:
    key,views, context, translation_de, translation_plural_de, translation_en, translation_plural_en...
    """

    def add_arguments(self, parser):
        """Attach argument for import_translations command."""

        parser.add_argument(
            "file_name",
            type=str,
            nargs=1,
        )

    @staticmethod
    def get_lang_dict():
        lang_dict = {}
        for lang in Language.objects.all():
            lang_dict[lang.lang_info] = lang
        return lang_dict

    def import_csv(self, file_name):
        """Import translations from CSV file to database."""

        file_name = Path(file_name)
        language_dict = self.get_lang_dict()
        if not language_dict:
            log.warning("No languages found in database. Please create languages first.")
            return
        log.info(f"Importing translations from {file_name.absolute()}")

        with file_name.open() as csvfile:
            reader_dict = csv.DictReader(csvfile)

            for record in reader_dict:
                snake_key = record.get("key")
                views = record.get("views").replace(" ", "").split(",")
                context = record.get("context")
                translation_key, _ = TranslationKey.objects.get_or_create(
                    snake_name=snake_key, defaults={"views": views, "usage_context": context}
                )

                for lang_code, lang in language_dict.items():
                    translation = record.get(f"translation_{lang_code}")
                    translation_plural = record.get(f"translation_plural_{lang_code}")

                    if not translation:
                        continue

                    translation_obj, created = Translation.objects.update_or_create(
                        language=lang,
                        key=translation_key,
                        defaults={"translation": translation, "translation_plural": translation_plural},
                    )
                    if created:
                        log.info(f"Creating record {snake_key} for {lang.lang_info} language")
                    else:
                        log.info(f"Updating record {snake_key} for {lang.lang_info} language")

    def handle(self, *args, **options):
        """Handle command."""
        file_name = options.get("file_name")[0]

        self.import_csv(file_name)

        log.info("Done!")
