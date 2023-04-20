import datetime

from data_setup.import_data import import_players, import_teams, import_games, import_player_stats
from games.game_crud import add_game, view_game, update_game, delete_game
from players.player_crud import add_player, view_player, update_player, delete_player
from teams.team_crud import add_team, view_team, update_team, delete_team


def player_menu_admin(cursor):
    """
    Displays the player menu
    :param cursor:
    :return:
    """
    while True:
        print("\nWelcome to the Player menu!")
        print("Select an option: ")
        print("1. Add Player")
        print("2. View Player")
        print("3. Update Player")
        print("4. Delete Player")
        print("5. Back to main menu")
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


def teams_menu_admin(cursor):
    """
    Displays the team menu
    :param cursor:
    :return:
    """
    while True:
        print("\nWelcome to the Team menu!")
        print("Select an option: ")
        print("1. Add Team")
        print("2. View Team")
        print("3. Update Team")
        print("4. Delete Team")
        print("5. Back to main menu")
        option = input("Enter option #: ")
        match option:
            case "1":
                add_team(cursor)
            case "2":
                view_team(cursor)
            case "3":
                update_team(cursor)
            case "4":
                delete_team(cursor)
            case "5":
                return
            case _:
                print("\nInvalid option\n")


def games_menu_admin(cursor):
    """
    Displays the game menu
    :param cursor:
    :return:
    """
    while True:
        print("\nWelcome to the Game menu!")
        print("Select an option: ")
        print("1. Add Game")
        print("2. View Game")
        print("3. Update Game")
        print("4. Delete Game")
        print("5. Back to main menu")
        option = input("Enter option #: ")
        match option:
            case "1":
                add_game(cursor)
            case "2":
                view_game(cursor)
            case "3":
                update_game(cursor)
            case "4":
                delete_game(cursor)
            case "5":
                return
            case _:
                print("\nInvalid option\n")


def update_database(cursor):
    """
    Updates the database to include most recent games and stats for players
    :param cursor:
    :return:
    """
    # Get current season
    current_year = datetime.datetime.now().year
    last_year = current_year - 1
    current_season = str(last_year) + "-" + str(current_year)[2:]

    print("Updating database will provide the most recent stats for players and games.")
    update_confirmation = input(
        "Do you want to import any new active players from API? (Y/N): ").upper()
    if update_confirmation == "Y":
        # Add players that are not in the database
        import_players(cursor)

    update_confirmation = input(
        "Do you want to import any new teams from API? (Y/N): ").upper()
    if update_confirmation == "Y":
        # Add teams that are not in the database
        import_teams(cursor)

    update_confirmation = input(
        "Do you want to import any new games from API? (Y/N): ").upper()
    if update_confirmation == "Y":
        # Add games that are not in the database
        print("Updating Games for %s Season from API..." % current_season)
        import_games(cursor, current_season)

    update_confirmation = input(
        "Do you want to import any new player stats from API? This will take a few minutes to "
        "complete and API maybe get rate limited. (Y/N): ").upper()
    if update_confirmation == "Y":
        # Add player stats for games that are not in the database
        try:
            print("Updating Player Stats for %s Season from API..." % current_season)
            import_player_stats(cursor, current_season)
        except Exception as e:
            print("Error: %s" % e)
            print("API may have been rate limited. Please try again later.")


def menu(cursor):
    """
    Displays the admin menu
    :return: None
    """
    while True:
        print("\nWelcome to the Admin menu!")
        print("Select an option: ")
        print("1. Players")
        print("2. Teams")
        print("3. Games")
        print("4. Update Database")
        print("5. Exit")
        option = input("Enter option #: ")
        match option:
            case "1":
                player_menu_admin(cursor)
            case "2":
                teams_menu_admin(cursor)
            case "3":
                games_menu_admin(cursor)
            case "4":
                update_database(cursor)
            case "5":
                return
            case _:
                print("\nInvalid option\n")
