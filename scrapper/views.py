from django.http import JsonResponse
from scrapper.scrapyfly_api import scrape_search
from scrapper.management.commands._record_compamies import record_companies

def index(request):
    result = scrape_search(role='python-developer', location='remote', page=4)
    companies = result['data']
    record_companies(companies)
    return JsonResponse(result)