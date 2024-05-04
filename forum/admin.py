from django.contrib import admin
from .models import Sezione, Discussione, Post

# Register your models here.
class DiscussioneModelAdmin(admin.ModelAdmin):
    model = Discussione
    list_display = ['titolo', 'sezione', 'autore']
    search_fields = ['titolo', 'autore']
    list_filter = ['sezione', 'data_creazione']

class PostModelAdmin(admin.ModelAdmin):
    model = Post
    list_display = ['autore', 'discussione']
    search_fields = ['contenuto']
    list_filter = ['data_creazione', 'autore']

class SezioneModelAdmin(admin.ModelAdmin):
    model = Sezione
    list_display = ['nome_sezione', 'descrizione']

admin.site.register(Sezione, SezioneModelAdmin)
admin.site.register(Discussione, DiscussioneModelAdmin)
admin.site.register(Post, PostModelAdmin)