import datetime
from django.db import models
from django.contrib.postgres.fields import ArrayField, DecimalRangeField
from django.utils.translation import gettext_lazy as _

class JobVacancy(models.Model):
    
    class JobTypes(models.TextChoices):
        FULL_TIME = 'full-time', _('Full time')
        PART_TIME = 'contract', _('Contract')
        INTERNSHIP = 'internship', _('Internship'),
        COFOUNDER = 'cofounder', _('Cofounder')

    company = models.ForeignKey(
        'Company',
        on_delete=models.CASCADE,
        help_text="Company"
    )
    id = models.CharField(primary_key=True, max_length=55)
    created_at = models.DateField(
        default=datetime.date.today,
        help_text=_('Posted at')
    )
    title = models.CharField(
        max_length=255,
        help_text=_('Title of the job vacancy/role')
    )
    slug = models.SlugField(
        max_length=255,
        help_text=_('slug of the job')
    )
    source_url = models.URLField(
        blank=True,
        help_text=_('Link to the job vacancy')
    )
    description = models.TextField(
        blank=True,
        help_text=_('Description'),
    )
    job_type = models.CharField(
        blank=True,
        max_length=255,
        choices=JobTypes.choices,
        help_text=_('Contract type: Part time or Full time')
    )
    remote = models.BooleanField(
        help_text=_('Is it allowed to work remotely')
    )
    location_names = ArrayField(
        models.CharField(max_length=255),
        blank=True,
        help_text=_('Locations of the job')
    )
    currency = models.CharField(
        max_length=3,
        blank=True,
        default='$',
        help_text=_('The currency of the salary')
    )
    salary = DecimalRangeField(
        blank=True,
        null=True,
        help_text=_('Salary')
    )
    equity = DecimalRangeField(
        blank=True,
        null=True,
        help_text=_('Equity'),
    )


class Company(models.Model):

    class CompanySizes(models.TextChoices):
        SIZE_1_10 = 'SIZE_1_10', _('1-10 employees')
        SIZE_11_50 = 'SIZE_11_50', _('11-50 employees')
        SIZE_51_200 = 'SIZE_51_200', _('51-200 employees')
        SIZE_201_500 = 'SIZE_201_500', _('201-500 employees')
        SIZE_501_1000 = 'SIZE_501_1000', _('501-1000 employees')
        SIZE_1001_5000 = 'SIZE_1001_5000', _('1001-5000 employees')
        SIZE_5000_PLUS = 'SIZE_5000_PLUS', _('5000+ employees')

    id = models.CharField(primary_key=True, max_length=55)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    company_size = models.CharField(
        max_length=255,
        choices=CompanySizes.choices,
        blank=True
    )
    high_concept = models.TextField(
        blank=True,
        help_text=_('Short description')
    )
    logo_url = models.URLField(blank=True)

