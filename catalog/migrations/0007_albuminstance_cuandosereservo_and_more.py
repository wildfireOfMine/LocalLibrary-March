# Generated by Django 5.1.5 on 2025-02-19 11:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_alter_bookinstance_borrower_alter_usuariox_usuario_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='albuminstance',
            name='cuandoSeReservo',
            field=models.DateField(null=True, verbose_name=datetime.datetime(2025, 2, 19, 11, 14, 18, 692317, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AddField(
            model_name='bookinstance',
            name='whenWasItBooked',
            field=models.DateField(null=True, verbose_name=datetime.datetime(2025, 2, 19, 11, 14, 18, 686566, tzinfo=datetime.timezone.utc)),
        ),
    ]
