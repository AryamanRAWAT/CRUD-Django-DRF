# Generated by Django 3.2.18 on 2023-12-16 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='user_details',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('company_name', models.CharField(max_length=70, null=True)),
                ('age', models.IntegerField()),
                ('city', models.CharField(max_length=50, null=True)),
                ('state', models.CharField(max_length=50, null=True)),
                ('zip', models.IntegerField()),
                ('email', models.CharField(max_length=50)),
                ('web', models.CharField(max_length=50)),
            ],
            options={
                'unique_together': {('id', 'first_name')},
            },
        ),
    ]
