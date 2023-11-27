# Generated by Django 4.2.7 on 2023-11-27 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0002_payment_plan'),
    ]

    operations = [
        migrations.AddField(
            model_name='paidsubscription',
            name='active',
            field=models.BooleanField(default=False, verbose_name='активация'),
        ),
        migrations.AlterField(
            model_name='paidsubscription',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='дата окончания подписки'),
        ),
        migrations.AlterField(
            model_name='paidsubscription',
            name='start_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='дата начала подписки'),
        ),
    ]
