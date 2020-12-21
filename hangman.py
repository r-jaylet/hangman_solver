import random


def load_words():
    my_file = open('words.txt', 'r')
    content = my_file.read()
    c_list = content.replace('\n', ' ')  # remove escape sequences
    c_list = c_list.split(' ')  # split according to space character
    my_file.close()
    return c_list


def get_secret_word(words):
    index = random.randint(0, len(words))  # retrieve a random number between 0 and len(words)
    return words[index]


def display_secret_word(secret_word, guessed_letters):
    empty = "_" * len(secret_word)  # initialize blank word
    for i in range(len(secret_word)):
        for j in range(len(guessed_letters)):
            if secret_word[i] == guessed_letters[j]:
                empty = empty[:i] + guessed_letters[j] + empty[i + 1:]  # replace blank letter with guessed letters
    return empty


def guess_word(secret_word, chances):
    guessed_letters = []  # initialize empty guessed letter list
    while chances > 0:  # continue playing until there is no more chances
        print('Number of chances left :', chances)
        letter = input()  # ask for the player's guess

        if len(letter) != 1:
            print('Enter only one letter')
            print(display_secret_word(secret_word, guessed_letters))
            continue  # ask for another letter if there is multiple letters entered

        if letter in guessed_letters:
            print('You already played the letter', letter)
            print(display_secret_word(secret_word, guessed_letters))
            continue  # ask for another letter not tried yet

        guessed_letters.append(letter)  # add in the guessed list the new letter
        for i in range(len(secret_word)):
            if letter == secret_word[i]:
                if display_secret_word(secret_word, guessed_letters) == secret_word:
                    return 1  # game is won as the word is the same as the secret word
                break
        if letter not in secret_word:
            chances -= 1  # if the letter is not in the word, remove a chance and ask for another letter
        print(display_secret_word(secret_word, guessed_letters))
    return -1  # game is lost


if __name__ == "__main__":
    words = load_words()  # loading the words from words.txt file
    chances = 10  # number of chances offered to the player
    play_again = True  # a flag telling is the game is over or not
    print(f'Guess the secret word in {chances} tries')
    while play_again:
        secret_word = get_secret_word(words)  # pull the secret word
        status = guess_word(secret_word, chances)  # ask the player to guess the secret word in while loop statement
        if status == 1:  # the player figured out the secret word
            print('You won!')
        else:  # -1 the player run out of chances
            print('You lost! The word was', secret_word)
        play_again = input('\nDo you want to play again (y/n)? ').lower() == 'y'  # asking the player for another party
    print('Goodbye!')