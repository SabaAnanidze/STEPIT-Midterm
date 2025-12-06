import random  # შემოგვყავს მოდული რომელსაც შემდგომში გამოვიყენებთ შემთხვევითი სიტყვების ასარჩევად


class Hangman:  # ვქმნით თამაშის კლასს
    def __init__(self, secret_word):
        self.secret_word = secret_word.upper()
        self.guessed_letters = set()
        self.wrong_guesses = 0  # ვითვლით არასწორ ცდებს
        self.max_wrong_guesses = 8  # მაქსიმუმ 8 არასწორი ცდა

    def guess(self, letter):  # მეთოდი რომელიც იღებს ერთ ასოს და აბრუნებს True თუ ასო სწორია,
        # False თუ არასწორია და
        # None თუ უშუალოდ ინფუთი არ აკმაყოფილებს მოთხოვნებს

        letter = letter.upper()

        if len(letter) != 1:
            return None

        if not letter.isalpha():
            return None

        if letter in self.guessed_letters: #უკვე გამოიყეა ეს ასო.
            return "repeated"

        self.guessed_letters.add(letter) #გამოყენებული ასოების ლისტში დაამატე შემდეგი გამოყენებული ასო

        if letter in self.secret_word:
            return True
        else:
            return False

    def display_word(self):  # ეს მეთოდი აჩვენებს დამალულ სიტყვას, სადაც მხოლოდ გამოცნობილი ასოები ჩანს.
        result = ""
        for character in self.secret_word:
            if character in self.guessed_letters:
                result = result + character + " "
            else:
                result = result + "_ "
        return result.strip()

    def is_won(self):  # მეთოდი რომელიც აბრუნებს True თუ იუზერმა მოიგო თამაში
        for character in self.secret_word:
            if character not in self.guessed_letters:  # თუ გვაქვს ყველა ასო, რომელიც საჭიროა სიტყვის ასაწყობად, თამაში მოგებულია
                return False
        return True
####################################################
    def is_lost(self):  # მეთოდი რომელიც აბრუნებს True თუ მოთამაშემ ამოწურა ყველა ცდა
        return self.wrong_guesses >= self.max_wrong_guesses

    def remaining_guesses(self):  # მეთოდი რომელიც აბრუნებს დარჩენილ ცდების რაოდენობას
        return self.max_wrong_guesses - self.wrong_guesses
##################################################

def choose_category():  # მეთოდი კონსოლისთვის, რითაც იუზერს შეუძლია აირჩიოს კატეგორია, ის აბრუნებს კატეგორიის ნომერს
    # რომელსაც შემდგომში ვაწვდით შემდეგ ფუნქცია
    print("Choose a category:")
    print("1. Countries")
    print("2. Sports")
    print("3. Animals")
    print("4. Professions")

    while True:
        user_choice = input("Enter 1, 2, 3, or 4: ").strip()

        if user_choice in ["1", "2", "3", "4"]:
            return int(user_choice)  # აბრუნებს ნომერს როგორც ინტეჯერს
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")


def get_word_list(category_number):  # წინა ფუნქციიდან ვიღებთ ციფრს და ვაბრუნებთ შესაბამის სიტყვების სიას/კატეგორიას
    # თითოეულ კატეგორიაში 20 სიტყვაა, საიდანაც რენდომაიზერი აირჩევს შემდგომში ერთს.
    if category_number == 1:
        return [
            "georgia", "germany", "france", "italy", "spain",
            "brazil", "argentina", "canada", "japan", "china",
            "india", "turkey", "norway", "sweden", "finland",
            "denmark", "mexico", "egypt", "greece", "portugal"
        ]

    if category_number == 2:
        return [
            "football", "basketball", "tennis", "swimming", "boxing",
            "running", "cycling", "golf", "volleyball", "baseball",
            "rugby", "wrestling", "skiing", "snowboarding", "surfing",
            "taekwondo", "karate", "badminton", "rowing", "fencing"
        ]

    if category_number == 3:
        return [
            "elephant", "tiger", "lion", "giraffe", "monkey",
            "zebra", "kangaroo", "bear", "wolf", "fox",
            "rabbit", "horse", "dolphin", "shark", "penguin",
            "eagle", "owl", "frog", "snake", "panda"
        ]

    if category_number == 4:
        return [
            "doctor", "nurse", "teacher", "engineer", "artist",
            "chef", "police", "lawyer", "pilot", "dentist",
            "farmer", "architect", "mechanic", "scientist", "programmer",
            "musician", "actor", "driver", "journalist", "plumber"
        ]

    return []


def build_guessed_text(guessed_letters):  # ეს ფუნქცია ყველა ცდის შემდგომ დააბრუნებს გამოყენებული ასოების ლისტს
    # რომელიც იქნება ანბანის მიხედვით დალაგებული.
    if not guessed_letters:
        return "None"

    sorted_letters = sorted(list(guessed_letters))
    text = ""
    i = 0
    while i < len(sorted_letters):
        text += sorted_letters[i] + " "
        i += 1
    return text.strip()


def main():  # მთავარი ფუნქცია რომელიც აკონტროლებს თამაშის ლოგიკას და იუზერთან ინტერაქციას კონსოლიდან
    category_number = choose_category()
    word_list = get_word_list(category_number)
    secret_word = random.choice(word_list)
    game = Hangman(secret_word)

    print("\nWelcome to Hangman!")
    print(f"You have {game.max_wrong_guesses} attempts to guess the word.\n")

    while not game.is_won() and not game.is_lost():  # სანამ კლასმეთოდი is_won() არ დააბრუნებს true, თამაში გრძელდება
        print("\nWord:", game.display_word())
        print("Guessed letters:", build_guessed_text(game.guessed_letters))
        print(f"Remaining attempts: {game.remaining_guesses()}")

        guess_input = input("Guess a letter: ").strip()
        if guess_input == "":
            print("Please enter a letter.")
            continue


        letter = guess_input[0]  # ვიზღვევთ თავს რათა კლასის მეთოდს მხოლოდ ერთი ასო მივაწოდოთ
        result = game.guess(letter)

        if result is True:
            print("Correct!")
        elif result is False:
            game.wrong_guesses += 1  # ვზრდით არასწორი ცდების რაოდენობას
            print(f"Wrong letter. Attempts remaining: {game.remaining_guesses()}")
        elif result == "repeated":    #<-------------
            print("This letter has already been used, try a new one.")
        else:
            print("Invalid or repeated guess.")

    if game.is_won():
        print("\nYou guessed the word:", game.secret_word)
        print("You won!")
    else:
        print("\nGame Over! You've run out of attempts.")
        print("The word was:", game.secret_word)


if __name__ == "__main__":
    main()