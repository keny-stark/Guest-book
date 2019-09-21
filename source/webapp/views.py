from django.shortcuts import render, get_object_or_404, redirect
from webapp.models import BookGuest, status_choices
from django.http import HttpResponseNotFound
from webapp.forms import ListForm
from django.db.models import Q


def index_views(request, *args, **kwargs):
    search = request.GET.get('search', '')
    if search:
        lists = BookGuest.objects.filter(Q(name=search))
    else:
        lists = BookGuest.objects.filter(status='active').order_by('-updated_at')
    return render(request, 'index.html', context={
        'lists': lists
    })


def list_view(request, pk):
    list = get_object_or_404(BookGuest, pk=pk)
    return render(request, 'list.html', context={
        'list': list})


def add_list(request, *args, **kwargs):
    if request.method == 'GET':
        form = ListForm()
        return render(request, 'add_comit.html', context={
            'form': form,
            'category_choices': status_choices
        })
    elif request.method == 'POST':
        form = ListForm(data=request.POST)
        if form.is_valid():
            article = BookGuest.objects.create(
            description=form.cleaned_data['description'],
            status=form.cleaned_data['status'],
            text=form.cleaned_data['text'],
            created_at=form.cleaned_data['created_at']
            )
            return redirect('article', pk=article.pk)
        else:
            return render(request, 'add_comit.html', context={'form': form})


def delete_list(request, pk):
    article = get_object_or_404(BookGuest, pk=pk)
    article.delete()
    return redirect('index')


def update_list(request, pk):
    try:
        articles = get_object_or_404(BookGuest, pk=pk)
        if request.method == 'GET':
            form = ListForm(data={
                'description': articles.description,
                'status': articles.status,
                'text': articles.text,
                'created_at': articles.created_at
            })
            return render(request, 'edit.html', context={
                'articles': articles, 'form': form})
        elif request.method == "POST":
            form = ListForm(data=request.POST)
            if form.is_valid():
                articles.description = form.cleaned_data['description']
                articles.status = form.cleaned_data['status']
                articles.text = form.cleaned_data['text']
                articles.created_at = form.cleaned_data['created_at']
                articles.save()
                return redirect('article', pk=articles.pk)
            else:
                return render(request, 'edit.html', context={'form': form, 'articles': articles})
    except BookGuest.DoesNotExist:
        return HttpResponseNotFound("<h2>Article not found</h2>")
