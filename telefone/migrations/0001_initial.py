# Generated by Django 3.0.5 on 2020-04-01 21:15

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contato', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_infos', django.contrib.postgres.fields.jsonb.JSONField()),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contato.Contact')),
            ],
        ),
    ]
