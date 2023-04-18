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


def menu(cursor):
    """
    Displays the admin menu
    :return: None
    """
    while True:
        print("\nWelcome to the admin menu!")
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
