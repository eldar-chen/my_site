from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Starting_pageView.as_view(), name="starting-page"),
    path("posts/", views.posts, name="posts-page"),
    path("posts/<slug:slug>", views.post_detail,
         name="post-detail-page"),

]
