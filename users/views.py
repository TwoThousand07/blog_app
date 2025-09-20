from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import logout

from .forms import UserRegistrationForm

def user_register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/registration.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        redirect('login')