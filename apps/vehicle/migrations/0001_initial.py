# Generated by Django 4.1.1 on 2022-12-12 14:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company', '0001_initial'),
        ('office', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('licence_plate', models.CharField(max_length=64)),
                ('model', models.CharField(max_length=64)),
                ('year_of_manufacture', models.PositiveIntegerField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicles', to='company.company')),
                ('drivers', models.ManyToManyField(related_query_name='vehicles', to=settings.AUTH_USER_MODEL)),
                ('office', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicles', to='office.office')),
            ],
        ),
    ]