# Generated by Django 3.1.2 on 2020-10-14 18:41

import contributions.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import functools
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contribution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, unique=True, verbose_name='NTNU-brukernavn')),
                ('confirmed', models.BooleanField(default=False)),
                ('confirmation_token', models.CharField(default=functools.partial(contributions.utils.get_random_token, *(10,), **{}), max_length=20, unique=True)),
                ('name', models.CharField(max_length=50, verbose_name='Innslagets navn')),
                ('video_link', models.URLField(help_text='Lenke til Vimeo eller YouTube video.')),
                ('approved', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Bidrag',
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, unique=True, verbose_name='NTNU-brukernavn')),
                ('confirmed', models.BooleanField(default=False)),
                ('confirmation_token', models.CharField(default=functools.partial(contributions.utils.get_random_token, *(10,), **{}), max_length=20, unique=True)),
                ('contribution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contributions.contribution')),
            ],
            options={
                'verbose_name': 'Stemme',
            },
        ),
        migrations.CreateModel(
            name='HistoricalVote',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('username', models.CharField(db_index=True, max_length=20, verbose_name='NTNU-brukernavn')),
                ('confirmed', models.BooleanField(default=False)),
                ('confirmation_token', models.CharField(db_index=True, default=functools.partial(contributions.utils.get_random_token, *(10,), **{}), max_length=20)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('contribution', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='contributions.contribution')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Stemme',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalContribution',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('username', models.CharField(db_index=True, max_length=20, verbose_name='NTNU-brukernavn')),
                ('confirmed', models.BooleanField(default=False)),
                ('confirmation_token', models.CharField(db_index=True, default=functools.partial(contributions.utils.get_random_token, *(10,), **{}), max_length=20)),
                ('name', models.CharField(max_length=50, verbose_name='Innslagets navn')),
                ('video_link', models.URLField(help_text='Lenke til Vimeo eller YouTube video.')),
                ('approved', models.BooleanField(default=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Bidrag',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
