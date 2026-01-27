word = input("WORD: ")
word_list = list(word)

def get_letter():
    while True:
        letter = input("letter: ")
        if len(letter) != 1:
            print("Must be exactly one character!")
            continue
        if not letter.islower():
            print("Character must be a lowercase letter!")
            continue
        return letter

while True:
    num = int(input("Num: "))
    if num == -1:
        break
    if num < 0 or num >= len(word_list):
        print("Invalid index")
        continue

    letter = get_letter()

    word_list[num] = letter
    word = "".join(word_list)
    print(word)

