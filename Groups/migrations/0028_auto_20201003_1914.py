# Generated by Django 3.1.1 on 2020-10-03 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Groups', '0027_auto_20201003_1905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='marks',
            field=models.ManyToManyField(related_name='stud_set', to='Groups.Mark'),
        ),
    ]