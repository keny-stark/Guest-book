from django.shortcuts import render, get_object_or_404, redirect
from webapp.models import Article, status_choices
from django.http import HttpResponseNotFound
from webapp.forms import ArticleForm


def index_views(request, *args, **kwargs):

    articles = Article.objects.all()
    return render(request, 'index.html', context={
        'articles': articles
    })


def article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'articale_view.html', context={
        'article': article})


def article_create_view(request, *args, **kwargs):
    if request.method == 'GET':
        form = ArticleForm()
        return render(request, 'create_view.html', context={
            'form': form,
            'category_choices': status_choices
        })
    elif request.method == 'POST':
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            article = Article.objects.create(
            description=form.cleaned_data['description'],
            status=form.cleaned_data['status'],
            text=form.cleaned_data['text'],
            created_at=form.cleaned_data['created_at']
            )
            return redirect('article', pk=article.pk)
        else:
            return render(request, 'create_view.html', context={'form': form})


def delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.delete()
    return redirect('index')


def edit_view(request, pk):
    try:
        articles = get_object_or_404(Article, pk=pk)
        if request.method == 'GET':
            form = ArticleForm(data={
                'description': articles.description,
                'status': articles.status,
                'text': articles.text,
                'created_at': articles.created_at
            })
            return render(request, 'edit.html', context={
                'articles': articles, 'form': form})
        elif request.method == "POST":
            form = ArticleForm(data=request.POST)
            if form.is_valid():
                articles.description = form.cleaned_data['description']
                articles.status = form.cleaned_data['status']
                articles.text = form.cleaned_data['text']
                articles.created_at = form.cleaned_data['created_at']
                articles.save()
                return redirect('article', pk=articles.pk)
            else:
                return render(request, 'edit.html', context={'form': form, 'articles': articles})
    except Article.DoesNotExist:
        return HttpResponseNotFound("<h2>Article not found</h2>")


def delete_more(request, *args, **kwargs):
    article = Article.objects.all()
    for i in article:
        pk = request.POST.get(str(i.pk))
        if pk == str(i.pk):
            i.delete()
    return redirect('index')