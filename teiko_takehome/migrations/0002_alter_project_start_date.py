# Generated by Django 4.2.7 on 2023-11-06 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teiko_takehome', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='start_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
