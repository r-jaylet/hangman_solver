from time import *
import json

with open("dictionary.json") as f:
    words = json.load(f)


def remove_false(wordPool, letter):
    """
    Remove all words that do not contain the given letter
    """
    for word in wordPool[:]:
        if letter in word:
            wordPool.remove(word)
    return wordPool


def remove_not_similar(wordPool, guess, revealed):
    """
    Remove all words that are not similar to the revealed state of the word
    """
    for word in wordPool[:]:
        for i, _ in enumerate(revealed):
            if revealed[i] == "-":
                if word[i] == guess:
                    wordPool.remove(word)
                    break
            elif revealed[i] != word[i]:
                wordPool.remove(word)
                break
    return wordPool


def getPopularLetter(wordPool, guessedLetters, onlyTable=False):
    """
    return the most popular letter in the given word pool
    """
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    # Create table for letter frequencies
    table = {}
    for letter in alphabet:
        table.update({letter: 0})

    # Count letter appearances
    for letter in alphabet:
        for word in wordPool:
            if letter in word:
                table[letter] += 1

    # Exclude all guessed letters from the table
    for item in list(table.items()):
        if item[0] in guessedLetters:
            table.update({item[0]: -10})

    if onlyTable:
        return table

    # Find the most popular letter among the table
    maxPopularity = -10
    for item in list(table.items()):
        if item[1] > maxPopularity:
            maxPopularity = item[1]
            popularLetter = item[0]

    return popularLetter


def chooseWord():
    word = input("Choose a word to guess: ").lower()
    for key in words:
        if word in words[key]:
            return word
    else:
        print("\nThat word is not in the dictionary")


# Main Game
def hangman(word):
    mistakes = 0
    revealed = []
    guessedLetters = []
    guess = ""

    for letter in word:
        revealed.append("-")

    wordPool = words[str(len(word))]

    done = False
    while not done:
        revealedText = ""
        for letter in revealed:
            revealedText += letter

        if "-" not in revealed:
            done = True  # game won
            print("\nI guess the letter {}!".format(guess))
            print(revealedText)
            print("Total number of mistakes : {} ".format(mistakes))
            input()
            break

        if guess != "":
            print("\nMistakes: ", mistakes)
            print("I guess the letter ", guess)
            print(revealedText)
            print("Number of possible words: {}".format(len(wordPool)))

        guess = getPopularLetter(wordPool, guessedLetters).lower()

        sleep(1)
        correct = False

        for i, _ in enumerate(word):
            if guess == word[i]:
                revealed[i] = guess
                correct = True

        # Update word pool
        if correct:
            wordPool = remove_not_similar(wordPool, guess, revealed)
        else:
            mistakes += 1
            wordPool = remove_false(wordPool, guess)

        guessedLetters.append(guess)

# Initiators
word = chooseWord()
while word is None:
    word = chooseWord()
hangman(word)