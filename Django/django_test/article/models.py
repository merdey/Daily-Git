from django.db import models

class Article(models.Model):
	title = models.CharField(max_length=200)
	body = models.TextField()
	pub_date =  models.DateTimeField('date published')
	likes = models.IntegerField(default=0)
	
	def __unicode__(self):
		return self.title