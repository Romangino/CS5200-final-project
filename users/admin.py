from players.player_crud import add_player, view_player, update_player, delete_player


def menu(cursor):
    """
    Displays the admin menu
    :return: None
    """
    while True:
        print("Welcome to the admin menu!")
        print("Select an option: ")
        print("1. Players")
        print("2. Teams")
        print("3. Games")
        print("4. Exit")
        option = input("Enter option #: ")
        match option:
            case "1":
                player_menu_admin(cursor)
            case "2":
                teams_menu_admin(cursor)
            case "3":
                games_menu_admin(cursor)
            case "4":
                return
            case _:
                print("\nInvalid option\n")


def player_menu_admin(cursor):
    """
    Displays the player menu
    :param cursor:
    :return:
    """
    while True:
        print("Welcome to the player menu!")
        print("Select an option: ")
        print("1. Add Player")
        print("2. View Player")
        print("3. Update Player")
        print("4. Delete Player")
        print("5. Exit")
        option = input("Enter option #: ")
        match option:
            case "1":
                add_player(cursor)
            case "2":
                view_player(cursor)
            case "3":
                update_player(cursor)
            case "4":
                delete_player(cursor)
            case "5":
                return
            case _:
                print("\nInvalid option\n")
