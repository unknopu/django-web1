# Generated by Django 3.1.5 on 2021-12-11 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bankservice', '0002_auto_20211207_1531'),
    ]

    operations = [
        migrations.CreateModel(
            name='personalKey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_ref_id', models.CharField(max_length=200, unique=True, verbose_name='userRefId')),
                ('e', models.CharField(max_length=8)),
                ('d', models.CharField(max_length=259)),
                ('n', models.CharField(max_length=259)),
            ],
        ),
        migrations.AlterField(
            model_name='transaction',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='user_model',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
