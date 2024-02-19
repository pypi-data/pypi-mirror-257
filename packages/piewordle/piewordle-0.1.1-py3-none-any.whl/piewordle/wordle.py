import argparse
import random
import sys
import os
from datetime import datetime as dt

from piewordle.util.data import WordleData, ANSI, ALPHABET
from piewordle.util.dictionary import words_en, words_de
from piewordle.util.thread import RepeatedTimer
from piewordle import __version__, __sysversion__, __author__

WD = WordleData(os.get_terminal_size())


def print_version() -> None:
    working_dir = os.path.dirname(os.path.realpath(__file__))
    piewordle_version = f"PieWordle {__version__} - from {working_dir}\n"
    version_message = '\n'
    version_message += '-' * len(piewordle_version) + '\n'
    version_message += piewordle_version
    version_message += '-' * len(piewordle_version) + '\n'
    version_message += '\n'
    version_message += f"Built with: \tPython {__sysversion__}\n"  # sys.version
    try:
        time_stamp = dt.fromtimestamp(os.path.getctime(os.path.realpath(__file__)))
        version_message += f"Install time: \t{time_stamp}\n"
    except OSError:
        version_message += 'Install time: \t-\n'
    version_message += f"Author: \t{__author__}\n"
    print(version_message)  

def println(*args, end='', **kwargs) -> None:
    print(*args, **kwargs, end=end, flush=True)

def print_guess(wordle: str, guess: str, guess_count: int, wordle_length: int) -> None:
    char_occurence = {letter: 0 for letter in set(wordle)}
    guess_ = list(guess)
    # color guess:
    for i in range(wordle_length):
        if guess_[i] not in wordle:
            WD.guessed[guess_[i]] = f"{ANSI.COLOR_DARK}{guess_[i]}{ANSI.RESET}"
        elif guess_[i] == wordle[i]:
            char_occurence[guess_[i]] += 1
            WD.guessed[guess_[i]] = f"{ANSI.COLOR_GREEN}{guess_[i]}{ANSI.RESET}"
            guess_[i] = WD.guessed[guess_[i]]
    for i in range(wordle_length):
        if guess_[i] in wordle and guess_[i] != wordle[i]:
            char_occurence[guess_[i]] += 1
            if char_occurence[guess_[i]] <= wordle.count(guess_[i]):
                if WD.guessed[guess_[i]] == guess_[i]: # only make it yellow if it is not green
                    WD.guessed[guess_[i]] = f"{ANSI.COLOR_YELLOW}{guess_[i]}{ANSI.RESET}"
                guess_[i] = f"{ANSI.COLOR_YELLOW}{guess_[i]}{ANSI.RESET}"

    # move to position of guess_count's guess
    println(ANSI.XY_POS % (4+2*guess_count, (WD.t_width-(2*wordle_length))//2 + 1))
    println(' '.join(guess_)) # print colored guess

def print_kb() -> None:
    println(ANSI.XY_POS % (WD.t_height-7, 0)) # move to display keyboard line
    split_alphabet = [(0,10), (10,19), (19,26)]
    if WD.german_words: # append 'üöä' if in german keyboard
        split_alphabet.append((26,29))
    for f, t in split_alphabet:
        println(' '.join([WD.guessed[c] for c in ALPHABET[f:t]]), end='\n')

def reset_msg() -> None:
    println(ANSI.XY_POS % (WD.t_height-1, 0)) # jump to line before last line
    println(ANSI.ERASE_LINE)

def print_msg(msg: str) -> None:
    reset_msg()
    println(msg)

def reset_prompt(wordle_length: int) -> None:
    println(ANSI.XY_POS % (WD.t_height-2, 0)) # move to prompt line
    println(ANSI.ERASE_LINE)
    println('> ')
    println(ANSI.SAVE_POS)
    println(ANSI.UNDERLINE)
    println(' ' * wordle_length)
    println(ANSI.RESET)
    println(ANSI.RESET_POS)

def init(wordle_length: int) -> None:
    println(ANSI.ERASE_SCREEN)
    println(ANSI.START_POS)
    println('-' * ((WD.t_width-6)//2), 'WORDLE',
            '-' * ((WD.t_width-6)//2), sep='') # display header
    println(ANSI.XY_POS % (WD.t_height, 0)) # move to bottom left
    println('-' * WD.t_width) # display bottom line
    x_offset = (WD.t_width-(2*wordle_length))//2 + 1
    for i in range(WD.allowed_guesses):
        println(ANSI.XY_POS % (4+2*i, x_offset)) # move to i'th guess position
        println(' '.join('☐' * wordle_length)) # print placeholder for guesses
    print_kb()
    reset_prompt(wordle_length)

def deinit(event: RepeatedTimer) -> None:
    # clear everything and reset styles
    println(ANSI.ERASE_SCREEN)
    println(ANSI.START_POS)
    println(ANSI.RESET)
    # cancel resize event thread
    event.cancel()

def retry() -> bool:
    reset_prompt(1)
    println(ANSI.UNDERLINE)
    answer = input()[:1]
    println(ANSI.RESET)
    return answer.upper() != 'N'

def get_wordle(daily: bool) -> str:
    if daily: # set a daily seed
        random.seed(int(dt.now().timestamp()//86400)) # 24*60*60 == 86400
    return random.choice(WD.words).upper()

def play_wordle(wordle: str) -> bool:
    wordle_length = len(wordle)
    init(wordle_length)

    input_buffer = ''
    guess_count = 0

    while guess_count < WD.allowed_guesses:
        if WD.screen_resized:
            # if the screen has been resized
            # rerender everything
            WD.screen_resized = False
            init(wordle_length)
            # including the old guesses
            for i, g in enumerate(WD.guess_history):
                print_guess(wordle, g, i, wordle_length)
        reset_prompt(wordle_length)
        println(ANSI.UNDERLINE) # underline prompt
        println(input_buffer) # in case the resize interrupted the prompt
        guess = input() # main prompt
        println(ANSI.RESET) # reset styles (underline)
        if WD.screen_resized:
            # if the resize thread prompted to press enter
            # we buffer the input
            input_buffer = guess
            continue
        guess = input_buffer + guess # in case the buffer was not empty
        input_buffer = ''
        if len(guess) != wordle_length:
            print_msg(f"ERROR: The wordle has {wordle_length} letters!")
            continue
        if guess.lower() not in WD.words and not WD.allow_random:
            print_msg(f"ERROR: Unknown word: {guess}")
            continue
        guess = guess.upper()
        reset_msg() # we reset the errors, because the current guess is valid
        WD.guess_history.append(guess)
        print_guess(wordle, guess, guess_count, wordle_length)
        print_kb()
        if wordle == guess:
            print_msg(f"Congratulations: You found the Wordle: {wordle}! "
                      'Play again? [y]es/[n]o')
            return retry()
        guess_count += 1
    print_msg(f"Sadly you did not find the Wordle! The Wordle was: {wordle}. "
              'Play again? [y]es/[n]o')
    return retry()

def check_terminal_size() -> None:
    width, height = os.get_terminal_size()
    if (width != WD.t_width or height != WD.t_height):
        WD.t_width, WD.t_height = width, height
        WD.screen_resized = True
        # display screen-resize-event message
        println(ANSI.ERASE_SCREEN)
        println(ANSI.START_POS)
        println(ANSI.RESET)
        println('Screen Resize has been detected. Press Enter to rerender the screen.')

def main(argv) -> int:
    # define arguments
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-v','--version', action='store_const', default=False,
                           const=True, dest='Version',
                           help='show the current version.')
    argparser.add_argument('--daily', action='store_const', default=False,
                           const=True, dest='Daily',
                           help='guess the daily wordle.')
    argparser.add_argument('-g', action='store', default=6,
                           metavar='GUESSES', dest='Guesses', type=int,
                           help='define the amount of guesses the player has. default is 6.')
    argparser.add_argument('-?', action='store_const', default=False,
                           const=True, dest='Random',
                           help='allow not existing words.')
    argparser.add_argument('--de', action='store_const', default=False,
                           const=True, dest='DE',
                           help='use german words.')
    argparser.add_argument('-w', action='store', default='',
                           metavar='WORDS', dest='Words', type=str,
                           help="define custom wordle options. Seperator is ';'.")

    parameters = argparser.parse_args(argv[1:])

    # handle arguments
    if getattr(parameters, 'Version'):
        print_version()
        return 0
    daily = getattr(parameters, 'Daily')
    WD.allowed_guesses = getattr(parameters, 'Guesses')
    if WD.allowed_guesses <= 0 or \
        WD.allowed_guesses > (WD.t_height-7)//2:
        print('Error: Invalid value for argument -g')
        print('the screen size might be too small to render')
        return 1
    WD.allow_random = getattr(parameters, 'Random')
    WD.german_words = getattr(parameters, 'DE')
    WD.words = words_de if WD.german_words else words_en
    words = getattr(parameters, 'Words')
    if words:
        WD.words = [word.lower() for word in words.split(';')]
        for wordle_option in WD.words:
            if not wordle_option.isalpha():
                print('Error: Invalid value for argument -w')
                return 2

    if 2*max(map(len, WD.words)) > WD.t_width-40:
        print('Error:')
        print('the screen size might be too small to render')
        return 3

    # init thread to handle screen resize event
    resize_event = RepeatedTimer(1, check_terminal_size)
    resize_event.start()

    try:
        while play_wordle(get_wordle(daily)):
            WD.reset()
    except (KeyboardInterrupt, EOFError):
        pass
    try:
        deinit(resize_event) # interrupts on pypy versions
    except KeyboardInterrupt:
        resize_event.cancel()
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
