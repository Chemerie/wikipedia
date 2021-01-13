from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.page, name="page"),
    path("wiki/newpage/", views.newpage, name="newpage"),
    path("editpage/<str:name>", views.editpage, name="editpage"),
    path("Random/", views.rand, name="rand"),
  
]
 