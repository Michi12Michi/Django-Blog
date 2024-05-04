from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic import ListView
from forum.models import Sezione, Discussione, Post

class HomeView(ListView):
    queryset = Sezione.objects.all()
    template_name = "core/homepage.html"

def user_profile_view(request, username):
    user = get_object_or_404(User, username=username)
    discussioni = Discussione.objects.filter(autore=user).order_by("-pk")
    context = {"user": user, "discussioni": discussioni}
    return render(request, "core/user_profile.html", context)

class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "core/user_list.html"

def search_form(request):
    if "q" in request.GET:
        querystring = request.GET.get("q")
        if len(querystring) == 0:
            return redirect(reverse("search"))
        discussioni = Discussione.objects.filter(titolo__icontains=querystring)
        posts = Post.objects.filter(contenuto__icontains=querystring)
        users = User.objects.filter(username__icontains=querystring)
        context = {"discussioni": discussioni,
                   "posts": posts,
                   "users": users}
        return render(request, "core/search.html", context)
    else:
        return render(request, "core/search.html")