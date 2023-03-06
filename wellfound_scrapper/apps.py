from django.utils.translation import gettext_lazy as _
from django.contrib.admin.apps import AdminConfig

class WellfoundScrapperAdminConfig(AdminConfig):
    default_site = 'wellfound_scrapper.admin.WellfoundScrapperAdminSite'