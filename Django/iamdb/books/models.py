from django.db import models

class Book(models.Model):
	title = models.CharField(max_length=100)
	review = models.TextField()
	rating = models.IntegerField()
	status = models.CharField(max_length=20)
