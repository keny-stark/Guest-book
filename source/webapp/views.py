from django.shortcuts import render, get_object_or_404, redirect
from webapp.models import BookGuest, status_choices
from django.http import HttpResponseNotFound
from webapp.forms import ListForm


def index_views(request, *args, **kwargs):
    search = request.GET.get('search', '')
    if search:
        lists = BookGuest.objects.filter(name__icontains=search, status='active')
    else:
        lists = BookGuest.objects.order_by('-updated_at').filter(status='active')
    return render(request, 'index.html', context={
        'lists': lists
    })


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
            BookGuest.objects.create(
            name=form.cleaned_data['name'],
            text=form.cleaned_data['text'],
            email=form.cleaned_data['email']
            )
            return redirect('index')
        else:
            return render(request, 'add_comit.html', context={'form': form})


def delete_list(request, pk):
    if request.method == 'GET':
        list = get_object_or_404(BookGuest, pk=pk)
        return render(request, 'list.html', context={
            'list': list})
    else:
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
                return redirect('index')
            else:
                return render(request, 'edit.html', context={'form': form, 'lists': lists})
    except BookGuest.DoesNotExist:
        return HttpResponseNotFound("<h2>Article not found</h2>")
