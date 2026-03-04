from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'index.html')

def starter(request):
    return render(request, 'starter-page.html')

def about(request):
    return render(request, 'about.html')

def appointment(request):
    return render(request, 'appointment.html')

def services(request):
    return render(request, 'services.html')
    
def departments(request):
    return render(request, 'departments.html')

def doctors(request):
    return render(request, 'doctors.html')

def contact(request):
    return render(request, 'contact.html')