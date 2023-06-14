from django.db import models
from account.models import *

from account.models import CommonInfo;


class Team(CommonInfo):
    team = models.CharField("팀이름",max_length=20, unique=True)
    vote_cnt = models.IntegerField("투표 횟수",default=0)

    def __str__(self):
        return self.team


class TeamVote(CommonInfo):
    # user_id=models.ForeignKey(User,
    #                            on_delete=models.CASCADE,
    #                            related_name="TeamVoteUserPk") #투표자
    team=models.ForeignKey(Team,
                               on_delete=models.CASCADE,
                               related_name="TeamVoteTeamPk") #팀 투표

    user_name = models.CharField("투표자이름", max_length=20, default='ceos') # 투표자 이름

    def __str__(self):
        return "TeamVote"


class Candidate(CommonInfo):
    name = models.CharField("파트장 후보 이름",max_length=20, unique=True)
    part = models.CharField("파트",max_length=20)
    vote_cnt = models.IntegerField("투표 횟수",default=0)

    def __str__(self):
        return self.name


class CandidateVote(CommonInfo):
    user_id = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name="CandidateVoteUserPk") #투표자
    candidate = models.ForeignKey(Candidate,
                                  on_delete=models.CASCADE,
                                  related_name="CandidateVoteCandidatePk") #후보자 선택

    def __str__(self):
        return "CandidateVote"