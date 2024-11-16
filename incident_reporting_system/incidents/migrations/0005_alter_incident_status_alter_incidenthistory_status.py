# Generated by Django 5.1 on 2024-10-11 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0004_incidenthistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='status',
            field=models.CharField(choices=[('', 'Click to select Severity'), ('REPORTED', 'Reported'), ('IN_PROGRESS', 'In Progress'), ('IN_REVIEW', 'In Review'), ('ESCALATED', 'Escalated'), ('RESOLVED', 'Resolved')], default='REPORTED', max_length=20),
        ),
        migrations.AlterField(
            model_name='incidenthistory',
            name='status',
            field=models.CharField(choices=[('', 'Click to select Severity'), ('REPORTED', 'Reported'), ('IN_PROGRESS', 'In Progress'), ('IN_REVIEW', 'In Review'), ('ESCALATED', 'Escalated'), ('RESOLVED', 'Resolved')], max_length=20),
        ),
    ]