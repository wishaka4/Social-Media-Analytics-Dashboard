# Generated by Django 3.1.8 on 2024-04-11 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RedditPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=255)),
                ('score', models.IntegerField()),
                ('num_comments', models.IntegerField()),
                ('upvote_ratio', models.FloatField()),
                ('selftext', models.TextField()),
                ('link_flair_text', models.CharField(max_length=255)),
            ],
        ),
    ]
