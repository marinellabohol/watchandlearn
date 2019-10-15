from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	vocabulary = models.IntegerField(default=0)
	reading = models.IntegerField(default=0)
	writing = models.IntegerField(default=0)
	grammar = models.IntegerField(default=0)
	composite = models.IntegerField(default=0)
	level = models.IntegerField(default=1)
	experience = models.IntegerField(default=0)

	def __str__(self):
		return self.user.username

class Word(models.Model):
	name = models.CharField(max_length=100)
	difficulty = models.IntegerField(default=0)

class Topic(models.Model):
	title = models.CharField(max_length=100)
	def __str__(self):
		return self.title

class Interest(models.Model):
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
	topic = models.ForeignKey(Topic, on_delete=models.CASCADE)


class Series(models.Model):
	title = models.CharField(max_length=100)
	image = models.CharField(default='', max_length=300)
	difficulty = models.IntegerField(default=0)
	topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
	def __str__(self):
		return self.title

class Quiz(models.Model):
	title = models.CharField(max_length=100)

	def __str__(self):
		return self.title

class Episode(models.Model):
	title = models.CharField(max_length=100)
	image = models.CharField(default='', max_length=300)
	video = models.CharField(max_length=100)
	number = models.IntegerField(default=1)
	subtitle = models.TextField(default="")
	quiz = models.OneToOneField(Quiz, on_delete=models.CASCADE)
	series = models.ForeignKey(Series, on_delete=models.CASCADE)
	def __str__(self):
		return self.title

class Question(models.Model):
	question_text = models.CharField(max_length=100)
	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
	answer = models.IntegerField(default=0)
	experience = models.IntegerField(default=0)
	option1 = models.CharField(max_length=100)
	option2 = models.CharField(max_length=100)
	option3 = models.CharField(max_length=100)

	def __str__(self):
		return self.question_text
