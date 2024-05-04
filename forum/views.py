from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.generic.edit import CreateView, DeleteView
from .forms import DiscussioneModelForm, PostModelForm
from .mixin import StaffMixin
from .models import Discussione, Sezione, Post

PAGES = 5

# Create your views here.
class CreaSezione(StaffMixin, CreateView):
    model = Sezione
    fields = "__all__"
    template_name = "forum/create_section.html"
    success_url = "/"

def visualizza_sezione(request, pk):
    sezione = get_object_or_404(Sezione, pk=pk)
    discussioni_sezione = Discussione.objects.filter(sezione=sezione).order_by("-data_creazione")
    context = {"sezione": sezione, "discussioni": discussioni_sezione}
    return render(request, "forum/sectionview.html", context)

@login_required
def crea_discussione(request, pk):
    sezione = get_object_or_404(Sezione, pk=pk)
    if request.method == "POST":
        form = DiscussioneModelForm(request.POST)
        if form.is_valid():
            discussione = form.save(commit=False)
            discussione.sezione = sezione
            discussione.autore = request.user
            discussione.save()
            Post.objects.create(autore=request.user, discussione=discussione, contenuto=form.cleaned_data["contenuto"])
            return HttpResponseRedirect(reverse("view-discussion", kwargs={"pk": discussione.pk}))
    else:
        form = DiscussioneModelForm()
    context = {"form": form, "sezione": sezione}
    return render(request, "forum/new_discussion.html", context)

def visualizza_discussione(request, pk):
    discussione = get_object_or_404(Discussione, pk=pk)    
    posts_discussione = Post.objects.filter(discussione=discussione)
    paginator = Paginator(posts_discussione, PAGES)
    page = request.GET.get("page")
    posts_rendered = paginator.get_page(page)
    form_risposta = PostModelForm()
    context = {"discussione": discussione, "posts": posts_rendered, "form": form_risposta}
    return render(request, "forum/single_discussion.html", context)

@login_required
def crea_post(request, pk):
    discussione = get_object_or_404(Discussione, pk=pk)
    if request.method == "POST":
        form = PostModelForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.discussione = discussione
            form.instance.autore = request.user
            form.save()
            url_to_redirect = reverse("view-discussion", kwargs={"pk": pk})
            pagine = discussione.get_n_page(PAGES)
            if pagine > 1:
                url_to_redirect += f"?page={pagine}"
            return HttpResponseRedirect(url_to_redirect)
    else:
        return HttpResponseBadRequest()
    
class CancellaPost(DeleteView):
    # post_confirm_delete
    model = Post
    success_url = "/"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(autore=self.request.user.id)