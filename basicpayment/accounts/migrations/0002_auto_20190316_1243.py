# Generated by Django 2.1.7 on 2019-03-16 12:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='destination_account',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='destination_currency',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='source_account',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='source_currency',
        ),
        migrations.AddField(
            model_name='transaction',
            name='account',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='transactions', to='accounts.Account', verbose_name='account'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='type',
            field=models.CharField(choices=[(0, 'DEBT'), (1, 'CREDIT')], default=0, max_length=10),
        ),
        migrations.AlterField(
            model_name='account',
            name='currency',
            field=models.CharField(choices=[('USD', 'USD'), ('EUR', 'EUR'), ('CNY', 'CNY')], max_length=5, verbose_name='account currency'),
        ),
    ]
