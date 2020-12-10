from django.shortcuts import render


def home(request):
    return render(request, 'base_app/index.html')


def about(request):
    return render(request, 'base_app/page-company-about.html', {'name': 'About'})

def panel(request):
    return render(request, 'base_app/home.html')

def contact(request):
    return render(request, 'base_app/page-company-contact.html')

def case_study(request):
    return render(request, 'base_app/page-portfolio-case-study.html')