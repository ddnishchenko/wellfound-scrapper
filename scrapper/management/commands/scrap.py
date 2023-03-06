from django.utils.translation import gettext_lazy as _
from django.core.management import BaseCommand, CommandError
from scrapper.scrapyfly_api import scrape_search
from scrapper.management.commands._record_compamies import record_companies


class Command(BaseCommand):
    """
    Description
    """
    help = _("scrape <role> <location> --page=<number> --page int")

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "role",
            help=_('Name of the role, for example: python-developer, software-developer'),
            nargs="+",
            type=str
        )

        parser.add_argument(
            "location",
            help=_("Location name city or country, for example: san-francisco, new-york, chicago. Special is remote"),
            nargs="+",
            type=str
        )

        parser.add_argument(
            "--page",
            help=_("page number in the search query"),
            nargs="+",
            type=int
        )

    def handle(self, *args, **options):
        role = options.get('role')[0]
        location = options.get('location')[0]
        try:
            self.stdout.write(self.style.HTTP_INFO("Start scrapping with query role: {}, location:{}".format(role, location)))
            result = scrape_search(role=role, location=location)
            page_count = int(result['query']['pageCount'])
            self.stdout.write(self.style.HTTP_INFO("Initial page scrapped"))

            self.stdout.write(self.style.HTTP_INFO("It will be scrapped pages {} in total by this query".format(page_count)))
            for page in range(1, page_count+1):
                if page == 1:
                    self.stdout.write(self.style.HTTP_INFO("Start saving scrapped data from page number {}".format(page)))
                    record_companies(result['data'])
                    self.stdout.write(self.style.HTTP_INFO("Scrapped data from page number {} is saved".format(page)))
                else:
                    self.stdout.write(self.style.HTTP_INFO("Start scrapping with query role: {}, location: {}, page: {}".format(role, location, page)))
                    next_page = scrape_search(role=role, location=location, page=page)
                    self.stdout.write(self.style.HTTP_INFO("Start saving scrapped data from page number {}".format(page)))
                    record_companies(next_page['data'])
                    self.stdout.write(self.style.HTTP_INFO("Scrapped data from page number {} is saved".format(page)))
        except Exception as e:
            raise CommandError(e)
        
        self.stdout.write(self.style.SUCCESS("Everything is scrapped and stored in database"))
