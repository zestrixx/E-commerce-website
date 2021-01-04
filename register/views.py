from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import RegisterForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username} Your account has been created. Login to continue')
        return redirect('Login')
    else:
        form = RegisterForm()
    return render(request, 'register/signup.html', {'form': form})
