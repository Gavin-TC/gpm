import sys
import random
import csv
# from Crypto.Cipher import AES
# from Crypto.Util.Padding import pad, unpad
# from Crypto.Random import get_random_bytes

file_name: str = 'pswd.csv'

def main() -> None:
    if len(sys.argv) < 2:
        return

    match sys.argv[1]:
        case "-c":
            if len(sys.argv) < 3:
                print("[ERROR] Missing name argument!")
                print("To create a password use: gpm -c \"password_name\"")
                return
            create_password(sys.argv[2])
        case "-r":
            if len(sys.argv) < 3:
                print("[ERROR] Missing name argument!")
                print("To replace a password do: 'gpm -r [password_name]'")
                return
            replace_password(sys.argv[2])
        case _:
            get_password(sys.argv[1])


def generate_password(length: int, number: bool, letter: bool, special: bool) -> str:
    password: str = ""

    chars_left = length
    parts: int = int(number) + int(letter) + int(special)

    numbers = "1234567890"
    letters = "abcdefghijklmnopqrstuvwxyz"
    specials = "!?@#$%&*-_"
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
        password = shuffle_password(password)    

    return password


def shuffle_password(password: str) -> str:
    password_arr = list(password)
    random.shuffle(password_arr)
    return ''.join(password_arr)


def get_password(pass_name: str) -> None:
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

        for row in rows:
            if row[0] == pass_name:
                print(row[1])


def create_password(pass_name: str) -> None:
    satisfied: bool = False
    password: str = ""

    while not satisfied:
        length: int = abs(int(max(1, min(ord(input("PASSWORD LENGTH: ").lower()[0]), 25))))
        letters:  bool = True if input("LETTERS?: [Y/n]: ").lower() == 'y' else False
        numbers:  bool = True if input("NUMBERS?: [Y/n]: ").lower() == 'y' else False
        specials: bool = True if input("SPECIAL?: [Y/n]: ").lower() == 'y' else False

        if letters == False and numbers == False and specials == False:
            print("[ERROR] You have to have atleast 1 type of character in your password!")
            continue

        password = generate_password(length, letters, numbers, specials)

        print("\nYour password is: \"" + password + "\"")
        satisfied = False if input("Remake? [Y/n]: ").lower() == 'y' else True
    
    store_password(sys.argv[2], password)


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
            print("[ERROR] There was a problem reading the file!")
            print(e)
    else:
        with open(file_name, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, password])


def exists(name) -> bool:
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        return any(row[0] == name for row in reader)
        

    
def replace_password(pass_name: str) -> None:
    print("Replacing password for", pass_name)


# def encrypt_file(filename, key):
#     data = ''
#     with open(filename, 'r') as file:
#         data = file.read()

#     cipher = AES.new(key, AES.MODE_CBC)
#     ciphertext = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))

#     with open(filename + '.enc', 'wb') as file:
#         file.write(cipher.iv)
#         file.write(ciphertext)


# def decrypt_file(filename, key):
#     with open(filename, 'rb') as file:
#         iv = file.read(16)
#         ciphertext = file.read()

#     cipher = AES.new(key, AES.MODE_CBC, iv=iv)
#     plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

#     with open(filename.replace('.enc', '.dec'), 'w') as file:
#         file.write(plaintext.decode('utf-8'))

# # Usage
# key = get_random_bytes(16)
# encrypt_file('passwords.csv', key)
# decrypt_file('passwords.csv.enc', key)


if __name__ == "__main__":
    main()
