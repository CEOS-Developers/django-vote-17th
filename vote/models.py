from django.db import models
from account.models import *

from account.models import CommonInfo;


class Team(CommonInfo):
    name = models.CharField(max_length=100, unique=True)
    voteCount = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class TeamVote(CommonInfo):
    userPk = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name="TeamVoteUserPk")
    teamPk = models.ForeignKey("Team",
                               on_delete=models.CASCADE,
                               related_name="TeamVoteTeamPk")

    def __str__(self):
        return "TeamVote"


class Candidate(CommonInfo):
    name = models.CharField(max_length=100, unique=True)
    part = models.CharField(max_length=30)
    voteCount = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class CandidateVote(CommonInfo):
    userPk = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name="CandidateVoteUserPk")
    candidatePk = models.ForeignKey("Candidate",
                                    on_delete=models.CASCADE,
                                    related_name="CandidateVoteCandidatePk")

    def __str__(self):
        return "CandidateVote"