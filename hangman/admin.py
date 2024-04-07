from django.contrib import admin

# Register your models here.
from .models import HangmanGame

@admin.register(HangmanGame)
class HangmanGameAdmin(admin.ModelAdmin):
    list_display = ['chosen_word', 'chosen_hint', 'word_length', 'lives', 'display']
    list_filter = ['lives']
    search_fields = ['chosen_word', 'chosen_hint']
