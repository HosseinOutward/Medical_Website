from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'base_panel/home.html')


def about(request):
    return render(request, 'base_panel/about.html', {'name': 'About'})


@login_required(login_url='login')
def panel(request):
    return render(request, 'index.html')


def contact(request):
    return render(request, 'base_panel/contact.html')


def case_study(request):
    return render(request, 'base_panel/page-portfolio-case-study.html')