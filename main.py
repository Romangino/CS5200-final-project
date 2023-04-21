from users import admin, user
from users.account import login, register
import pymysql.cursors


def create_connection():
    """
    Creates a connection to the database
    :return: The connection object
    """
    DB_HOST = input("Enter MySQL hostname: ")
    DB_USER = input("Enter MySQL user: ")
    DB_PASSWORD = input("Enter MySQL password: ")
    DB_NAME = input("Enter MySQL database: ")

    connection = pymysql.connect(host=DB_HOST,
                                 user=DB_USER,
                                 password=DB_PASSWORD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


def quit_program(cursor, connection):
    """
    Quits the program
    :param cursor: cursor object
    :param connection: connection object
    :return: None
    """
    # Close the cursor
    cursor.close()

    # Close the connection
    connection.close()

    print("Exiting...")
    print("Goodbye!")
    exit()


def start_screen(cursor):
    """
    Displays the start screen
    :param cursor: The cursor object
    :return: The current user
    """
    while True:
        print("Welcome to NBA Stats!")
        print("Select an option: ")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        option = input("Enter option #: ")
        match option:
            case "1":
                return login(cursor)
            case "2":
                return register(cursor)
            case "3":
                return
            case _:
                print("\nInvalid option\n")


def main():
    """
    Main function
    :return: None
    """
    try:
        # Connect to the database
        connection = create_connection()

        # connection autocommit enabled
        connection.autocommit(True)

        # Create a cursor object
        cursor = connection.cursor()

        # Start the program
        current_user = start_screen(cursor)

        if current_user is not None:
            match current_user['admin']:
                case 1:
                    admin.menu(cursor)
                case 0:
                    user.menu(cursor)
                case _:
                    print("Error: Invalid admin value! Account error contact admin!")

        quit_program(cursor, connection)

    except pymysql.Error as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))


if __name__ == "__main__":
    main()
