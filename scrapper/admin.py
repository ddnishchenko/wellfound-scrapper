from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from scrapper import models
# Register your models here.

@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'company_size')
    list_display_links = ('name',)
    list_filter = ('company_size',)
    search_fields = ('name', 'high_concept')
    search_help_text = _('Searching by name and short description')

@admin.register(models.JobVacancy)
class JobVacancyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'company_name', 'company_size', 'job_type', 'remote', 'location_names', 'currency', 'salary', 'equity', 'created_at')
    list_display_links = ('title',)
    list_filter = ('job_type', 'remote', 'currency', 'company__name', 'company__company_size')
    search_fields = ('title', 'description')
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

