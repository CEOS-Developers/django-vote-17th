from django.db import models


class Poll(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Vote(models.Model):
    # 어떤 투표인지 : 데모데이/파트장
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    # 투표자가 누구인지(중복 확인)
    voter = models.ForeignKey('account.User', on_delete=models.CASCADE)

    # related_name = 'votes'로 user.votes.all()로 접근 가능
    target_account = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='votes', null=True)
    # related_name = 'votes'로 team.votes.all()로 접근 가능
    target_team = models.ForeignKey('account.Team', on_delete=models.CASCADE, related_name='votes', null=True)

    def __str__(self):
        return self.poll

