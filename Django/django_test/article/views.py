from django.shortcuts import render_to_response
from article.models import Article
from django.http import HttpResponse, HttpResponseRedirect
from forms import ArticleForm
from django.core.context_processors import csrf

def articles(request):
	return render_to_response('articles.html', 
	                         {'articles': Article.objects.all()})
	
def article(request, article_id=1):
	language = 'en-us'
	session_language =  'en-us'
	
	if 'lang' in request.COOKIES:
		language = request.COOKIES['lang']
		
	if 'lang' in request.session:
		session_language = request.session['lang']
		
	return render_to_response('article.html',
	                         {'article': Article.objects.get(id=article_id),
							  'language': language,
							  'session_language': session_language})

def language(request, language='en-us'):
	response = HttpResponse("setting language to %s" % language)
	response.set_cookie('lang', language)
	request.session['lang'] = language
	return response
	
def create(request):
	if request.POST:
		form = ArticleForm(request.POST)
		if form.is_valid():
			form.save()
			
			return HttpResponseRedirect('/articles/all')
	else:
		form = ArticleForm()
	
	args = {}
	args.update(csrf(request))
	args['form'] = form
	
	return render_to_response('create_article.html', args)