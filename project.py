import cowsay
import csv
import os
import pyfiglet
import random
import re
import string
import time
from tabulate import tabulate


def title(message: str, font: str = "standard") -> None:
    """
    Display a title using ASCII art.

    Args:
        message (str): Message to display as a title.
        font (str, optional): Font style. Defaults to "standard".
    """
    print("\n" * 5)
    print(pyfiglet.figlet_format(message, font=font), "\n")  # Display the title using ASCII art.


def menu(info) -> list | str:
    """
    Generate a menu based on the given input.

    Args:
        info (str): Information to generate the menu.

    Returns:
        list|str: Generated menu as a list of strings or an error message.
    """
    match info:
        case "menu":
            menu: list = ["Register", "Login", "Display Account registered", "Quit System"]  # Main menu options.
        case "login":
            menu: list = ["Show passwords", "Account information", "Delete Account", "Quit Account"]  # Account menu options.
        case "password":
            menu: list = [
                "Add password",
                "Modify password",
                "Search password",
                "Delete password",
                "Quit password Interface",
            ]  # Password menu options.
        case _:
            return "Un problème est survenu"  # Return an error message for an invalid menu type.

    return [f"[{menu.index(ele) + 1}] {ele}" for ele in menu]  # Return the menu as a list of formatted strings.


def generate_password() -> str:
    """
    Generate a random password.

    Returns:
        str: Randomly generated password.
    """
    alphabet: str = string.ascii_letters + string.digits + string.punctuation
    pwd_length: int = 15  # Set the desired password length.
    pwd: str = "".join(random.choice(alphabet) for _ in range(pwd_length))  # Generate random characters for the password.
    return pwd


def data_recovery(path: str) -> list:
    """
    Recover data from the CSV file.

    Args:
        path (str): Path to the CSV file.

    Returns:
        list: List of dictionaries containing the data from the CSV file.
    """
    try:
        with open(path, "r") as file:
            reader = csv.DictReader(file)  # Read the CSV file as dictionaries.
            return [row for row in reader]  # Convert the reader object to a list of dictionaries.
    except FileNotFoundError:
        try:
            with open(path, "w"):
                pass
            return data_recovery(path)  # Create the file if not found and recursively call the function.
        except FileNotFoundError:
            os.makedirs("passwords")


def store_csv(information_to_test: list, path: str = "data.csv", modify: bool = False):
    """
    Store information in the CSV file.

    Args:
        information_to_test (list): List of dictionaries containing the information to store.
        path (str, optional): Path to the CSV file. Defaults to "data.csv".
        modify (bool, optional): Indicates if the data is being modified. Defaults to False.

    Returns:
        bool: True if the data is stored successfully, False otherwise.
    """
    mode: str = "a"
    if modify:
        mode: str = "w"
    # Set the default mode as append, or change to write if data is being modified.

    with open(path, mode) as f:
        writer = csv.DictWriter(f, information_to_test[0].keys())  # Create a CSV writer with the dictionary keys as headers.
        if match(information_to_test[0], path) and modify:
            return False  # If data already exists and modification is required, return False.
        else:
            datas: list = data_recovery(path)  # Get existing data from the CSV file.
            if not datas:
                writer.writeheader()  # If the CSV file is empty, write the header.
        for row in information_to_test:
            writer.writerow(row)  # Write each dictionary as a row in the CSV file.


def delete(path: str, data_to_delete: dict = False, remove: bool = False):
    """
    Delete data from the CSV file.

    Args:
        path (str): Path to the CSV file.
        data_to_delete (dict, optional): Data to delete. Defaults to False.
        remove (bool, optional): Indicates if the file should be removed. Defaults to False.

    Returns:
        bool: True if the data is deleted successfully, False otherwise.
    """
    if remove:
        os.remove(remove)  # Remove the specified file if remove is True.
    match_password: list = match(data_to_delete, path)  # Find the data to delete in the CSV file.
    if match_password:
        data: list = data_recovery(path)  # Get existing data from the CSV file.
        data.remove(match_password[0])  # Remove the matched data from the list of dictionaries.
        store_csv(data, path, modify=True)  # Store the updated data in the CSV file.
    else:
        return False  # If data to delete is not found, return False.


def match(data_to_compare: dict, path: str, login: bool = False) -> list:
    """
    Match the provided data with the data in the CSV file.

    Args:
        data_to_compare (dict): Data to compare and match with the data in the CSV file.
        path (str): Path to the CSV file.
        login (bool, optional): Indicates if the matching is for login purposes. Defaults to False.

    Returns:
        list: List of dictionaries containing the matched data.
    """
    datas: list = data_recovery(path)  # Get data from the CSV file.
    if len(data_to_compare) > 2 or login:
        match: list = [ele for ele in datas if ((ele.get("name") == data_to_compare.get("name") and ele.get("password") == data_to_compare.get("password")) or (ele.get("email") == data_to_compare.get("email") and ele.get("password") == data_to_compare.get("password")))]
    else:
        match: list = [ele for ele in datas if ele.get("name") == data_to_compare.get("name") or ele.get("password") == data_to_compare.get("password")]
    return match


def register(path: str="data.csv", store=True) -> dict | None:
    """
    Register a new account.

    Returns:
        dict|None: Dictionary containing the registered account information, or None if registration is not successful.
    """
    information: dict = {}
    information_regex: dict = {
        "name": r"[a-zA-Z ]+",
        "date of birth": r"[0-3]?[0-9]/[0-1]?[0-9]/\d{4}",
        "country": r"[a-zA-Z]",
        "email": r"^[a-zA-Z0-9.! $%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9]{0,61}[a-zA-Z0-9])?)*$",
        "password": r"[^.]+",
    }
    title("Registration")  # Display the title using ASCII art.
    for k in information_regex.keys():
        while True:
            try:
                information[k] = input(f"Enter {k}: ")  # Get user input for each registration field.
                if not re.search(information_regex[k], information[k]):
                    raise ValueError  # Raise an error if the input does not match the expected pattern.
                break
            except ValueError:
                print("Invalid format")  # Display an error message for invalid input.
    if store:
        store_csv([information], path)  # Store the registered account information in the CSV file.
    return [information]

def main():
    def menu_interface():
        """
        Display the main menu and handle user input.
        """
        while True:
            try:
                title("Passwords manager")  # Display the title using ASCII art.
                print(*menu("menu"), sep="\n")  # Display the main menu options.
                response: int = int(input("\n" + "Enter option: "))  # Get user input for the menu choice.
                match response:
                    # Handle user response using match case.
                    case 1:
                        account = register()
                        menu_account(account)
                    case 2:
                        test_name: str = input("\n" + "Name / email to login: ").strip()
                        test_password: str = input("\n" + "Password: ").strip()
                        information: list = match({"name": test_name, "password": test_password}, "data.csv", login=True)
                        if not information:
                            title("Incorrect email or password.", font="digital")
                        else:
                            menu_account(information)
                    case 3:
                        title("Accounts")
                        show(information=False, path="data.csv")
                        time.sleep(1)
                    case 4:
                        print("\n" * 2)
                        cowsay.cow("Goodbye, world...")
                        break
                    case _:
                        raise ValueError

            except ValueError:
                title("Invalid input, please enter a correct answer!", font="digital")

    def menu_account(account):
        """
        Display the account menu and handle user input.
        """
        password_account_path: str = f"passwords/{account[0]['name']}{account[0]['password']}.csv"
        while True:
            try:
                title("Account")  # Display the title using ASCII art.
                print(*menu("login"), sep="\n")  # Display the account menu options.
                response: int = int(input("\n" + "Enter option: "))  # Get user input for the menu choice.
                match response:
                    # Handle user response using match case.
                    case 1:
                        menu_password(password_account_path)
                    case 2:
                        show(information=account)
                        time.sleep(1)
                    case 3:
                        ans: str = input("Do you want to delete this account? (y/n) ")
                        if ans.strip().lower() == "y":
                            delete("data.csv", data_to_delete=account[0], remove=password_account_path)
                            break
                    case 4:
                        break
                    case _:
                        raise ValueError

            except ValueError:
                title("Invalid input, please enter a correct answer!", font="digital")

    def menu_password(password_account_path):
        """
        Display the password menu and handle user input.
        """
        while True:
            try:
                title("Passwords menu")  # Display the title using ASCII art.
                show(path=password_account_path)  # Show the passwords in the account.
                print("\n" * 2)
                print(*menu("password"), sep="\n")  # Display the password menu options.
                response: int = int(input("\n" + "Enter option: "))  # Get user input for the menu choice.
                match response:
                    # Handle user response using match case.
                    case 1:
                        add_password(password_account_path)
                    case 2:
                        password: str = input("\n" + "Enter name or password to select: ").strip()
                        edit_password(password, password_account_path)
                    case 3:
                        ans: str = input("\n" + "Enter name or password to show: ").strip()
                        show(information=match({"name": ans, "password": ans}, password_account_path))
                        time.sleep(1)
                    case 4:
                        password: str = input("\n" + "Enter name or password to select: ").strip()
                        ans: str = input("Do you want to delete this password? (y/n) ")
                        if ans.strip().lower() == "y":
                            delete(password_account_path, data_to_delete={"name": password, "password": password})
                    case 5:
                        break
                    case _:
                        raise ValueError

            except ValueError:
                title("Invalid input, please enter a correct answer!", font="digital")

    def edit_password(password, path):
        """
        Edit a password.

        Args:
            password (str): Password to edit.
            path (str): Path to the account file.
        """
        passwords_matched: list = match({"name": password, "password": password}, path)  # Find the password to edit in the account.
        if passwords_matched:
            password_to_change: dict = passwords_matched[0].copy()  # Make a copy of the password to change.
            password_changed: dict = password_to_change.copy()  # Make a copy of the password that will be changed.
            name: str = input("\n" + "Enter the new name of this password (type k to keep the older) ")
            password: str = input("Enter the new password (type k to keep the older) ")
            if name != "k":
                password_changed["name"] = name  # Update the name if a new name is provided.
            if password != "k":
                password_changed["password"] = password  # Update the password if a new password is provided.
            passwords: list = data_recovery(path)  # Get existing passwords from the account file.
            passwords.insert(passwords.index(password_to_change), password_changed)  # Insert the updated password in the correct position.
            passwords.remove(password_to_change)  # Remove the original password from the list of passwords.
            store_csv(passwords, path=path, modify=True)  # Store the updated passwords in the account file.
        else:
            print("Aucun mot de passe a été trouvé !")  # Display a message if the password to edit is not found.

    def add_password(account_path):
        """
        Add a password to an account.

        Args:
            account_path (str): Path to the account file.
        """
        ans_gen_password: str = input("Do you want to generate a random password? (y/n) ")
        name: str = input("\n" + "Give a name to this password: ")
        if ans_gen_password.strip().lower() == "y":
            password: str = generate_password()
        else:
            password: str = input("\n" + "Password: ")
        store_csv([{"name": name, "password": password}], path=account_path)  # Store the password information in the account file.

    def show(information: list = False, path: str = False) -> None:
        """
        Display the information in a tabular format.

        Args:
            information (list, optional): List of dictionaries containing the information to display. Defaults to False.
            path (str, optional): Path to the CSV file containing the information. Defaults to False.
        """
        if not information:
            datas: list = data_recovery(path)  # Get data from the CSV file.
            if not datas:
                return None
            accounts: list = [list(ele.values()) for ele in datas]  # Extract values from dictionaries.
            if len(datas[0]) == 5:
                for ele in accounts:
                    ele[-1] = "*" * len(ele[-1])  # Hide passwords with asterisks if they exist.
            values: list = accounts
            keys: list = datas[0].keys()  # Get the keys of the dictionaries.

        else:
            values: list = [ele.values() for ele in information]  # Extract values from dictionaries.
            keys: list = information[0].keys()  # Get the keys of the dictionaries.

        print(tabulate(values, [ele.upper() for ele in list(keys)], tablefmt="grid"))  # Display data in a tabular format.

    menu_interface()


if __name__ == "__main__":
    main()  # Run the main menu interface when the script is executed.
