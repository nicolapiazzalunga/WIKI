from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/search_results", views.search_results, name="search_results"),
    path("wiki/new_entry", views.new_entry, name="new_entry"),
    path("wiki/random_entry", views.random_entry, name="random_entry"),
    path("wiki/edit-<str:entry_name>", views.edit_entry, name="edit_entry"),
    path("wiki/<str:entry_name>", views.entry, name="entry")
]
