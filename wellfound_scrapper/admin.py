from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy
from django.contrib import admin

comany_name = 'Wellfound'
class WellfoundScrapperAdminSite(admin.AdminSite):
    site_title = gettext_lazy("Wellfound scrapper site admin")
    site_header = gettext_lazy("Wellfound administration")
    index_title = gettext_lazy("Wellfound administration")