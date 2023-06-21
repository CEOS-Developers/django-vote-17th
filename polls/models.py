from django.db import models
from account.models import *

class teamPoll(models.Model):

    team = models.CharField(max_length=10)
    name = models.CharField(max_length=10) # 투표자 이름

    def __str__(self):
        return self.team


class partPoll(models.Model):
    part = models.CharField(max_length=10)
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.part