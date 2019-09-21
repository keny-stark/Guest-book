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
            name=form.cleaned_data['name'],
            text=form.cleaned_data['text'],
            email=form.cleaned_data['email']
            )
            return redirect('list_view', pk=article.pk)
        else:
            return render(request, 'add_comit.html', context={'form': form})


def delete_list(request, pk):
    list = get_object_or_404(BookGuest, pk=pk)
    list.delete()
    return redirect('index')


def update_list(request, pk):
    try:
        lists = get_object_or_404(BookGuest, pk=pk)
        if request.method == 'GET':
            form = ListForm(data={
                'name': lists.name,
                'text': lists.text,
                'email': lists.email
            })
            return render(request, 'edit.html', context={
                'lists': lists, 'form': form})
        elif request.method == "POST":
            form = ListForm(data=request.POST)
            if form.is_valid():
                lists.name = form.cleaned_data['name']
                lists.text = form.cleaned_data['text']
                lists.email = form.cleaned_data['email']
                lists.save()
                return redirect('article', pk=lists.pk)
            else:
                return render(request, 'edit.html', context={'form': form, 'lists': lists})
    except BookGuest.DoesNotExist:
        return HttpResponseNotFound("<h2>Article not found</h2>")
