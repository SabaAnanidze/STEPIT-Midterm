class Calculator: #ვქმნით კლასს Calculator რომელიც შეიცავს ყველა საჭირო მეთოდს
    def __init__(self):
        self.history = []

    def add(self, a, b): #ორი რიცხვის ჯამი
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result

    def subtract(self, a, b): #ორი რიცხვის სხვაობა
        result = a - b
        self.history.append(f"{a} - {b} = {result}")
        return result

    def multiply(self, a, b): #ორი რიცხვის ნამრავლი
        result = a * b
        self.history.append(f"{a} * {b} = {result}")
        return result

    def divide(self, a, b): #ორი რიცხვის განაყოფი
        if b == 0:
            return None
        result = a / b
        self.history.append(f"{a} / {b} = {result}")
        return result

    def sqrt(self, a): #კვადრატული ფესვი ერთი რიცხვიდან
        if a < 0:
            return None
        result = a ** 0.5
        self.history.append(f"√{a} = {result}")
        return result

    def square(self, a): #ერთი რიცხვის კვადრატი
        result = a ** 2
        self.history.append(f"{a}^2 = {result}")
        return result

    def power(self, a, b): #რიცხვის აყვანა კონკრეტულ ხარისხში
        result = a ** b
        self.history.append(f"{a}^{b} = {result}")
        return result

    def get_history(self): #ჩვენს მიერ ჩატარებული ოპერაციების ისტორიის ნახვა
        for _ in range(len(self.history)):
            return "\n".join(self.history)


def input_number(prompt): #შეყვანილი რიცხვი უნდა იყოს ან ფლოუტი ან ინტეჯერი.
    while True:
        text = input(prompt).strip()
        try:
            value = float(text)
            return value
        except ValueError:
            print("Invalid number, please enter a valid one.")


def print_menu(): #საწყისი მენიუ რომელიც მეორდება და არ იცვლება სანამ მომხმარებელი არ გადაწყვეტს გამოსვლას
    print("\n=== CALCULATOR ===")
    print("1. Add (+)")
    print("2. Subtract (-)")
    print("3. Multiply (*)")
    print("4. Divide (/)")
    print("5. Square root (√x)")
    print("6. Square (x^2)")
    print("7. Power (x^y)")
    print("8. Show history")
    print("0. Exit")


def show_history(calc): #კლასმეთოდის გამოყენება და ოპერაციების ისტორიის იუზერისთვის ჩვენება
    ops = calc.get_history()

    if len(ops) == 0: #თუ არც ერთი ოპერაცია არ არის ჩატარებული, ისტორია ცარიელია
        print("History is empty.")
        return

    print("\nHistory:")
    print(ops)



def main(): #მთავარი ფუნქცია რომელიც აკონტროლებს პროგრამის მუშაობას იუზერის მოქმედების შესაბამისად.
    calc = Calculator()

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == "0":
            print("Goodbye!")
            break

        elif choice in ["1", "2", "3", "4", "7"]: #ოპერაციები სადაც საჭიროა ორი ინფუთი მოვითხოვოთ,
            # და ოპერაციისთვის ორი რიცხვი გამოვიყენოთ
            first = input_number("Enter first number: ")
            second = input_number("Enter second number: ")

            if choice == "1":
                print("Result:", calc.add(first, second))

            elif choice == "2":
                print("Result:", calc.subtract(first, second))

            elif choice == "3":
                print("Result:", calc.multiply(first, second))

            elif choice == "4": 
                result = calc.divide(first, second)
                if second == 0: # დაუშვებელია ნულზე გაყოფა
                    print("Error: cannot divide by zero.") #შეგვეძლო ასევე raise ZerodivisionError
                else:
                    print("Result:", result)

            elif choice == "7":
                print("Result:", calc.power(first, second))

        elif choice in ["5", "6"]:
            number = input_number("Enter number: ")

            if choice == "5":
                result = calc.sqrt(number)
                if number == -1:
                    print("Result: i") #თუ რიცხვი არის -1, კვადრატული ფესვი იქნება i
                elif number < 0: #ვერ ამოვიყვანთ კვადრატულ ფესვს უარყოფითი რიცხვისგან
                    print("Error: cannot take square root of a negative number.")
                else:
                    print("Result:", result)

            elif choice == "6":
                print("Result:", calc.square(number))

        elif choice == "8":
            show_history(calc)

        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    main()

