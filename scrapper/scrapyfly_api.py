import datetime
import json
import re
from loguru import logger as log
from scrapfly import ScrapeApiResponse, ScrapeConfig, ScrapflyClient
from wellfound_scrapper.settings import SCRAPYFLY_KEY, SCRAPYFLY_TARGET



api_key = SCRAPYFLY_KEY
api_base = SCRAPYFLY_TARGET


def parse_job_compensation(data: str):
    if not data or type(data) is not str:
        raise Exception('The "data" parameter should be type of string with at least 1 char')
    only_numbers = re.findall(r'\d+\.*\d*', data)

    currency = data[0]
    res = {'currency': currency, 'salary': None, 'equity': None}
    if len(only_numbers) == 1:
        salary = float(only_numbers[0])
        res.update({'salary': (salary, salary)})

    if len(only_numbers) > 1: 
        salary_min = float(only_numbers[0])
        salary_max = float(only_numbers[1])
        res.update({'salary': (salary_min, salary_max)})

    if len(only_numbers) > 3:
        equity_min = float(only_numbers[2])
        equity_max = float(only_numbers[3])
        res.update({'equity': (equity_min, equity_max)})
    else:
        res.update({'equity': (0, 0)})

    return res

def extract_job_vacancies(data):

    startups = list()
    q = None
    for key in data:
        if key == 'ROOT_QUERY':
            for k in data[key]['talent']:
                if not q and 'seoLandingPageJobSearchResults' in k:
                    q = data[key]['talent'][k]

        if 'StartupResult' == data[key]['__typename']:
            if len(data[key]['highlightedJobListings']):
                data[key]['jobListings'] = list()
                for job in data[key]['highlightedJobListings']:
                    data[key]['jobListings'].append(data[job['__ref']])

                for job in range(len(data[key]['jobListings'])):
                    data[key]['jobListings'][job]['source_url'] = 'https://angel.co/company/{}/jobs/{}-{}'.format(
                        data[key]['slug'],
                        data[key]['jobListings'][job]['id'],
                        data[key]['jobListings'][job]['slug']
                    )
                    data[key]['jobListings'][job].update({'created_at': datetime.datetime.fromtimestamp(data[key]['jobListings'][job]['liveStartAt'])})

                    if data[key]['jobListings'][job]['compensation']:
                        compensation = parse_job_compensation(data[key]['jobListings'][job]['compensation'])
                        data[key]['jobListings'][job].update(compensation)
                    else:
                        data[key]['jobListings'][job].update({'currency': '$', 'salary': None, 'equity': None})
            
            startups.append(data[key])
    return {'data': startups, 'query': q}


def extract_apollo_state(result: ScrapeApiResponse):
    """extract apollo state graph from a page"""
    data = result.selector.css("script#__NEXT_DATA__::text").get()
    data = json.loads(data)
    graph = data["props"]["pageProps"]["apolloState"]["data"]
    return graph


def scrape_search(role: str = "", location: str = "", page: int = 0):
    """scrape angel.co search"""
    client = ScrapflyClient(api_key)
    # angel.co has 3 types of search urls: for roles, for locations and for combination of both
    if role and location and location == 'remote':
        url = f"https://angel.co/role/r/{role}"
    elif role and location and location != 'remote':
        url = f"https://angel.co/role/l/{role}/{location}"
    elif role:
        url = f"https://angel.co/role/{role}"
    elif location:
        url = f"https://angel.co/location/{location}"
    else:
        raise ValueError("need to pass either role or location argument to scrape search")
    
    if page:
        url = "{}?page={}".format(url, page)

    scrape = ScrapeConfig(
        url=url,  # url to scrape
        asp=True,  # this will enable anti-scraping protection bypass
    )
    result = client.scrape(scrape)
    if result.response.status_code != 200:
        err = result.response.json()
        log.error(err['result']['error']['message'])
        print(err['result']['error']['message'])
        return {'data': list()}
    graph = extract_apollo_state(result)
    data = extract_job_vacancies(graph)
    return data