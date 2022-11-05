# Generated by Django 4.0.6 on 2022-11-04 00:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bus',
            name='destination',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arrivals', to='tickets.busstop'),
        ),
        migrations.AlterField(
            model_name='bus',
            name='origin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departures', to='tickets.busstop'),
        ),
        migrations.AlterField(
            model_name='train',
            name='destination',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arrivals', to='tickets.railway'),
        ),
        migrations.AlterField(
            model_name='train',
            name='origin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departures', to='tickets.railway'),
        ),
    ]