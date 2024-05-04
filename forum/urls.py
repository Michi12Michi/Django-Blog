from django.urls import path
from . import views

urlpatterns = [
    path('new-section', views.CreaSezione.as_view(), name='create-section'),
    path('section/<int:pk>', views.visualizza_sezione, name="single-section-view"),
    path('section/<int:pk>/new-discussion', views.crea_discussione, name="create-discussion"),
    path('discussion/<int:pk>', views.visualizza_discussione, name="view-discussion"),
    path('discussion/<int:pk>/answer', views.crea_post, name="create-post"),
    path('discussion/<int:id>/delete/<int:pk>', views.CancellaPost.as_view(), name='delete-post'),
]
