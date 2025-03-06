# Generated by Django 5.0.6 on 2024-07-21 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arena_events', '0005_rename_nationality_circuit_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='poster',
            field=models.ImageField(blank=True, null=True, upload_to='events/poster/'),
        ),
        migrations.AddField(
            model_name='race',
            name='initial_time_day',
            field=models.CharField(choices=[('Personalized', 'Personalized'), ('Sunrise', 'Sunrise'), ('Morning', 'Morning'), ('Late morning', 'Late morning'), ('Noon', 'Noon'), ('Afternoon', 'Afternoon'), ('Late afternoon', 'Late afternoon'), ('Evening', 'Evening'), ('Sunset', 'Sunset'), ('Night', 'Night'), ('Midnight', 'Midnight')], default='Late morning', max_length=100),
        ),
        migrations.AddField(
            model_name='race',
            name='restrictions',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='race',
            name='start_time_game',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='race',
            name='weather',
            field=models.CharField(choices=[('Random', 'Random'), ('Variable', 'Variable'), ('Clear', 'Clear'), ('Mostly clear', 'Mostly clear'), ('Partly cloudy', 'Partly cloudy'), ('Cloudy', 'Cloudy'), ('Threatening clouds', 'Threatening clouds'), ('Thundering clouds', 'Thundering clouds'), ('Light mist', 'Light mist'), ('Irregular fog', 'Irregular fog'), ('Thick fog', 'Thick fog'), ('Cloudy (dry)', 'Cloudy (dry)'), ('Cloudy (wet)', 'Cloudy (wet)'), ('Fine rain', 'Fine rain'), ('Light rain', 'Light rain'), ('Moderate rain', 'Moderate rain'), ('Heavy rain', 'Heavy rain'), ('Tempest', 'Tempest'), ('Storm', 'Storm')], max_length=100),
        ),
    ]
