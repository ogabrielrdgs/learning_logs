# Generated by Django 4.2.4 on 2023-11-20 11:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learning_logs', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entry',
            options={'ordering': ('-date_added',), 'verbose_name': 'entry', 'verbose_name_plural': 'entries'},
        ),
        migrations.AlterModelOptions(
            name='topic',
            options={'ordering': ('-date_added',), 'verbose_name': 'topic', 'verbose_name_plural': 'topics'},
        ),
    ]
