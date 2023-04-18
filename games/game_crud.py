import pymysql


def add_game(cursor):
    """
    Adds a game to the database
    :param cursor:
    :return:
    """
    print("\nAdd Game")
    try:
        cursor.callproc("get_teams")
        team_result = cursor.fetchall()
        print(team_result)
        print("Team Available: ")
        for team in team_result:
            print("Team ID: %s | Team Name: %s" % (team['team_id'], team['team_name']))
        home_team_id = input("Enter home team ID: ")
        away_team_id = input("Enter away team ID: ")
        home_team_pts = input("Enter home team points: ")
        away_team_pts = input("Enter away team points: ")
        game_date = input("Enter game date (YYYY-MM-DD): ")
        if home_team_pts == away_team_pts:
            winner_id = -1
        elif home_team_pts > away_team_pts:
            winner_id = home_team_id
        else:
            winner_id = away_team_id
        cursor.callproc("view_team_by_id", (home_team_id,))
        home_team_name = cursor.fetchone()['team_name']
        cursor.callproc("view_team_by_id", (away_team_id,))
        away_team_name = cursor.fetchone()['team_name']
        cursor.callproc("view_team_by_id", (winner_id,))
        winner_name = cursor.fetchone()['team_name']

        print("\nHome Team: %s"
              "\nAway Team: %s"
              "\nHome Team Points: %s"
              "\nAway Team Points: %s"
              "\nWinner: %s"
              "\nGame Date: %s" % (home_team_name,
                                   away_team_name,
                                   home_team_pts,
                                   away_team_pts,
                                   winner_name,
                                   game_date))

        game_add_confirm = input("Add game? (Y/N): ").upper()
        while game_add_confirm not in ["Y", "N"]:
            game_add_confirm = input("Invalid input. Add game? (Y/N): ").upper()

        if game_add_confirm == "Y":
            cursor.callproc("create_game",
                            (home_team_id,
                             away_team_id,
                             home_team_pts,
                             away_team_pts,
                             game_date,
                             winner_id))
            return print("Game added successfully!")

    except pymysql.Error as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
    return print("Game not added")


def view_game(cursor):
    """
    Displays a game from the database
    :param cursor:
    :return:
    """
    print("\nView Game")
    try:
        game_id = input("Enter game ID: ")
        cursor.callproc("view_game_by_id", (game_id,))
        game_result = cursor.fetchone()
        if game_result:
            print("\nGame ID: %s"
                  "\nHome Team ID: %s"
                  "\nAway Team ID: %s"
                  "\nGame Date: %s"
                  "\nGame Time: %s" % (game_result[0],
                                       game_result[1],
                                       game_result[2],
                                       game_result[3],
                                       game_result[4]))
            return
    except pymysql.Error as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
    return print("Game not found")


def update_game(cursor):
    """
    Updates a game in the database
    :param cursor:
    :return:
    """
    print("\nUpdate Game")
    try:
        game_id = input("Enter game ID: ")
        cursor.callproc("view_game_by_id", (game_id,))
        game_result = cursor.fetchone()
        if game_result:
            print("\nGame ID: %s"
                  "\nHome Team ID: %s"
                  "\nAway Team ID: %s"
                  "\nGame Date: %s"
                  "\nGame Time: %s" % (game_result[0],
                                       game_result[1],
                                       game_result[2],
                                       game_result[3],
                                       game_result[4]))
            game_update_confirm = input("Update game? (Y/N): ")
            if game_update_confirm == "Y":
                home_team_id = input("Enter home team ID: ")
                away_team_id = input("Enter away team ID: ")
                game_date = input("Enter game date (YYYY-MM-DD): ")
                game_time = input("Enter game time (HH:MM:SS): ")
                cursor.callproc("update_game",
                                (game_id,
                                 home_team_id,
                                 away_team_id,
                                 game_date,
                                 game_time))
                print("Game updated successfully!")
                return
    except pymysql.Error as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
    return print("Game not updated")


def delete_game(cursor):
    """
    Deletes a game from the database
    :param cursor:
    :return:
    """
    print("\nDelete Game")
    try:
        game_id = input("Enter game ID: ")
        cursor.callproc("view_game_by_id", (game_id,))
        game_result = cursor.fetchone()
        if game_result:
            print("\nGame ID: %s"
                  "\nHome Team ID: %s"
                  "\nAway Team ID: %s"
                  "\nGame Date: %s"
                  "\nGame Time: %s" % (game_result[0],
                                       game_result[1],
                                       game_result[2],
                                       game_result[3],
                                       game_result[4]))
            game_delete_confirm = input("Delete game? (Y/N): ")
            if game_delete_confirm == "Y":
                cursor.callproc("delete_game", (game_id,))
                print("Game deleted successfully!")
                return
    except pymysql.Error as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
    return print("Game not deleted")
