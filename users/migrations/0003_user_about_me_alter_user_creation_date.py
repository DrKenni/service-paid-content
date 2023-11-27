# Generated by Django 4.2.7 on 2023-11-23 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_rename_comment_user_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='about_me',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='фамилия'),
        ),
        migrations.AlterField(
            model_name='user',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='дата создания аккаунта'),
        ),
    ]
