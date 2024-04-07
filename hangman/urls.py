from django.urls import path
from . import views

urlpatterns = [
    path("", views.HangmanView.as_view(), name="hangman"),
    path("new_game/", views.new_game, name="new_game"),
    path("you_won/", views.you_won, name="you_won"),
]
