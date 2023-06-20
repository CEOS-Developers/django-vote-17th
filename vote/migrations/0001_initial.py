
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='파트장 후보 이름')),
                ('part', models.CharField(max_length=20, verbose_name='파트')),
                ('vote_cnt', models.IntegerField(default=0, verbose_name='투표 횟수')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('team', models.CharField(max_length=20, unique=True, verbose_name='팀이름')),
                ('vote_cnt', models.IntegerField(default=0, verbose_name='투표 횟수')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TeamVote',
            fields=[
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CandidateVote',
            fields=[

            ],
            options={
                'abstract': False,
            },
        ),
    ]
