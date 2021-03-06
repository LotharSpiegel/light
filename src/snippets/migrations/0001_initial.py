# Generated by Django 2.2.3 on 2019-07-23 00:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('language_code', models.CharField(max_length=50)),
                ('mime_type', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Snippet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('description_html', models.TextField(editable=False)),
                ('code', models.TextField()),
                ('highlighted_code', models.TextField(editable=False)),
                ('pub_date', models.DateTimeField(editable=False)),
                ('updated_date', models.DateTimeField(editable=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='snippets', to=settings.AUTH_USER_MODEL)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='snippets', to='snippets.Language')),
            ],
            options={
                'ordering': ['-pub_date'],
            },
        ),
    ]
