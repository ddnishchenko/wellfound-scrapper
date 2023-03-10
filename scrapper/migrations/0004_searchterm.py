# Generated by Django 4.1 on 2023-03-07 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapper', '0003_jobvacancy_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchTerm',
            fields=[
                ('slug', models.SlugField(help_text='Slug of the search term', max_length=255, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Search term', max_length=255)),
            ],
        ),
    ]
