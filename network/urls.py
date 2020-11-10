
from django.urls import path

from . import views

app_name = "network"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.user_posts, name="profile"),
    path("following", views.following_view, name="following"),
    path("add_post", views.add_post, name="add_post"),
    path("like/<int:post_id>", views.like, name="like"),
    path("posts/<str:username>", views.user_posts, name="user_posts"),
    path("follow_user/<str:user_to_follow>", views.follow_user, name="follow_user"),
    path("posts", views.posts, name="posts"),
]
