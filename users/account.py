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
        # TODO: Create stored procedure check_username in login_procs.sql
        cursor.callproc('check_username', (username_p,))
        result = cursor.fetchone()
        if result is None:
            print("Username does not exist")
            print("Please try again")
        else:
            break

    while True:
        password_p = input("Password: ")
        # TODO: Create stored procedure check_password in login_procs.sql
        cursor.callproc('check_password', (password_p,))
        result = cursor.fetchone()
        if result is None:
            print("Password does not exist")
            print("Please try again")
        else:
            break

    print("Logging in...")

    # Call the stored procedure to log in the user
    # TODO: Create stored procedure login_user in login_procs.sql
    cursor.callproc('login_user', (username_p, password_p))
    result = cursor.fetchone()

    username = result['username']
    password = result['password_hash']
    account_type = result['account_type']

    returning_user = {
        "username": username,
        "password": password,
        "account_type": account_type
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
        username = input("Username: ")
        # TODO: Create stored procedure check_username in login_procs.sql
        cursor.callproc('check_username', (username,))
        result = cursor.fetchone()
        if result is not None:
            print("Username already exists")
            print("Please try again")
        else:
            break

    hashed_password = get_hashed_password(input("Password: "))
    while True:
        confirm_password = input("Confirm Password: ")
        if hashed_password == get_hashed_password(confirm_password):
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
            account_type = "USER"
            break
        elif account_type == "2":
            security_code = input("Enter Security Code (FOR TESTING: 1234): ")
            if security_code == "1234":
                account_type = "ADMIN"
                break
            else:
                print("Invalid Security Code")
                print("Please try again")
        else:
            print("Invalid Account Type")
            print("Please try again")

    new_user = {
        "username": username,
        "password": hashed_password,
        "account_type": account_type
    }
    print("Registering...")

    # Call the stored procedure to register the user
    # TODO: Create stored procedure register_user in login_procs.sql
    cursor.callproc('register_user',
                    (new_user['username'],
                     new_user['password'],
                     new_user['account_type']))
    result = cursor.fetchone()
    status = result

    print("Welcome, " + new_user['username'] + "!")
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
