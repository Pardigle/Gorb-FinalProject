# Generated by Django 5.1.4 on 2025-04-27 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payslip',
            name='month_integer_reference',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
