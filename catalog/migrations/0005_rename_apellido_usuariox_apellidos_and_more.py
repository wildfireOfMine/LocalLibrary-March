# Generated by Django 5.0.10 on 2025-02-06 18:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_usuariox_municipio'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usuariox',
            old_name='apellido',
            new_name='apellidos',
        ),
        migrations.RenameField(
            model_name='usuariox',
            old_name='primerNombre',
            new_name='nombres',
        ),
    ]
