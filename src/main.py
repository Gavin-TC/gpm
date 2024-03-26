import sys
import os
import random
import csv

file_name: str = 'pswd.csv'
os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

def main() -> None:
    if len(sys.argv) < 2:
        print("Use: [gpm -h] for help.")
        return
    else:
        match sys.argv[1]:
            case "-c":  # create/change passwords flag
                if len(sys.argv) < 3:
                    print("[ERROR] Missing name argument!")
                    print("To create a password use: [gpm -c \"password_name\"]")
                    print()
                    return
                create_password(sys.argv[2])
                print()
            
            case "-a":  # add existing password flag
                if len(sys.argv) < 4:
                    print("[ERROR] Missing an argument!")
                    print("To add a password use: [gpm -a \"password_name\" \"password\"]")
                    print()
                    return
                add_password(sys.argv[2], sys.argv[3])
                print()
            
            case "-r":  # remove password flag
                if len(sys.argv) < 3:
                    print("[ERROR] Missing name argument!")
                    print("To remove a password use: [gpm -r \"password_name\"]")
                    print()
                    return
                remove_password(sys.argv[2])
                print()
                
            case "-l":  # list passwords flag
                try:
                    with open(file_name, 'r') as file:
                        reader = csv.reader(file)
                        rows = list(reader)

                        if len(rows) > 0:
                            for row in rows:
                                print(row[0] + ": " + row[1])
                        else:
                            print("[ERROR] There aren't any passwords stored!")
                            print()
                            return
                except Exception as e:
                    print("[ERROR] There was an error when reading the file!: \"" + str(e) + "\"")
                print()
            
            case "-h":  # help flag
                print("Use the \"-c\" flag to create/change a current password.")
                print("Use the \"-a\" flag to add an external password.")
                print("Use the \"-r\" flag to remove an existing password.")
                print("Use the \"-l\" flag to list all existing passwords.")
                print("Use \"password_name\" argument to get the password associated with that name. This will also copy the password to your clipboard.")
                print("Ctrl + C to cancel at any point during password creation.")
                print()

            case _:  # retrieve password 'flag'
                get_password(sys.argv[1])
                print()

# -c FLAG
def create_password(pass_name: str) -> None:
    satisfied: bool = False
    password: str = ""

    while not satisfied:
        length: int = abs(max(1, min(int(input("LENGTH?: ").lower()), 25)))
        numbers:  bool = True if input("NUMBERS?: [Y/n]: ").lower() == 'y' else False
        letters:  bool = True if input("LETTERS?: [Y/n]: ").lower() == 'y' else False
        specials: bool = True if input("SPECIAL?: [Y/n]: ").lower() == 'y' else False

        if letters == False and numbers == False and specials == False:
            print("[ERROR] You have to have atleast 1 type of character in your password!")
            continue

        password = generate_password(length, numbers, letters, specials)

        print("\nYour password is: \"" + password + "\"")
        satisfied = False if input("Remake? [Y/n]: ").lower() == 'y' else True
    
    store_password(sys.argv[2], password)


# -a FLAG
def add_password(pass_name: str, password: str) -> None:
    if not exists(pass_name):
        store_password(pass_name, password)
    else:
        print("[ERROR] That password already exists!")
        print()


# -r FLAG
def remove_password(pass_name: str) -> None:
    if exists(pass_name):
        with open(file_name, 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)

        rows = [row for row in rows if row[0] != pass_name]

        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
    else:
        print("[ERROR] That password doesn't exist!")
        print()


# default FLAG
def get_password(pass_name: str) -> None:
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

        for row in rows:
            if row[0] == pass_name:
                print(row[1])
                os.system('echo '+ row[1] + '| clip')  # copy password
                return
    print("[ERROR] That password doesn't exist!")
    print()


def generate_password(length: int, number: bool, letter: bool, special: bool) -> str:
    password: str = ""

    chars_left = length
    parts: int = int(number) + int(letter) + int(special)

    numbers = "1234567890"
    letters = "abcdefghijklmnopqrstuvwxyz"
    specials = "!?@#$%-*_"
    all_chars = numbers + letters + specials

    chosen_numbers = ""
    chosen_letters = ""
    chosen_specials = ""

    if number:
        for x in range(length // parts):
            chars_left -= 1
            chosen_numbers += random.choice(numbers)
    if letter:
        for x in range(length // parts):
            chars_left -= 1
            chosen_letters += random.choice(letters)
    if special:
        for x in range(length // parts):
            chars_left -= 1
            chosen_specials += random.choice(specials)
    
    if chars_left > 0:
        for x in range(chars_left):
            if   numbers:   chosen_numbers += random.choice(numbers)
            elif letters:   chosen_letters += random.choice(letters)
            elif specials:  chosen_special += random.choice(specials)

    password = chosen_letters + chosen_numbers + chosen_specials

    # shuffle password length times, for fun
    for x in range(length):
        password_arr = list(password)
        random.shuffle(password_arr)
        password = ''.join(password_arr)

    return password


def store_password(name, password) -> None:
    if exists(name):
        try:
            with open(file_name, 'r') as file:
                reader = csv.reader(file)
                rows = list(reader)

            with open(file_name, 'w', newline='') as file:
                writer = csv.writer(file)
                for row in rows:
                    if row[0] == name:
                        row[1] = password
                    writer.writerow(row)
        except Exception as e:
            print("[ERROR] There was a problem reading the file!: \"" + str(e) + "\"")
            print()
    else:
        with open(file_name, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, password])


def exists(name) -> bool:
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        return any(row[0] == name for row in reader)
        

if __name__ == "__main__":
    main()
