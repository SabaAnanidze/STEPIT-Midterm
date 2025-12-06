import json  # JSON ფორმატთან სამუშაოდ (მონაცემების შენახვა/წაკითხვა)
import os  # ოპერაციული სისტემის ფუნქციებისთვის

# ფაილის სახელები
USERS_FILE = "users_data.txt"
BLOCKED_FILE = "blocked_accounts.txt"


def load_users(): #ფუნქცია კითხულობს users_data.txt ფაილიდან მომხმარებლების მონაცემებს და აბრუნებს tuple-ების სიას: [(account, pin, balance), ...]
    if os.path.exists(USERS_FILE):
        try: ## ფაილის გახსნა კითხვის რეჟიმში, UTF-8 ენკოდინგით (ქართული ასოებისთვის)
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f) # # JSON ფორმატიდან Python list-ად გარდაქმნა
                # JSON-დან tuple-ებად გარდაქმნა, რადგან tuple უფრო უსაფრთხოა და არ იცვლება
                return [tuple(user) for user in data]
        except:
            print("შეცდომა მონაცემების ჩატვირთვისას. იყენებს ნაგულისხმევ მონაცემებს.")

    # თუ ფაილი არ არსებობს, დააბრუნე ნაგულისხმევი მონაცემები, თავის დაზღვევის მიზნით
    return [
        ("1111 1111 1111 1111", "1111", 1000),
        ("2222 2222 2222 2222", "2222", 2500),
        ("3333 3333 3333 3333", "3333", 1500),
        ("4444 4444 4444 4444", "4444", 3000),
        ("5555 5555 5555 5555", "5555", 500),
        ("6666 6666 6666 6666", "6666", 4500),
        ("7777 7777 7777 7777", "7777", 1200),
        ("8888 8888 8888 8888", "8888", 800),
    ]


def save_users(users):
    #ფუნქცია ინახავს მომხმარებლების მონაცემებს users_data.txt ფაილში JSON ფორმატში, ლამაზად დაფორმატებული (indent=4)
    try:
        # ფაილის გახსნა ჩაწერის რეჟიმში
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            # tuple-ები list-ებად გარდაქმნა JSON-ისთვის რადგან ჯეისონი ტაპლებს არ იცნობს
            users_list = [list(user) for user in users]
            # ensure_ascii=False - რომ ქართული ასოები \u1234 ფორმატში არ გადაიქცეს
            # indent=4 - ლამაზი ფორმატირება 4 სივრცით
            json.dump(users_list, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"შეცდომა მონაცემების შენახვისას: {e}")
        return False


def load_blocked_accounts():
    if os.path.exists(BLOCKED_FILE):
        try:
            with open(BLOCKED_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []


def save_blocked_accounts(blocked_accounts):
    try:
        with open(BLOCKED_FILE, 'w', encoding='utf-8') as f:
            json.dump(blocked_accounts, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"შეცდომა დაბლოკილი ანგარიშების შენახვისას: {e}")
        return False


# მონაცემების ჩატვირთვა ფაილებიდან
users = load_users() ## ყველა მომხმარებლის ჩატვირთვა
blocked_accounts = load_blocked_accounts() # დაბლოკილი ანგარიშების ჩატვირთვა


class ATM:
    def __init__(self, account_number, balance, user_index):
        self.account_number = account_number  # ანგარიშის ნომერი
        self.balance = balance  # მიმდინარე ბალანსი
        self.user_index = user_index  # მომხმარებლის ინდექსი users სიაში
        self.dollar_rate = 2.70
        self.euro_rate = 3.15

    def update_balance(self):
        """ბალანსის განახლება ფაილში"""
        global users
        users[self.user_index] = (
            users[self.user_index][0],  # # ანგარიშის ნომერი
            users[self.user_index][1],  # pin_code
            self.balance  # განახლებული balance
        )
        # განახლებული მონაცემების ფაილში შენახვა
        save_users(users)

    def check_balance_gel(self, language="geo"):
        if language == "geo":
            print(f"{self.balance:.2f} ლარი")
        else:
            print(f"{self.balance:.2f} GEL")

    def check_balance_usd(self, language="geo"):
        print(f"{self.balance / self.dollar_rate:.2f} $")

    def check_balance_eur(self, language="geo"):
        print(f"{self.balance / self.euro_rate:.2f} €")

    def withdraw(self, amount, currency, language="geo"):
        """
              თანხის გატანის მთავარი მეთოდი
              amount: გამოსატანი თანხის რაოდენობა
              currency: "1" - ლარი, "2" - დოლარი, "3" - ევრო
              language: "geo" - ქართული
              """
        if currency == "1":  # GEL
            # პირველ რიგში ვამოწმებთ ბალანსს
            if amount > self.balance:
                if language == "geo":
                    return False, f"არასაკმარისი ბალანსი! თქვენი ბალანსია {self.balance:.2f} ლარი"
                else:
                    return False, f"Insufficient balance! Your balance is {self.balance:.2f} GEL"

            # შემდეგ ვამოწმებთ კუპიურის ვალიდურობას
            if amount % 10 != 0 and amount % 10 != 5 and amount != int:
                if language == "geo":
                    return False, "მსგავსი კუპიურა არ არსებობს! ხელმისაწვდომი კუპიურებია: 5, 10, 20, 50, 100 ₾"
                else:
                    return False, "There is no such banknote! Available banknotes: 5, 10, 20, 50, 100 ₾"

            self.balance -= amount
            self.update_balance()  # ბალანსის შენახვა
            if language == "geo":
                return True, f"თქვენ გამოიტანეთ {amount} ლარი. დარჩენილი ბალანსი: {self.balance:.2f} ლარი"
            else:
                return True, f"You withdrew {amount} GEL. Remaining balance: {self.balance:.2f} GEL"

        elif currency == "2":  # USD
            gel_amount = amount * self.dollar_rate

            # პირველ რიგში ვამოწმებთ ბალანსს
            if gel_amount > self.balance:
                if language == "geo":
                    return False, f"არასაკმარისი ბალანსი! თქვენი ბალანსია {self.balance:.2f} ლარი ({self.balance / self.dollar_rate:.2f} $)"
                else:
                    return False, f"Insufficient balance! Your balance is {self.balance:.2f} GEL ({self.balance / self.dollar_rate:.2f} $)"

            # შემდეგ ვამოწმებთ კუპიურის ვალიდურობას
            if amount % 1 != 0:
                if language == "geo":
                    return False, "მსგავსი კუპიურა არ არსებობს! ხელმისაწვდომი კუპიურებია: 1, 2, 5, 10, 20, 50, 100 $"
                else:
                    return False, "There is no such banknote! Available banknotes: 1, 2, 5, 10, 20, 50, 100 $"

            self.balance -= gel_amount
            self.update_balance()  # ბალანსის შენახვა
            if language == "geo":
                return True, f"თქვენ გამოიტანეთ {amount} $. დარჩენილი ბალანსი: {self.balance:.2f} ლარი ({self.balance / self.dollar_rate:.2f} $)"
            else:
                return True, f"You withdrew {amount} $. Remaining balance: {self.balance:.2f} GEL ({self.balance / self.dollar_rate:.2f} $)"

        elif currency == "3":  # EUR
            gel_amount = amount * self.euro_rate

            # პირველ რიგში ვამოწმებთ ბალანსს
            if gel_amount > self.balance:
                if language == "geo":
                    return False, f"არასაკმარისი ბალანსი! თქვენი ბალანსია {self.balance:.2f} ლარი ({self.balance / self.euro_rate:.2f} €)"
                else:
                    return False, f"Insufficient balance! Your balance is {self.balance:.2f} GEL ({self.balance / self.euro_rate:.2f} €)"

            # შემდეგ ვამოწმებთ კუპიურის ვალიდურობას
            if amount % 10 != 0 and amount % 10 != 5 and amount != int:
                if language == "geo":
                    return False, "მსგავსი კუპიურა არ არსებობს! ხელმისაწვდომი კუპიურებია: 5, 10, 20, 50, 100 €"
                else:
                    return False, "There is no such banknote! Available banknotes: 5, 10, 20, 50, 100 €"

            self.balance -= gel_amount
            self.update_balance()  # ბალანსის შენახვა
            if language == "geo":
                return True, f"თქვენ გამოიტანეთ {amount} €. დარჩენილი ბალანსი: {self.balance:.2f} ლარი ({self.balance / self.euro_rate:.2f} €)"
            else:
                return True, f"You withdrew {amount} €. Remaining balance: {self.balance:.2f} GEL ({self.balance / self.euro_rate:.2f} €)"


def authenticate_user():
    global users  # users-ის განახლებისთვის
    attempts = 3

    while attempts > 0:
        print("\n" + "-" * 50)
        print("კეთილი იყოს თქვენი მობრძანება!")
        print("Welcome!")
        print("-" * 50)

        account_number = input("\nშეიყვანეთ ბარათის მონაცემები (16 ციფრი) / Enter card details (16 digits): ")

        # შემოწმება დაბლოკილია თუ არა ანგარიში
        if account_number in blocked_accounts:
            print("\n თქვენი ანგარიში დაბლოკილია! გთხოვთ დაუკავშირდეთ ბანკს.")
            print(" Your account is blocked! Please contact the bank.")
            return None

        pin_code = input("შეიყვანეთ PIN კოდი: ")

        # შემოწმება მონაცემების სიაში
        for i, user in enumerate(users):
            if user[0] == account_number and user[1] == pin_code:
                print("\nავტორიზაცია წარმატებით გაიარა!")
                return ATM(user[0], user[2], i)  # ვაგზავნით user_index-ს

        attempts -= 1

        if attempts > 0:
            print(f"\nარასწორი ანგარიშის ნომერი ან PIN კოდი! / Incorrect account number or PIN code!")
            print(f"დარჩენილი მცდელობები: {attempts} / Remaining attempts: {attempts}")
        else:
            print("\nთქვენ ამოიწურეთ ყველა მცდელობა! / You have used all attempts!")
            print(
                "თქვენი ანგარიში დაიბლოკა უსაფრთხოების მიზნებისთვის. / Your account has been blocked for security purposes.")
            blocked_accounts.append(account_number) # # ანგარიშის დამატება დაბლოკილების სიაში
            save_blocked_accounts(blocked_accounts)  # დაბლოკილი ანგარიშის შენახვა
            return None

    return None


def main():  # პროგრამის მთავარი ფუნქცია რომელიც აკონტროლებს მთელ პროგრამის ნაკადს
    # ავტორიზაცია
    atm = authenticate_user()

    # თუ ავტორიზაცია ვერ მოხერხდა (None დაბრუნდა)
    if atm is None:
        print("\nგმადლობთ! ნახვამდის!")
        print("Thank you! Goodbye!")
        return

    continue_operation = True

    while continue_operation:
        language = get_language(atm)
        print(language)

        print("\nგსურთ სხვა ოპერაციის შესრულება? / Do you want to perform another operation?")
        choice = input("კი/არა (yes/no): ").lower()
        if choice not in ["კი", "yes"]:
            print("\nმადლობა! ნახვამდის!")
            print("Thank you! Goodbye!")
            continue_operation = False


def get_language(atm):
    print("\nაირჩიეთ რა ენაზე გსურთ ოპერაციის გაგრძელება")
    print("Select the language in which you want to continue the operation")
    ena = input("ქართული | English: ").lower()

    if ena == "english":
        return eng_atm(atm)
    elif ena == "ქართული":
        return geo_atm(atm)
    else:
        return "შეიყვანე სწორი სიტყვა / Enter a valid word"


def geo_atm(atm):
    print("\nაირჩიე ოპერაცია")
    print("1. ბალანსის შემოწმება")
    print("2. თანხის გატანა")
    choice1 = input("აირჩიე ოპერაცია: ")

    if choice1 == "1":
        return check_balance_geo(atm)
    elif choice1 == "2":
        return withdraw_geo(atm)
    else:
        return "მსგავსი ოპერაცია არ არსებობს"


def check_balance_geo(atm):
    print("\n1. შეამოწმე ბალანსი ლარში")
    print("2. შეამოწმე ბალანსი დოლარში")
    print("3. შეამოწმე ბალანსი ევროში")
    choice_balance = input("აირჩიე ოპერაცია: ")

    if choice_balance == "1":
        atm.check_balance_gel("geo")
    elif choice_balance == "2":
        atm.check_balance_usd("geo")
    elif choice_balance == "3":
        atm.check_balance_eur("geo")
    else:
        return "არასწორი არჩევანი"

    return "ოპერაცია წარმატებით დასრულდა"


def eng_atm(atm):
    print("\nSelect an operation:")
    print("1. Check balance")
    print("2. Withdraw funds")
    choice1 = input("Select an operation: ")

    if choice1 == "1":
        return check_balance_eng(atm)
    elif choice1 == "2":
        return withdraw_eng(atm)
    else:
        return "Invalid operation"


def check_balance_eng(atm):
    print("\n1. Check balance in GEL")
    print("2. Check balance in USD")
    print("3. Check balance in EUR")
    choice_balance = input("Select an operation: ")

    if choice_balance == "1":
        atm.check_balance_gel("eng")
    elif choice_balance == "2":
        atm.check_balance_usd("eng")
    elif choice_balance == "3":
        atm.check_balance_eur("eng")
    else:
        return "Invalid choice"

    return "Operation completed successfully"


def withdraw_geo(atm):
    print("\nაირჩიე ვალუტა:")
    print("1. ლარი (GEL)")
    print("2. დოლარი (USD)")
    print("3. ევრო (EUR)")
    currency_choice = input("აირჩიე ვალუტა: ")

    if currency_choice not in ["1", "2", "3"]:
        return "არასწორი ვალუტა"

    try:
        amount = float(input("შეიყვანეთ თანხის რაოდენობა: "))
        if amount <= 0:  #მათემატიკაში რომ არ აგვერიოს და უარყოფითი რიცხვით თანხა არ შევიტანოთ
            return "თანხა უნდა იყოს დადებითი რიცხვი"

        success, message = atm.withdraw(amount, currency_choice, "geo")
        print(f"\n{message}")

        if success:
            return "ოპერაცია წარმატებით დასრულდა"
        else:
            return "ოპერაცია ვერ შესრულდა"
    except ValueError:
        return "გთხოვთ შეიყვანოთ სწორი რიცხვი"


def withdraw_eng(atm):
    print("\nSelect currency:")
    print("1. GEL")
    print("2. USD")
    print("3. EUR")
    currency_choice = input("Select currency: ")

    if currency_choice not in ["1", "2", "3"]:
        return "Invalid currency"

    try:
        amount = float(input("Enter amount: "))
        if amount <= 0:
            return "Amount must be positive"

        success, message = atm.withdraw(amount, currency_choice, "eng")
        print(f"\n{message}")

        if success:
            return "Operation completed successfully"
        else:
            return "Operation failed"
    except ValueError:
        return "Please enter a valid number"


if __name__ == '__main__':
    main()