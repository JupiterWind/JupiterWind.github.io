from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create" ),
    path("category/<str:category>", views.category, name="category" ),
    path("<int:auction_id>", views.detail, name="detail"),
    path("comment/<int:auction_id>", views.comment, name="comment"),
    path("bid/<int:auction_id>", views.bid, name="bid"),
    path("close/<int:auction_id>", views.close, name="close"),
    path("watch/<str:user_id>", views.watch, name="watch"),
]
