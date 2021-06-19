from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Vacancy

from .forms import FindForm

def home_view(request):
    # print(request.POST)
    form = FindForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    form_request = dict()
    if city or language:
        if city:
            form_request['city__slug'] = city
        if language:
            form_request['language__slug'] = language
    querySet = Vacancy.objects.filter(**form_request)


    return render(request, 'myapp/home.html',  {'object_list': querySet,
                                                    'form' : form})

def list_view(request):
    # print(request.POST)
    form = FindForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    form_request = dict()
    if city or language:
        if city:
            form_request['city__slug'] = city
        if language:
            form_request['language__slug'] = language
    querySet = Vacancy.objects.filter(**form_request)
    paginator = Paginator(querySet, 10)  # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'myapp/list.html',  {'object_list': page_obj,
                                                    'form': form})
