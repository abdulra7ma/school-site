# Generated by Django 4.1rc1 on 2022-07-30 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("school", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="teacher",
            name="is_stuff",
            field=models.BooleanField(
                default=False, verbose_name="Account Activation status"
            ),
        ),
    ]