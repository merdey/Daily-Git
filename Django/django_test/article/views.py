from django.shortcuts import render_to_response
from article.models import Article
from django.http import HttpResponse, HttpResponseRedirect
from forms import ArticleForm
from django.core.context_processors import csrf

def articles(request):
	args = {}
	args.update(csrf(request))
	
	args['articles'] = Article.objects.all()

	return render_to_response('articles.html', args)
	
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
							 
def like_article(request, article_id=1):
	if article_id:
		article = Article.objects.get(id=article_id)
		article.likes += 1
		article.save()
	
	return HttpResponseRedirect('/articles/get/%s' % article_id)

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
	
def search_titles(request):
	if request.method == "POST":
		search_text = request.POST['search_text']
	else:
		search_text = ''
		
	articles = Article.objects.filter(title__contains=search_text)
	
	return render_to_response('ajax_search.html', {'articles': articles})