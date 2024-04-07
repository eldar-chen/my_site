from django.db import models

class HangmanGame(models.Model):
    chosen_word = models.CharField(max_length=50)
    chosen_hint = models.CharField(max_length=50)
    word_length = models.IntegerField()
    lives = models.IntegerField(default=6)
    display = models.CharField(max_length=50, default='')

    def save(self, *args, **kwargs):
        if not self.display:
            self.display = '_' * len(self.chosen_word)
        super(HangmanGame, self).save(*args, **kwargs)

    def __str__(self):
        return f"Game with word: {self.chosen_word}"
