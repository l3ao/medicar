# Generated by Django 4.1.7 on 2023-02-26 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consulta',
            name='data_agendamento',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Data do agendamento'),
        ),
    ]