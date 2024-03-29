# Generated by Django 5.0.2 on 2024-03-01 12:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(max_length=64)),
                ('category', models.CharField(choices=[('pol', 'Politics'), ('art', 'Art'), ('tech', 'Technology'), ('trivia', 'Trivia')], max_length=32)),
                ('region', models.CharField(choices=[('uk', 'UK'), ('eu', 'European'), ('w', 'World')], max_length=32)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('details', models.CharField(max_length=128)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.author')),
            ],
        ),
    ]
