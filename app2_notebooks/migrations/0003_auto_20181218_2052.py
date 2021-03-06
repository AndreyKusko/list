# Generated by Django 2.1.3 on 2018-12-18 20:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app2_notebooks', '0002_auto_20181202_1550'),
    ]

    operations = [
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordering_number', models.IntegerField(blank=True, null=True, verbose_name='Номер')),
                ('title', models.CharField(blank=True, max_length=120, null=True, verbose_name='Название')),
                ('text', models.TextField(blank=True, default=False, max_length=3000, null=True, verbose_name='Текст')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('hidden_note', models.TextField(blank=True, max_length=3000, null=True, verbose_name='Скрытая заметка')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'point',
                'ordering': ['-active', '-title', 'note', 'ordering_number'],
            },
        ),
        migrations.RemoveField(
            model_name='paper',
            name='notebook',
        ),
        migrations.RemoveField(
            model_name='paper',
            name='user',
        ),
        migrations.RemoveField(
            model_name='note',
            name='text',
        ),
        migrations.AlterField(
            model_name='note',
            name='paper',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='note', to='app2_notebooks.Notebook'),
        ),
        migrations.AlterField(
            model_name='notebook',
            name='library',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app1_accounts.Library'),
        ),
        migrations.DeleteModel(
            name='Paper',
        ),
        migrations.AddField(
            model_name='point',
            name='note',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app2_notebooks.Note'),
        ),
        migrations.AddField(
            model_name='point',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
