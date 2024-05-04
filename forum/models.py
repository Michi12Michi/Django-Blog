from django.db import models
from django.contrib.auth.models import User
from math import ceil

# Create your models here.
class Sezione(models.Model):
    nome_sezione = models.CharField(max_length=80)
    descrizione = models.CharField(max_length=150, blank=True, null=True)
    logo_sezione = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.nome_sezione
    
    def get_last_discussions(self):
        return Discussione.objects.filter(sezione=self).order_by("-data_creazione")[:2]
    
    def get_all_posts(self):
        return Post.objects.filter(discussione__sezione=self).count()
    
    class Meta:
        verbose_name = "Sezione"
        verbose_name_plural = "Sezioni"

class Discussione(models.Model):
    titolo = models.CharField(max_length=120)
    data_creazione = models.DateTimeField(auto_now_add=True)
    autore = models.ForeignKey(User, on_delete=models.CASCADE, related_name="discussioni")
    sezione = models.ForeignKey(Sezione, on_delete=models.CASCADE)

    def __str__(self):
        return self.titolo
    
    def get_n_page(self, page):
        posts = self.post_set.count()
        return ceil(posts/page)
    
    class Meta:
        verbose_name = "Discussione"
        verbose_name_plural = "Discussioni"

class Post(models.Model):
    autore = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    contenuto = models.TextField()
    data_creazione = models.DateTimeField(auto_now_add=True)
    discussione = models.ForeignKey(Discussione, on_delete=models.CASCADE)

    def __str__(self):
        return self.autore.username