# Generated by Django 2.1.3 on 2018-12-02 15:04

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app1_accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordering_number', models.IntegerField(blank=True, null=True, verbose_name='_ordering_number')),
                ('title', models.CharField(blank=True, max_length=100, null=True, verbose_name='Title')),
                ('note', models.BooleanField(default=True, verbose_name='Is note')),
                ('list', models.BooleanField(default=False, verbose_name='Is list')),
                ('ck_text', ckeditor.fields.RichTextField(blank=True, max_length=10000, null=True, verbose_name='CK Text')),
                ('text', models.TextField(blank=True, max_length=10000, null=True, verbose_name='Записка')),
                ('hidden_note', models.TextField(blank=True, max_length=3000, null=True, verbose_name='Hidden note')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Note',
                'verbose_name_plural': '1.1.1 Note',
                'db_table': 'note',
            },
        ),
        migrations.CreateModel(
            name='Notebook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordering_number', models.IntegerField(blank=True, default=0, null=True, verbose_name='_ordering_number')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('hidden_note', models.TextField(blank=True, max_length=1000, null=True, verbose_name='Hidden note')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('library', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app1_accounts.Library')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Notebook',
                'verbose_name_plural': '1 Notebook',
                'db_table': 'notebook',
            },
        ),
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordering_number', models.IntegerField(blank=True, null=True, verbose_name='_ordering_number')),
                ('title', models.CharField(blank=True, max_length=100, null=True, verbose_name='Title')),
                ('note', models.TextField(blank=True, max_length=3000, null=True, verbose_name='Hidden note')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('notebook', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app2_notebooks.Notebook')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Paper',
                'verbose_name_plural': '1.1 Paper',
                'db_table': 'paper',
            },
        ),
        migrations.AddField(
            model_name='note',
            name='paper',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='paper', to='app2_notebooks.Paper'),
        ),
        migrations.AddField(
            model_name='note',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
