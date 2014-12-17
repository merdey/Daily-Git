import datetime
from django.utils import timezone
from django.db import models

class Poll(models.Model):
	question = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')

	def wasPublishedRecently(self):
		return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
	wasPublishedRecently.admin_order_field = 'pub_date'
	wasPublishedRecently.boolean = True
	wasPublishedRecently.short_description = 'Published recently?'

	def __unicode__(self):
		return self.question

class Choice(models.Model):
	poll = models.ForeignKey(Poll)
	choice = models.CharField(max_length=200)
	votes = models.IntegerField()

def __unicode__(self):
	return self.choice
