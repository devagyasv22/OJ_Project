# Generated by Django 4.2.23 on 2025-07-19 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CodeSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(choices=[('cpp', 'C++'), ('py', 'Python')], max_length=10)),
                ('code', models.TextField()),
                ('input_data', models.TextField(blank=True, null=True)),
                ('output_data', models.TextField(blank=True, null=True)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
