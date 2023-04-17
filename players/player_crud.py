from datetime import date

import pymysql


def add_player(cursor):
    """
    Adds a player to the database
    :param cursor:
    :return:
    """
    while True:
        try:
            print("Please enter the player's information")
            first_name = input("First name: ").capitalize()
            last_name = input("Last name: ").capitalize()

            print("Please enter the player's birth date")
            day = input("Day: ")
            month = input("Month: ")
            year = input("Year: ")
            while (not day.isdigit() or not month.isdigit() or not year.isdigit()
                   or int(day) < 1 or int(day) > 31
                   or int(month) < 1 or int(month) > 12
                   or int(year) < 1900 or int(year) > 2021):
                print("Invalid date")
                day = input("Day: ")
                month = input("Month: ")
                year = input("Year: ")

            birth_date = year + "-" + month + "-" + day

            print("Please enter the player's height")
            feet = input("Feet: ")
            inches = input("Inches: ")
            while (not feet.isdigit() or not inches.isdigit()) or (
                    int(feet) < 0 or int(inches) < 0 or int(inches) > 11):
                print("Invalid height")
                feet = input("Feet: ")
                inches = input("Inches: ")
            height = float(feet) + (float(inches) / 100)

            cursor.callproc('get_positions')
            result = cursor.fetchall()
            print("Positions:")
            for i in range(len(result)):
                print("ID: %i | Position Name: %s" %
                      (result[i]['position_id'],
                       result[i]['position_name']))

            position = input("Select a position #: ")
            while (not position.isdigit()) or (
                    int(position) < 0 or int(position) > len(result)):
                print("Invalid position")
                position = input("Select a position #: ")

            jersey_number = input("Jersey number: ")
            while not jersey_number.isdigit() or int(jersey_number) < 0:
                print("Invalid jersey number")
                jersey_number = input("Jersey number: ")

            is_active = input("Is active? (1/0): ")
            while is_active != "1" and is_active != "0":
                print("Invalid input")
                is_active = input("Is active? (1/0): ")

            season_exp = input("Season experience: ")
            while not season_exp.isdigit() or int(season_exp) < 0:
                print("Invalid season experience")
                season_exp = input("Season experience: ")

            cursor.callproc('get_teams')
            result = cursor.fetchall()
            all_team_ids = [result[i]['team_id'] for i in range(len(result))]
            print("Teams:")
            for i in range(len(result)):
                print("ID: %i | Team Name: %s" %
                      (result[i]['team_id'],
                       result[i]['team_name']))

            team_id = input("Enter a team ID: ")
            while (not team_id.isdigit()) or (int(team_id) not in all_team_ids):
                print("Invalid team")
                team_id = input("Select a team #: ")

            earliest_year = 1945
            season_year = input("Season year the player played on Team ID %s (ex. 2023): "
                                % team_id)
            while not season_year.isdigit() or int(season_year) < earliest_year \
                    or int(season_year) > date.today().year:
                print("Invalid season year")
                season_year = input("Season year the player played: ")

            print("Do you want to add Player:"
                  "\nFirst name: %s"
                  "\nLast name: %s"
                  "\nBirth date: %s"
                  "\nHeight: %s"
                  "\nPosition: %s"
                  "\nJersey number: %s"
                  "\nIs active: %s"
                  "\nSeason experience: %s"
                  "\nTeam ID: %s"
                  "\nSeason year: %s" % (first_name,
                                         last_name,
                                         birth_date,
                                         height,
                                         position,
                                         jersey_number,
                                         is_active,
                                         season_exp,
                                         team_id,
                                         season_year))

            add_player_confirmation = input("Add player? (Y/N): ").upper()
            while add_player_confirmation != "Y" and add_player_confirmation != "N":
                print("Invalid input")
                add_player_confirmation = input("Add player? (Y/N): ").upper()
            if add_player_confirmation == "N":
                print("Player not added\n")
                return

            cursor.callproc('create_player',
                            (first_name,
                             last_name,
                             birth_date,
                             height,
                             position,
                             jersey_number,
                             is_active,
                             season_exp,
                             team_id,
                             season_year))
            print("Player %s %s added\n" % (first_name, last_name))
            return
        except pymysql.Error as e:
            print("Error %d: %s" % (e.args[0], e.args[1]))


def view_player(cursor):
    """
    Views a player's information
    :param cursor:
    :return:
    """
    while True:
        try:
            player_id = input("Enter a Player ID (q to quit): ")
            if player_id.lower() == "q":
                break
            cursor.callproc('view_player_by_id', (player_id,))
            result = cursor.fetchone()
            if result is not None:
                print("ID: %s | "
                      "Name: %s %s | "
                      "Birth date: %s | "
                      "Height: %s | "
                      "Position: %s | "
                      "Jersey number: %s | "
                      "Is active: %s | "
                      "Season experience: %s |"
                      "Team: %s" % (result['player_id'],
                                    result['first_name'],
                                    result['last_name'],
                                    result['birth_date'],
                                    result['height'],
                                    result['position_name'],
                                    result['jersey_number'],
                                    result['is_active'],
                                    result['season_exp'],
                                    result['team_name']))
                print("\nWould you like to view another player?")
                view_another_player = input("Y/N: ").upper()
                if view_another_player == "N":
                    return
            else:
                print("Player not found")
        except pymysql.Error as e:
            print("Error %d: %s" % (e.args[0], e.args[1]))


def update_player(cursor):
    """
    Updates a player's information
    :param cursor:
    :return:
    """
    print("Please enter the ID of the player you want to update")
    player_id = input("Player ID: ")
    cursor.callproc('view_player_by_id', (player_id,))
    player_results = cursor.fetchone()
    if player_results is not None:
        print("Player ID: %s"
              "\nName: %s %s"
              "\nBirth date: %s"
              "\nHeight: %s"
              "\nPosition: %s"
              "\nJersey number: %s"
              "\nIs active: %s"
              "\nSeason experience: %s"
              "\nTeam: %s" % (player_results['player_id'],
                              player_results['first_name'],
                              player_results['last_name'],
                              player_results['birth_date'],
                              player_results['height'],
                              player_results['position_name'],
                              player_results['jersey_number'],
                              player_results['is_active'],
                              player_results['season_exp'],
                              player_results['team_name']))
        print("Enter in the following information to update the player's information")
        print("Leave blank if you do not want to update the field")

        while True:
            try:
                first_name_update = input("First name: ").capitalize() or player_results[
                    'first_name']

                last_name_update = input("Last name: ").capitalize() or player_results[
                    'last_name']

                birth_date_update = input("Birth date (YYYY-MM-DD): ") or player_results[
                    'birth_date']

                height_update = input("Height (ex. 6.02): ") or player_results['height']

                cursor.callproc('get_positions')
                positions_results = cursor.fetchall()
                print("Positions:")
                for i in range(len(positions_results)):
                    print("ID: %i | Position: %s" %
                          (positions_results[i]['position_id'],
                           positions_results[i]['position_name']))
                position_id_update = input("Enter Position ID: ") or player_results['position_id']

                jersey_number_update = input("Jersey number: ") or player_results['jersey_number']

                is_active_update = input("Is active? (1/0): ") or player_results['is_active']

                season_exp_update = input("Season experience: ") or player_results['season_exp']

                cursor.callproc('get_teams')
                teams_results = cursor.fetchall()
                print("Teams:")
                for i in range(len(teams_results)):
                    print("ID: %i | Team: %s" %
                          (teams_results[i]['team_id'],
                           teams_results[i]['team_name']))
                team_id_update = input("Enter Team ID: ") or player_results['team_id']

                season_year_update = input("Season year Player played on Team: ") or player_results[
                    'season_year']

                update_confirmation = input(
                    "Are you sure you want to update this player? (Y/N): ").upper()
                if update_confirmation == "Y":
                    player_id = player_results['player_id']
                    first_name_p = first_name_update or player_results['first_name']
                    last_name_p = last_name_update or player_results['last_name']
                    birth_date_p = birth_date_update or player_results['birth_date']
                    height_p = height_update or player_results['height']
                    position_id_p = position_id_update or player_results['position_id']
                    jersey_number_p = jersey_number_update or player_results['jersey_number']
                    is_active_p = is_active_update or player_results['is_active']
                    season_exp_p = season_exp_update or player_results['season_exp']
                    team_id_p = team_id_update or player_results['team_id']
                    season_year_p = season_year_update or player_results['season_year']

                    cursor.callproc('update_player', (player_id,
                                                      first_name_p,
                                                      last_name_p,
                                                      birth_date_p,
                                                      height_p,
                                                      position_id_p,
                                                      jersey_number_p,
                                                      is_active_p,
                                                      season_exp_p,
                                                      team_id_p,
                                                      season_year_p))

                    print("Player updated")
                    return
            except pymysql.Error as e:
                print("Error %d: %s" % (e.args[0], e.args[1]))

            else:
                print("Player not updated")
                return
    else:
        print("Player not found. Check Player ID.")
        return


def delete_player(cursor):
    """
    Deletes a player from the database
    :param cursor:
    :return:
    """
    print("Please enter Player ID of the player you want to delete")
    player_id = input("Player ID: ")
    try:
        cursor.callproc('view_player_by_id', (player_id,))
        player_results = cursor.fetchone()
        if player_results is not None:
            print("Player ID: %s"
                  "\nName: %s %s"
                  "\nBirth date: %s"
                  "\nHeight: %s"
                  "\nPosition: %s"
                  "\nJersey number: %s"
                  "\nIs active: %s"
                  "\nSeason experience: %s"
                  "\nTeam: %s" % (player_results['player_id'],
                                  player_results['first_name'],
                                  player_results['last_name'],
                                  player_results['birth_date'],
                                  player_results['height'],
                                  player_results['position_name'],
                                  player_results['jersey_number'],
                                  player_results['is_active'],
                                  player_results['season_exp'],
                                  player_results['team_name']))
            delete_confirmation = input(
                "Are you sure you want to delete this player? (Y/N): ").upper()
            if delete_confirmation == "Y":
                cursor.callproc('delete_player', (player_id,))
                print("Player deleted")
                return
        else:
            print("Player not found. Check Player ID.")
    except pymysql.Error as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
    return
