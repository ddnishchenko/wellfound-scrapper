from scrapper.models import Company, JobVacancy

def record_companies(companies):
    for c in companies:
        company, created_company = Company.objects.update_or_create(
            id=c['id'],
            name=c['name'],
            slug=c['slug'],
            company_size=c['companySize'],
            high_concept=c['highConcept'],
            logo_url=c['logoUrl'],
            defaults={
                'id': c['id'],
                'name': c['name'],
                'slug': c['slug'],
                'company_size': c['companySize'],
                'high_concept': c['highConcept'],
                'logo_url' :c['logoUrl'],
            }
        )

        for j in c['jobListings']:
            job, created_job = JobVacancy.objects.update_or_create(
                id=j['id'],
                created_at=j['created_at'],
                title=j['title'],
                slug=j['slug'],
                source_url=j['source_url'],
                description=j['description'],
                job_type=j['jobType'],
                remote=j['remote'],
                location_names=j['locationNames'],
                currency=j['currency'],
                salary=j['salary'],
                equity=j['equity'],
                company=company,
                defaults={
                    'id': j['id'],
                    'created_at': j['created_at'],
                    'title': j['title'],
                    'slug': j['slug'],
                    'source_url': j['source_url'],
                    'description': j['description'],
                    'job_type': j['jobType'],
                    'remote': j['remote'],
                    'location_names': j['locationNames'],
                    'currency': j['currency'],
                    'salary': j['salary'],
                    'equity': j['equity'],
                    'company': company,
                }
            )