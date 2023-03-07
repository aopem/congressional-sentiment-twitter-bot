from django.db import models

class CongressMember(models.Model):
    id = models.CharField(primary_key=True)
    first_name = models.CharField()
    last_name = models.CharField()
    gender = models.CharField()
    party = models.CharField()
    state = models.CharField()
    twitter_account_name = models.CharField()
    chamber = models.IntegerField()
    middle_name = models.CharField(null=True)
