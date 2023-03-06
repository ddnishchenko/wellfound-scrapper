# Generated by Django 4.1 on 2023-03-03 17:39

import django.contrib.postgres.fields.ranges
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapper', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='high_concept',
            field=models.TextField(blank=True, help_text='Short description'),
        ),
        migrations.AlterField(
            model_name='company',
            name='id',
            field=models.CharField(max_length=55, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='jobvacancy',
            name='equity',
            field=django.contrib.postgres.fields.ranges.DecimalRangeField(blank=True, help_text='Equity', null=True),
        ),
        migrations.AlterField(
            model_name='jobvacancy',
            name='id',
            field=models.CharField(max_length=55, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='jobvacancy',
            name='salary',
            field=django.contrib.postgres.fields.ranges.DecimalRangeField(blank=True, help_text='Salary', null=True),
        ),
    ]
