from polls.models import Choice, Poll
from django.contrib import admin

class ChoiceInline(admin.TabularInline):
	model = Choice
	extra = 3

class PollAdmin(admin.ModelAdmin):
	fields = ['question', 'pub_date']
	inlines = [ChoiceInline]
	list_display = ('question', 'pub_date', 'wasPublishedRecently')
	list_filter = ['pub_date']
	search_fields = ['question']
	date_hierarchy = 'pub_date'

admin.site.register(Poll, PollAdmin)