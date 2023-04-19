def player_menu_user(cursor):
    while True:
        print("Enter the player's first and last names: ")
        first_name = input("First name: ")
        last_name = input("Last name: ")
        cursor.execute("get_player_id", (first_name, last_name))
        player_id = cursor.fetchone()
        if player_id is None:
            print("Player not found, please try again")
        else:
            break
    print("What would you like to view?")
    print(f"1. {first_name} {last_name}'s info")
    print(f"2. {first_name} {last_name}'s stats")
    option = input("Enter option #: ")
    match option:
        case "1":
            cursor.callproc('get_player_info', player_id)
            player_info = cursor.fetchall()
            if player_info["is_active"] == 0:
                player_info["is_active"] = "NO"
            else:
                player_info["is_active"] = "YES"
            print(
                "First name: %s"
                "Last name: %s"
                "Birth date: %s"
                "Height: %s"
                "Jersey number: %s"
                "Currently playing: %s"
                "NBA seasons: %s"
                %
                (
                    player_info["first_name"],
                    player_info["last_name"],
                    player_info["birth_date"],
                    player_info["height"],
                    player_info["jersey_number"],
                    player_info["is_active"],
                    player_info["season_exp"],
                )
            )


def teams_menu_user(cursor):
    pass


def games_menu_user(cursor):
    pass


def menu(cursor):
    """
    Displays the user menu
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
