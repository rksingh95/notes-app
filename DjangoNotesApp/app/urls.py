from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("profile/signup", views.handle_user_signup, name="handle_user_signup"),
    path("profile/login", views.handle_user_login, name="handle_user_login"),
    path("logout", views.handle_user_logout, name="handle_user_logout"),
    path("addnote", views.add_note, name="add_note"),
    path("edit/note/<str:note_id>", views.edit_note, name="edit_note"),
    path("update/note/<str:note_id>", views.update_note, name="update_note"),
    path("search/note/<str:tag>", views.search_note, name="search_note"),
    path("delete/note/<str:note_id>", views.delete_note, name="delete_note"),
]
