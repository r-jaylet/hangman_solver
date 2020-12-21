from time import *
import math
import json


with open("dictionary.json") as f:
    """
    return json with words from dictionary
    """
    words = json.load(f)


def validWord(word):
    """
    Checks if the given word exists in the dictionary
    """
    for key in words:
        if word in words[key]:
            return True


def setWordPool(length):
    """
    Return a word pool with words with the given length
    """
    return words[str(length)]



def printPossibleWords(wordPool):
    """
    Return all possible words (same length)
    """
    print("Possible words: ", end="")
    if len(wordPool) > 10:
        for word in wordPool:
            print(word, end="")
            if word == wordPool[9]:
                print(" and {} more!".format(len(wordPool) - 10))
                break
            else:
                print(", ", end="")
    else:
        for word in wordPool:
            print(word, end="")
            if word == wordPool[-1]:
                print("")
                break
            else:
                print(", ", end="")


def printWorstWords(wordPool, guessedLetters):
    """
    Print the 3 worst words based on letter popularity
    """
    maxnum = math.inf
    table = getPopularLetter(wordPool, guessedLetters, True)
    updatedTable = {}

    for key in table:
        if table[key] == -10 or table[key] == 0:
            pass
        else:
            updatedTable.update({key: table[key]})

    for key in updatedTable:
        inverse = 1000 / updatedTable[key]
        updatedTable.update({key: inverse})

    # Calculate each word's "badness" value
    worstWords = [("", 0), ("", 0), ("", 0)]
    for word in wordPool[::-1]:
        score = 0
        for key in updatedTable:
            if key in word:
                score += updatedTable[key]

        for index, item in enumerate(worstWords):
            string, value = item
            if score > value:
                worstWords[index] = (word, score)
                break

    print("Worst words: ", end="")
    for index, item in enumerate(worstWords):
        word = item[0]
        print(word, end="")
        if index == 0:
            print(", ", end="")
        elif index == 1:
            print(" and ", end="")
        else:
            print("\n")


## Word pool pruning Methods ##

def falsePrune(wordPool, letter):
    """
    Remove words that do not contain the given letter
    """
    for word in wordPool[:]:
        if letter in word:
            wordPool.remove(word)
    return wordPool


def indexPrune(wordPool, guess, revealed):
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
    Gets the most popular letter in the given word pool
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
    """
    Input a word for the AI to guess
    """
    word = input("\nChoose a word for the AI to guess: ").lower()

    if validWord(word):
        return word
    else:
        print("\nThat word is not in the dictionary!")


def hangman(word):
    mistakes = 0
    revealed = []
    guessedLetters = []
    guess = ""

    for letter in word:
        revealed.append("-")

    wordPool = setWordPool(len(word))

    done = False
    while not done:
        revealedText = ""
        for letter in revealed:
            revealedText += letter

        # Check Win
        if "-" not in revealed:
            done = True
            print("\nI guess the letter {}!".format(guess))
            print(revealedText)
            if mistakes > 1:
                print("The AI guessed the word within {} mistakes!".format(mistakes))
            elif mistakes == 1:
                print("The AI guessed the word only within {} mistake!".format(mistakes))
            else:
                print("The AI guessed the word without mistakes!")

            input()
            break

        if guess != "":
            print("\nMistakes: ", mistakes)
            print("I guess the letter ", guess)
            print(revealedText)
            printPossibleWords(wordPool)
            if len(wordPool) > 3:
                printWorstWords(wordPool, guessedLetters)
        else:
            print("\nI am analyzing the word...")

        guess = getPopularLetter(wordPool, guessedLetters).lower()

        if len(wordPool) > 5:
            sleep(1)
        else:
            sleep(.2)

        correct = False

        for i, _ in enumerate(word):
            if guess == word[i]:
                revealed[i] = guess
                correct = True

        # Update word pool
        if correct:
            wordPool = indexPrune(wordPool, guess, revealed)
        else:
            mistakes += 1
            wordPool = falsePrune(wordPool, guess)

        guessedLetters.append(guess)


word = chooseWord()
while word is None:
    word = chooseWord()
hangman(word)
