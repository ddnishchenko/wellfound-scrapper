from django.core.management import call_command
from django_cron import CronJobBase, Schedule
from scrapper.management.commands import scrap

class ScrapperCronJob(CronJobBase):
    RUN_EVERY_DAYS = [0] # Run every Monday
    RUN_AT_TIMES = ['12:00']
    code = 'scrapper.ScrapperCronJob'
    schedule = Schedule(run_on_days=RUN_EVERY_DAYS)
    def do(self):
        call_command(scrap.BaseCommand())
