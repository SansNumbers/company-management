# Generated by Django 4.1.5 on 2023-01-27 10:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('office', '0002_office_vehicle_count'),
        ('company', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vehicle', '0002_alter_vehicle_office'),
    ]

    operations = [
        migrations.CreateModel(
            name='Audit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='audits', to='company.company')),
                ('drivers', models.ManyToManyField(blank=True, related_query_name='drivers', to=settings.AUTH_USER_MODEL)),
                ('office', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='office', to='office.office')),
                ('vehicle', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='audit', to='vehicle.vehicle')),
            ],
        ),
    ]
