# Generated by Django 3.1.2 on 2020-10-14 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_category',
            field=models.CharField(choices=[('python', 'python'), ('java', 'java'), ('php', 'php'), ('c', 'c')], default='', max_length=100),
        ),
    ]
