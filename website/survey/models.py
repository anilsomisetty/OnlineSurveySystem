# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class user(models.Model):
	 user = models.OneToOneField(User, on_delete=models.CASCADE)
class Survey(models.Model):
	#surveyid=models.IntegerField(primary_key=True)
	surveyname=models.CharField(max_length=50)
	surveymessage=models.TextField(max_length=2000,default='New Survey')
	numberofquestions=models.IntegerField(default=0)
	userid=models.CharField(max_length=100,default='admin')
	check=models.BooleanField(default=True)
	#userid=models.ForeignKey('user')

class questions(models.Model):
	questionid=models.IntegerField(default=0)
	question=models.CharField(max_length=200,default='question')
	option1=models.CharField(max_length=100)
	option2=models.CharField(max_length=100)
	option3=models.CharField(max_length=100)
	option4=models.CharField(max_length=100)
	count1=models.IntegerField(default=0)
	count2=models.IntegerField(default=0)
	count3=models.IntegerField(default=0)
	count4=models.IntegerField(default=0)
	yid=models.IntegerField(default=0)
	#numberofquestions=models.IntegerField(default=0)

