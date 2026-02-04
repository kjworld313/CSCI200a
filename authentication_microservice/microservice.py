import sqlite3
import hashlib
import getpass
import argparse

### Source code above supplied by Professor Leeson
#################################################################

def initialize_db()->sqlite3.Cursor:
    """Creates the database and the users table if they don't exist."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    return conn

def input_validation(target: str)->bool:
    '''Performs input validation on provided string. Ensures argument only contains
    characters from the following permitted characters: letters (uppercase or lowercase),
    numbers, underscores, or the special characters ! & $'''
    valid_characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_!&$"

    # go through argument and validate each character
    for char in target:
        # end function if character is invalid
        if char not in valid_characters:
            return False
    return True # valid string

def add_user()->None:
    """Prompts for credentials and saves them to the database."""
    # get username and password
    username = input("Enter new username: ")
    password = getpass.getpass("Enter new password: ")

    # ensure requirements are met
    if not(input_validation(username) and input_validation(password)):
         # alert user and end add user attempt if invalid
        print("Error: Username or password cannot contain forbidden special characters.")
        return
    elif len(password) < 8: # ensure password is an appropriate length
        print("Error: Password must have a minimum of 8 characters.")
        return
    
    # hash password
    password = hashlib.pbkdf2_hmac("sha512", password.encode('utf-8'), password.encode('utf-8') * len(password) * 2, 300000, dklen=None) 
    
    # establish connection to database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # attempt to create an entry for the new user
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
                       (username, password))
        conn.commit()
        print(f"User '{username}' registered successfully!")
    except sqlite3.IntegrityError:
        print("Error: That username is already taken.")
    finally:
        conn.close()

def verify_login()->bool:
    '''Prompts for credentials, authenticates user by comparing inputted credentials
    to the credentials stored in the database, and returns the status of the authentication
    process.'''
    # get username and password
    username = input("Enter new username: ")
    password = getpass.getpass("Enter new password: ")

    # ensure requirements are met
    if not(input_validation(username) and input_validation(password)):
         # alert user and end login attempt if invalid
        print("Error: Username or password cannot contain forbidden special characters.")
        return
    elif len(password) < 8: # ensure password is an appropriate length
        print("Error: Password must have a minimum of 8 characters.")
        return

    # establish connection to database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # get user details
    details = cursor.execute("SELECT username, password FROM users WHERE username=?", (username,)).fetchone()
    conn.close()

    # check if username or password is invalid
    if details == None or details[1] != hashlib.pbkdf2_hmac("sha512", password.encode('utf-8'), password.encode('utf-8') * len(password) * 2, 300000, dklen=None):
        print("Error: That username does not exist or the password is incorrect.")
        return False
    else: # user authenticated
        return True

#################################################################
### Source code below supplied by Professor Leeson

parser = argparse.ArgumentParser(prog='HW-6')
parser.add_argument("--add", action="store_true", help="Adding a new user")
parser.add_argument("--login", action="store_true", help="Verify user login")

if __name__ == "__main__":
    args = parser.parse_args()

    initialize_db()
    if args.add == True:
        add_user()
    elif args.login == True:
        verify_login()
    else:
        parser.print_help()