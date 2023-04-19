import bcrypt as bcrypt


def login(cursor):
    """
    Login to an existing user account
    :param cursor: cursor object
    :return: The current user
    """
    print("Please enter your username and password")
    while True:
        username_p = input("Username: ")
        cursor.callproc('check_username', (username_p,))
        result = cursor.fetchone()
        if result is not None:
            break
        else:
            print("Username does not exist")
            print("Please try again")

    while True:
        password_p = input("Password: ").encode()
        cursor.callproc('get_password_hash', (username_p,))
        result = cursor.fetchone()
        if result is not None:
            hashed_password = result['password_hash'].encode()
            if check_password(password_p, hashed_password):
                break
        print("Incorrect password")
        print("Please try again")

    print("Logging in...\n")

    # Call the stored procedure to log in the user
    cursor.callproc('get_user', (username_p,))
    result = cursor.fetchone()

    user_id = result['user_id']
    username = result['username']
    hashed_password = result['password_hash']
    admin = result['admin']

    returning_user = {
        "user_id": user_id,
        "username": username,
        "hashed_password": hashed_password,
        "admin": admin
    }

    print("Welcome back, " + returning_user['username'] + "!")

    return returning_user


def register(cursor):
    """
    Register a new user account
    :param cursor: cursor object
    :return: The new user
    """
    print("Please enter your username and password")

    while True:
        username_p = input("Username: ")
        cursor.callproc('check_username', (username_p,))
        result = cursor.fetchone()
        if result is not None:
            print("Username already exists")
            print("Please try again")
        else:
            break

    hashed_password = get_hashed_password(input("Password: ").encode())
    while True:
        confirm_password = input("Confirm Password: ").encode()
        if check_password(confirm_password, hashed_password):
            break
        else:
            print("Passwords do not match")
            print("Please try again")

    while True:
        print("Select Account Type #: ")
        print("1. User")
        print("2. Admin")
        account_type = input("Account Type: ")
        if account_type == "1":
            admin = False
            break
        elif account_type == "2":
            security_code = input("Enter Security Code (FOR TESTING: 1234): ")
            if security_code == "1234":
                admin = True
                break
            else:
                print("Invalid Security Code")
                print("Please try again")
        else:
            print("Invalid Account Type")
            print("Please try again")

    print("Registering...\n")

    # Call the stored procedure to register the user
    cursor.callproc('create_user', (username_p,
                                    hashed_password,
                                    admin))
    new_user = {
        "username": username_p,
        "hashed_password": hashed_password,
        "admin": admin
    }
    return new_user


def get_hashed_password(plain_text_password):
    """
    Hashes a password
    :param plain_text_password: The password to hash
    :return: The hashed password
    """
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())


def check_password(plain_text_password, hashed_password):
    """
    Checks a password against a hashed password
    :param plain_text_password: un-hashed password
    :param hashed_password: hashed password
    :return: True if the passwords match, False otherwise
    """
    return bcrypt.checkpw(plain_text_password, hashed_password)
