season_2018_2019_start = "2018-09-01"
season_2018_2019_end = "2019-08-31"
season_2019_2020_start = "2019-09-01"
season_2019_2020_end = "2020-08-31"
season_2020_2021_start = "2020-09-01"
season_2020_2021_end = "2021-08-31"
season_2021_2022_start = "2021-09-01"
season_2021_2022_end = "2022-08-31"
season_2022_2023_start = "2022-09-01"
season_2022_2023_end = "2023-08-31"


def player_menu_user(cursor):
    while True:
        print("Enter the player's first and last names: ")
        first_name = input("First name: ").capitalize()
        last_name = input("Last name: ").capitalize()
        query = "SELECT get_player_id(%s, %s)"
        cursor.execute(query, (first_name, last_name))
        player_id = cursor.fetchone().values()
        if None in player_id:
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
            player_info = cursor.fetchall()[0]
            if player_info["is_active"] == 0:
                player_info["is_active"] = "NO"
            else:
                player_info["is_active"] = "YES"
            player_info["height"] = str(player_info["height"]).replace(".", "\'") + "\""
            print(
                "\nFirst name: %s\n"
                "Last name: %s\n"
                "Team: %s\n"
                "Position: %s\n"
                "Birth date: %s\n"
                "Height: %s\n"
                "Jersey number: %s\n"
                "Currently playing: %s\n"
                "NBA seasons: %s\n"
                %
                (
                    player_info["first_name"],
                    player_info["last_name"],
                    player_info["team_name"],
                    player_info["position_name"],
                    player_info["birth_date"],
                    player_info["height"],
                    player_info["jersey_number"],
                    player_info["is_active"],
                    player_info["season_exp"],
                )
            )
        case "2":
            cursor.callproc('get_player_stats', player_id)
            player_stats = cursor.fetchall()[0]
            print(
                "\nPPG: %s\n"
                "APG: %s\n"
                "RPG: %s\n"
                "SPG: %s\n"
                "BPG: %s\n"
                "TPG: %s\n"
                "FPG: %s\n"
                "MPG: %s\n"
                %
                (
                    player_stats["avg_ppg"],
                    player_stats["avg_apg"],
                    player_stats["avg_rpg"],
                    player_stats["avg_spg"],
                    player_stats["avg_bpg"],
                    player_stats["avg_tpg"],
                    player_stats["avg_fpg"],
                    player_stats["avg_mpg"],
                )
            )


def teams_menu_user(cursor):
    while True:
        print("Enter the team's city and name: ")
        city = input("City: ").capitalize()
        name = input("Name: ").capitalize()
        query = "SELECT get_team_id(%s, %s)"
        cursor.execute(query, (city, name))
        team_id = cursor.fetchone().values()
        if None in team_id:
            print("Team not found, please try again")
        else:
            break
    print("What would you like to view?")
    print(f"1. {city} {name}'s info")
    print(f"2. {city} {name}'s stats")
    option = input("Enter option #: ")
    match option:
        case "1":
            cursor.callproc('get_team_info', team_id)
            team_info = cursor.fetchall()[0]
            print(
                "\nName: %s\n"
                "Abbreviation: %s\n"
                "State: %s\n"
                "Established: %s\n"
                "Wins: %s\n"
                "Losses: %s\n"
                %
                (
                    team_info["team_name"],
                    team_info["abbreviation"],
                    team_info["state"],
                    team_info["year_founded"],
                    team_info["wins"],
                    team_info["losses"]
                )
            )
        case "2":
            cursor.callproc('get_team_stats', team_id)
            team_stats = cursor.fetchall()[0]
            print(
                "\nPPG: %s\n"
                %
                (
                    team_stats["avg_ppg"]
                )
            )
        #case _:


def games_menu_user(cursor):
    while True:
        print("What would you like to view?")
        print(f"1. {city} {name}'s info")
        print(f"2. {city} {name}'s stats")


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
