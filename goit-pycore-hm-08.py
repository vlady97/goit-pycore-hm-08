import pickle
from collections import UserDict

def save_data(book, filename="addressbook.pkl"):
         with open(filename, "wb") as f:
             pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
       try:
          with open(filename, "rb") as f:
            return pickle.load(f)
       except FileNotFoundError:
           return AddressBook()

def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        else:
            print("Invalid command.")

    save_data(book)

if __name__ == "__main__":
    main()

class AddressBook(UserDict):
    
     def add_record(self, record):
           if not isinstance(record, Record):
                raise ValueError()
           self.data[record.name.value] = record
     
     def find(self, name: str) -> Record:
            return self.data.get(name)
     
     def delete(self, name:str):
              if name in self.data:
                   del self.data[name]

     def get_upcoming_birthdays(self, days=7):
       upcoming_birthdays = []
       today = date.today()
       for record in self.data.values():
        if record.birthday:
            birthday_this_year = record.birthday.replace(year=today.year)
        
        if birthday_this_year.date < today:
            birthday_this_year = birthday_this_year.value.replace(year=today.year + 1)
        
        birthday_this_year = self.adjust_for_weekend(birthday_this_year)
        if 0 <= (birthday_this_year.date() - today).days <= days:
            congratulation_date_str = self.date_to_string(birthday_this_year)
            upcoming_birthdays.append({
                "name": record.name, 
                "congratulation_date": congratulation_date_str
                })
       return upcoming_birthdays
     
     @input_error
     def add_birthday(args, book):
         name, date_str = args
         record = book.get(name)
         if not record:
             return f'No contact found'
         try:
             record.add_birthday(date_str)
             return f'Birthday for {name}:{date_str} added'
         except ValueError as e:
             return str(e)
    
     @input_error
     def show_birthday(args, book):
         name = args[0]
         record = book.find(name)
         if not record:
             return f'No contact found'
         if record.birthday:
             return f'{name}´s birday is {record.birthday}'
         else:
             return f'{name} bithday was not found'

     @input_error
     def birthdays(args, book):
         upcoming_birthdays = book.get_upcoming_birthdays()
         if not upcoming_birthdays:
             return f'No upcoming birthdays'
         result = "Upcoming birthdays in the next week:\n"
         return result