from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib import admin, messages
from django.core.management import call_command
from django.shortcuts import redirect
from django.forms import Media
import logging

logger = logging.getLogger(__name__)

from scrapper import models
from scrapper.management.commands import scrap


@admin.register(models.JobVacancy)
class JobVacancyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'company_name', 'company_size', 'job_type', 'remote', 'location_names', 'currency', 'salary', 'equity', 'created_at')
    list_display_links = ('title',)
    list_filter = ('job_type', 'remote', 'currency', 'company__name', 'company__company_size')
    search_fields = ('id', 'title', 'description')
    search_help_text = _('Searching by title and description')
    save_on_top = True

    @admin.display(description=_('Company'))
    def company_name(self, obj):
        return obj.company.name
    
    @admin.display(description=_('Company size'))
    def company_size(self, obj):
        for choice in obj.company.CompanySizes.choices:
            value, label = choice
            if value == obj.company.company_size:
                return label
        return 'Unknown'

@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'company_size')
    list_display_links = ('name',)
    list_filter = ('company_size',)
    search_fields = ('id', 'name', 'high_concept')
    search_help_text = _('Searching by name and short description')


@admin.action()
def scrap_vacancies(modeladmin, request, queryset):
    slugs = list()
    if not request.user.scrapfly_key:
        message = _('The "scrapfly key" is missing. Add scrapfly key in your user profile')
        modeladmin.message_user(request, message, level=messages.ERROR)
    else:
        try:
            for query in queryset:
                call_command(scrap.Command(), query.slug, 'remote', api_key=request.user.scrapfly_key)
                slugs.append(query.slug)
                query.scrapped_at = timezone.now()
                query.save()
            message = _('Vacancies has been successfuly scrapped')
            modeladmin.message_user(request, message, level=messages.SUCCESS)
        except Exception as e:
            logger.error(e)
            
            message = 'Error during scrapping.\n'
            if len(slugs):
                slug_joined = ', '.join(slugs)
                message = message + f"{slug_joined} has been successfully scrapped."
            modeladmin.message_user(request, message, level=messages.ERROR)
    
    

@admin.register(models.SearchTerm)
class SearchTermAdmin(admin.ModelAdmin):
    actions = [scrap_vacancies]
    list_display = ('name', 'slug', 'scrapped_at')
    list_display_links = ('name',)
    list_filter = ('name',)
    search_fields = ('name', 'slug')
    search_help_text = _('Searching by name and slug')
    class Media:
        css = {
            'all': ('css/style.css',)
        }
        js = ('js/script.js',)