# Generated by Django 2.1.3 on 2019-04-27 18:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app2_notebooks', '0013_point_sub_point'),
    ]

    operations = [
        migrations.RenameField(
            model_name='point',
            old_name='sub_point',
            new_name='parent_point',
        ),
    ]
