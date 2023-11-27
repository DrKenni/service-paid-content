# Generated by Django 4.2.7 on 2023-11-23 22:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_about_me_alter_user_creation_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='название')),
                ('price', models.PositiveIntegerField(default=1, verbose_name='стоймость')),
                ('length', models.CharField(choices=[(1, 'месяц'), (3, 'три месяца'), (6, 'шесть месяцев'), (12, 'двенадцать месяцев')], default=1, verbose_name='длительность')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plan_own', to=settings.AUTH_USER_MODEL, verbose_name='владелец')),
            ],
        ),
    ]