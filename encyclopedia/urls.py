from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/new", views.new, name="new"),
    path("wiki/random_entry", views.random_entry, name="random_entry"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("wiki/edit/<str:title>", views.edit, name="edit")
]
