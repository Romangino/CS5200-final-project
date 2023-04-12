def menu(cursor):
    """
    Displays the admin menu
    :return: None
    """
    while True:
        print("Welcome to the user menu!")
        print("Select an option: ")
        print("1. Players")
        print("2. Teams")
        print("3. Games")
        print("4. Exit")
        option = input("Enter option #: ")
        match option:
            case "1":
                player_menu_user(cursor)
            case "2":
                teams_menu_user(cursor)
            case "3":
                games_menu_user(cursor)
            case "4":
                return
            case _:
                print("\nInvalid option\n")
