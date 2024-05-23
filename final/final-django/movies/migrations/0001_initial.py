# Generated by Django 4.2.8 on 2024-05-23 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('genreId', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='OTTPlatform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('platformId', models.IntegerField()),
                ('logopath', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('casts', models.JSONField()),
                ('overview', models.TextField()),
                ('popularity', models.FloatField()),
                ('poster_path', models.CharField(max_length=255)),
                ('release_date', models.DateField()),
                ('title', models.CharField(max_length=100)),
                ('vote_average', models.FloatField()),
                ('vote_count', models.IntegerField()),
                ('genres', models.ManyToManyField(related_name='movies', to='movies.genre')),
                ('likes', models.ManyToManyField(blank=True, related_name='liked_movies', to='accounts.userinfo')),
                ('ott_platforms', models.ManyToManyField(related_name='movies', to='movies.ottplatform')),
            ],
        ),
    ]
