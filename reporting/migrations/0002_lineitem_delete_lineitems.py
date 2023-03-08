# Generated by Django 4.1.7 on 2023-02-28 20:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LineItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('description', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='reporting.invoice')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='reporting.job')),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='reporting.payment')),
                ('self_item', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='reporting.lineitem')),
            ],
        ),
        migrations.DeleteModel(
            name='LineItems',
        ),
    ]