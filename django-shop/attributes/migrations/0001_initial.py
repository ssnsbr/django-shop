# Generated by Django 5.0.7 on 2024-11-03 12:51

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AttributeOption',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('value', models.CharField(max_length=255)),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='attributes.attribute')),
            ],
            options={
                'unique_together': {('attribute', 'value')},
            },
        ),
        migrations.CreateModel(
            name='AttributeValue',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attributes.attribute')),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attributes.attributeoption')),
            ],
            options={
                'unique_together': {('attribute', 'option')},
            },
        ),
    ]
