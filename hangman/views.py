from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from .models import HangmanGame
import random
import logging


word_list = [
    'abruptly',
    'absurd',
    'abyss',
    'avenue',
    'awkward',
    'bagpipes',
    'bandwagon',
    'beekeeper',
    'bikini',
    'blizzard',
    'boggle',
    'bookworm',
    'boxcar',
    'boxful',
    'buffalo',
    'buffoon',
    'cockiness',
    'curacao',
    'cycle',
    'daiquiri',
    'disavow',
    'dizzying',
    'duplex',
    'dwarves',
    'embezzle',
    'equip',
    'espionage',
    'faking',
    'fishhook',
    'fixable',
    'fjord',
    'flyby',
    'funny',
    'galaxy',
    'glowworm',
    'gossip',
    'icebox',
    'injury',
    'jackpot',
    'jaundice',
    'jawbreaker',
    'jaywalk',
    'jelly',
    'jigsaw',
    'jinx',
    'jiujitsu',
    'jogging',
    'joking',
    'joyful',
    'jumbo',
    'kayak',
    'khaki',
    'kilobyte',
    'kiosk',
    'lucky',
    'microwave',
    'oxygen',
    'puppy',
    'quartz',
    'shiv',
    'staff',
    'stronghold',
    'subway',
    'unknown',
    'unworthy',
    'vodka',
    'whiskey',
    'wimpy',
    'witchcraft',
    'wizard',
    'zipper',
    'zombie',
]

hint_list = [
    'suddenly',
    'nonsense',
    'a dark place',
    'big street',
    'unpleasant',
    'a Scottish thing',
    'band car',
    'honey maker',
    'hot summer shit',
    'way too cold',
    'shmoggle',
    'nerd',
    'square car',
    'full',
    'animal',
    'animal',
    'trait of a shit person',
    'a Danish island in the Caribbean',
    'of life',
    'a drink?',
    'unclaim',
    'making you sick',
    'no idea you figure it out',
    'midgets', 'illegally claim',
    'put on',
    'sneaky stuff for the government',
    'lying',
    'something used to catch fish',
    'not broken',
    'river surrounded by mountains',
    'saying hi in the sky',
    'hilarious',
    'star neighborhood',
    'a worm that glows',
    'spreading fake news',
    'a cold box',
    'pain in the ass',
    'Fuck yeah!',
    'yellowing of the skin',
    'candy from Ed, Edd and Eddy',
    'law that restricts freedom of navigation for pedestrians',
    'yummy',
    'puzzle',
    'fuck',
    'martial art',
    'fancy way of running',
    'not really',
    'happy',
    'American size',
    'dumb small boat',
    'color',
    'smallest byte',
    'place to buy beer',
    'bastard',
    'gets your shit warm',
    'will die without it',
    'cute fucker',
    'best watch',
    'prison weapon :)',
    'slaves',
    'where cunts tend to hide with lots of guns',
    'can ride it, can eat it. what is it?',
    'nobody knows',
    'im [ ] of thors hammer',
    "Russia's favorite",
    "a man's drink",
    'skinny cunt',
    'old cunt in a hat throwing fire balls',
    'old cunt in a hat',
    'thing that can get stuck on your balls',
    'a healthy dead'
]

chosen_word = random.choice(word_list)
word_index = word_list.index(chosen_word)
chosen_hint = hint_list[word_index]
word_length = len(chosen_word)


def create_game():
    default_lives = 6

    chosen_word = random.choice(word_list)
    word_index = word_list.index(chosen_word)
    chosen_hint = hint_list[word_index]
    word_length = len(chosen_word)

    game_obj, created = HangmanGame.objects.get_or_create(
        chosen_word=chosen_word,
        chosen_hint=chosen_hint,
        defaults={'word_length': word_length, 'lives': default_lives, 'display': '_' * word_length}
    )

    if game_obj.lives < default_lives:
        print("Deleting entry...")
        game_obj.delete()
    elif not created:
        # Update the existing entry if it already exists
        game_obj.chosen_hint = chosen_hint
        game_obj.word_length = word_length
        game_obj.lives = default_lives
        game_obj.display = '_' * word_length
        game_obj.save()
    elif game_obj.lives < default_lives:
        print("Deleting entry...")
        game_obj.delete()

    print(f"Word: {chosen_word}")
    print(f"Hint: {chosen_hint}")
    print(f"Lives: {game_obj.lives}")


create_game()


class HangmanView(View):
    def get(self, request):
        if 'hangman_game_id' in request.session:
            try:
                hangman_game = HangmanGame.objects.get(
                    pk=request.session['hangman_game_id'])
            except HangmanGame.DoesNotExist:
                # Handle the case where the HangmanGame does not exist
                del request.session['hangman_game_id']
                return redirect('hangman')
        else:
            hangman_game = HangmanGame.objects.order_by('?').first()
            request.session['hangman_game_id'] = hangman_game.id

        context = {
            'hangman_game': hangman_game,
        }
        return render(request, 'hangman/index.html', context)

    def post(self, request):
        if 'hangman_game_id' in request.session:
            hangman_game = HangmanGame.objects.get(
                pk=request.session['hangman_game_id'])
        else:
            # Redirect to start a new game if no game is in progress
            return redirect('hangman')

        guessed_letter = request.POST.get('guess', '').lower()

        if guessed_letter not in hangman_game.chosen_word:
            hangman_game.lives -= 1
        else:
            display_list = list(hangman_game.display)
            for i, letter in enumerate(hangman_game.chosen_word):
                if guessed_letter == letter:
                    display_list[i] = guessed_letter
                    if "_" not in display_list:
                        # Remove the current game session
                        hangman_game.delete()
                        return render(request, 'hangman/you_won.html')
            hangman_game.display = "".join(display_list)

        if hangman_game.lives == 0:
            # return HttpResponse(f'Game over. The word was {hangman_game.chosen_word}.')
            # Remove the current game session
            hangman_game.delete()
            return render(request, 'hangman/game_over.html')
        hangman_game.save()

        return redirect('hangman')


def new_game(request):
    if 'hangman_game_id' in request.session:
        del request.session['hangman_game_id']

    create_game()

    return redirect('hangman')


def you_won(request):
    if 'hangman_game_id' in request.session:
        game_id = request.session['hangman_game_id']
        HangmanGame.objects.filter(id=game_id).delete()
        del request.session['hangman_game_id']

    create_game()

    return render(request, 'hangman/you_won.html')


def game_over(request):
    if 'hangman_game_id' in request.session:
        game_id = request.session['hangman_game_id']
        HangmanGame.objects.filter(id=game_id).delete()
        del request.session['hangman_game_id']

    create_game()

    return render(request, 'hangman/game_over.html')
