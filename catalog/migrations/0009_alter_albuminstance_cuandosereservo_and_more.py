# Generated by Django 5.1.5 on 2025-03-04 13:24

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_alter_albuminstance_cuandosereservo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='albuminstance',
            name='cuandoSeReservo',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='bookinstance',
            name='whenWasItBooked',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
