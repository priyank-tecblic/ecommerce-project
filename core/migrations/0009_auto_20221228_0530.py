# Generated by Django 3.2.16 on 2022-12-28 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_productcomment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productcomment',
            name='id',
        ),
        migrations.AlterField(
            model_name='productcomment',
            name='cno',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]