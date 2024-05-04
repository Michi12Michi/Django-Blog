from django.shortcuts import render, HttpResponsePermanentRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from accounts.forms import FormRegister

# Create your views here.
def register_view(request):
    if request.method == "POST":
        form = FormRegister(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            User.objects.create_user(username = username, email = email, password = password)
            user = authenticate(username = username, password = password)
            login(request, user)
            return HttpResponsePermanentRedirect("/")
    else:
        form = FormRegister()
    context = {"form": form}
    return render(request, "accounts/register.html", context)