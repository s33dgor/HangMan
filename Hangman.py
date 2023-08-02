from dataclasses import dataclass
from collections import Counter
from random import choice
import pygame
from getpass import getpass
from typing import List

@dataclass
class GameParams:
    mode: str
    hardness: str


class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def take_valid_input(valid_input: list, var: str) -> str:
    user_input = None
    while user_input not in valid_input:
        g_input = input(f'\nWhat is your preferred {var.replace("_", " ")} {"[" + "/".join(valid_input) + "]"} ?? ')
        if g_input.lower() in valid_input:
            user_input = g_input.lower()
            print(f'\nYour preferred {var.replace("_", " ")} is {user_input}')
        else:
            print('\nSorry!!! Please Enter valid input')
    return user_input


class PhraseInstance:
    def __init__(self, true_phrase):
        self.true_phrase = true_phrase
        self.guess_phrase_dict = {ch: 0 if ch.isalnum() else 1 for ch in true_phrase.lower()}
        self.ch_freq = Counter(true_phrase.lower())
        self.remaining_count = sum(1 - self.guess_phrase_dict[ch] for ch in true_phrase.lower())

    def is_guessed(self) -> bool:
        return set(self.guess_phrase_dict.values()) == {1}

    def make_guess(self, guess) -> int:
        guess = guess.lower()
        if len(guess) == 1 and guess in self.guess_phrase_dict:
            if self.guess_phrase_dict[guess] == 0:
                self.guess_phrase_dict[guess] = 1
                self.remaining_count -= self.ch_freq[guess]
                return True
            else:
                print('You already guessed it')
                return True
        elif guess == self.true_phrase.lower():
            for ch in self.true_phrase.lower():
                self.guess_phrase_dict[ch] = 1
            self.remaining_count = 0
            return True
        else:
            return False

    def display_phrase(self):
        disp_str = ''
        for ch in self.true_phrase:
            if self.guess_phrase_dict[ch.lower()] == 1:
                disp_str += " " + ch
            else:
                disp_str += ' _'
        return disp_str


def init():
    game_mode = take_valid_input(['cpu', 'user'], 'game_mode')
    hardness = take_valid_input(['easy', 'medium', 'hard'], 'hardness')
    if game_mode == 'cpu':
        game_params = GameParams(game_mode, hardness)
    else:
        game_params = GameParams(game_mode, hardness='None')
    return game_params


def game(phrase):
    p = PhraseInstance(phrase)
    while p.wrong_guess != 11 and not p.is_guessed():
        if p.wrong_guess == 0:
            print(p.display_phrase())
        guess = input("\nWhat's your guess: ")
        count = p.make_guess(guess)
        print(p.display_phrase())
        print(f'You have {count} remaining')
        print(f'You got {11 - p.wrong_guess} guess left')
        if p.is_guessed():
            print('\nBravo!!! You guessed it correct ')
    if not p.is_guessed():
        print('\nOOps!!! you lost, Better luck next time')


def run_game():
    game_init = init()
    game_mode = game_init.mode
    hardness = game_init.hardness
    if game_mode == 'cpu':
        movies_list = [movies.rstrip() for movies in open('Hangman_movies')]
        phrase = choice(movies_list)
        game(phrase)
    else:
        phrase = getpass('Give your phrase: ')
        game(phrase)

# run_game()


def load_images(n: int, name: str, i: int = 0) -> list:
    images = []
    for image_index in range(n):
        if i != 0:
            images.append(pygame.image.load(f'{name + str(image_index)}.png'))
        else:
            images.append(pygame.image.load(f'{name}.png'))
    return images


def make_buttons(n: int, names: list, cor: list, dim: list) -> list:
    l_buttons = []
    length, breath = dim
    gap = length + 50
    x_cor, y_cor = cor
    for i in range(n):
        l_buttons.append([x_cor, y_cor, length, breath, names[i]])
        x_cor += gap
        y_cor = cor[-1]
    return l_buttons


def display_word(word: str, color: str, cor: list, size:int):
    font = pygame.font.SysFont('comicsans', size)
    text = font.render(word, 1, color)
    screen.blit(text, cor)


def display_buttons(buttons: list):
    for button in buttons:
        x_cor, y_cor, length, breath = button[0: 4]
        name = button[-1]
        pygame.draw.rect(screen, black, [x_cor, y_cor, length, breath], 2)
        display_word(name, blue_violet, [x_cor + 30, y_cor + 15], 40)

def selected_buttons(buttons: List[list], cor: List[int], var:str) -> str:
    m_x, m_y = cor
    for button in buttons:
        x, y, l, b = button[0: 4]
        if x <= m_x <= x + l and y <= m_y <= y + b:
            globals()[var] = button[-1]
        else:
            pass

def game():
    movies_list = [movies.rstrip() for movies in open('Hangman_movies')]
    phrase = choice(movies_list)
    global p
    p = PhraseInstance(phrase)
    global disp_phrase
    disp_phrase = p.display_phrase()
    global guessed_letters
    guessed_letters = []

pygame.init()

white = [255, 255, 255]
black = [0, 0, 0]
red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]
blue_violet = [138,43,226]

screen = pygame.display.set_mode([1200, 800])
pygame.display.set_caption('Hangman')


FPS = 60
clock = pygame.time.Clock()
Hangman = load_images(1, 'hangman-name')
images = load_images(11, '', 11)


screen.fill(white)
game_modes = make_buttons(2, ['cpu', 'user'], [430, 558], [150, 100])
hardness = make_buttons(3, ['easy', 'medium', 'hard'], [260, 558], [200, 100])
replay = make_buttons(2, ['Yes', 'No'], [430, 400], [150, 100])


game_status = Hangman + images
phrases = ['Choose your Game mode', 'Choose your difficulty']

game()

wrong_guesses = 0
j = 0
running = True
while running:
    clock.tick(FPS)
    # game gets finished by wining
    if p.is_guessed():
        screen.fill(white)
        display_word('BRAVO !!! You did it', black, [412, 113], 40)
        display_word('Want to play it again', green, [410, 300], 40)
        display_buttons(replay)

    # game gets finished by losing
    if wrong_guesses == 11:
        screen.fill(white)
        display_word('OOps!!! you lost, Better luck next time', black, [240, 113], 40)
        display_word('Want to play it again', green, [410, 300], 40)
        display_buttons(replay)


    if wrong_guesses == 0:
        try:
            if replay_choice == 'Yes':
                game()
                screen.fill(white)
                screen = pygame.display.set_mode([1200, 800])
                screen.fill(white)
        except:
            pass
        screen = pygame.display.set_mode([1200, 800])
        screen.fill(white)
        screen.blit(game_status[wrong_guesses], (300, 50))

    elif wrong_guesses < 11 and not p.is_guessed():
        screen = pygame.display.set_mode([1200, 600])
        screen.fill(white)
        screen.blit(game_status[wrong_guesses], (90, 50))

    if j == 0:
        display_word(phrases[j], red, [373, 447], 40)
        display_buttons(game_modes)

    elif game_mode == 'cpu' and j == 1:
        display_word(phrases[j], red, [385, 447], 40)
        display_buttons(hardness)


    elif game_mode == 'cpu' and wrong_guesses < 11 and not p.is_guessed():
        display_word('Your phrase to guess', blue, [370, 70], 40)
        display_word(disp_phrase, black, [370, 150], 30)
        display_word('Your guessed letters till now', blue, [370, 210], 30)
        display_word(str(guessed_letters), red, [360, 260], 20)
        display_word(f'You got {11 - wrong_guesses} guess left', black, [370, 300], 30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            m_x, m_y = pygame.mouse.get_pos()
            print(m_x, m_y)
            if j == 0:
                selected_buttons(game_modes, [m_x, m_y], 'game_mode')
                try:
                    print(game_mode)
                    j += 1
                    break
                except:
                    continue
            elif j == 1:
                selected_buttons(hardness, [m_x, m_y], 'difficulty')
                try:
                    print(difficulty)
                    j += 1
                    wrong_guesses += 1
                    break
                except:
                    continue
            elif wrong_guesses == 11 or p.is_guessed():
                selected_buttons(replay, [m_x, m_y], 'replay_choice')
                try:
                    print(replay_choice)
                    if replay_choice == 'Yes':
                        j = 0
                        wrong_guesses = 0

                    else:
                        running = False
                    break
                except:
                    continue
        if event.type == pygame.KEYDOWN:
            guess = event.unicode
            success = p.make_guess(guess)
            guessed_letters.append(guess)
            disp_phrase = p.display_phrase()
            if not success:
                wrong_guesses += 1
            break
    pygame.display.update()
    screen.fill(white)

