import pymysql


def add_player(cursor):
    """
    Adds a player to the database
    :param cursor:
    :return:
    """
    # TODO: Add a player to the database
    while True:
        try:
            # TODO: Validate name doesn't exist
            print("Please enter the player's information")
            first_name = input("First name: ")
            last_name = input("Last name: ")

            # TODO: Validate the birth date
            print("Please enter the player's birth date")
            day = input("Day: ")
            month = input("Month: ")
            year = input("Year: ")
            birth_date = year + "-" + month + "-" + day

            # TODO: Validate the height
            print("Please enter the player's height")
            feet = input("Feet: ")
            inches = input("Inches: ")
            height = float(feet) + (float(inches) / 100)

            # TODO: Create procedure to get positions
            cursor.callproc('get_positions')
            result = cursor.fetchall()
            highest_id = len(result)
            lowest_id = 1
            print("Positions:")
            for i in range(len(result)):
                print(str(i + 1) + ". " + result[i]['position_id'])
            position = input("Select a position #: ")
            while (not position.isdigit()) or (
                    int(position) < lowest_id or int(position) > highest_id):
                print("Invalid position")
                position = input("Select a position #: ")

            # TODO: Validate the JERSEY NUMBER
            jersey_number = input("Jersey number: ")
            while not jersey_number.isdigit() or int(jersey_number) < 0:
                print("Invalid jersey number")
                jersey_number = input("Jersey number: ")

            # TODO: Validate is_active
            is_active = input("Is active? (Y/N): ").upper()
            while is_active != "Y" and is_active != "N":
                print("Invalid input")
                is_active = input("Is active? (Y/N): ").upper()

            # TODO: Validate season_exp
            season_exp = input("Season experience: ")
            while not season_exp.isdigit() or int(season_exp) < 0:
                print("Invalid season experience")
                season_exp = input("Season experience: ")

            # TODO: Show teams in the database and allow the user to select one. Create a
            #  procedure to get teams
            cursor.callproc('get_teams')
            result = cursor.fetchall()
            highest_id = len(result)
            lowest_id = 1
            print("Teams:")
            for i in range(len(result)):
                print(str(i + 1) + ". " + result[i]['team_name'])

            team = input("Select a team #: ")
            while (not team.isdigit()) or (int(team) < lowest_id or int(team) > highest_id):
                print("Invalid team")
                team = input("Select a team #: ")

            # TODO: Validate season_year
            earliest_year = 1945
            season_year = input("Season year the player played on the %s (ex. 2023): "
                                % result[int(team) - 1]['team_name'])
            while not season_year.isdigit() or int(season_year) < earliest_year:
                print("Invalid season year")
                season_year = input("Season year the player played: ")

            # TODO: create the player
            cursor.callproc('create_player',
                            (first_name,
                             last_name,
                             birth_date,
                             height,
                             position,
                             jersey_number,
                             is_active,
                             season_exp,
                             team,
                             season_year))

            break
        except pymysql.Error as e:
            print("Error %d: %s" % (e.args[0], e.args[1]))
    # TODO: Create and update the stored procedure
    cursor.callproc('create_player', (first_name, last_name, team, position, age, height))
    print("Player added")
    return


def view_player(cursor):
    """
    Views a player's information
    :param cursor:
    :return:
    """
    # TODO: View a player's information add options to search by id or name.
    print("Please enter the player's name")
    first_name = input("First name: ")
    last_name = input("Last name: ")
    cursor.callproc('view_player', (first_name, last_name))
    result = cursor.fetchone()
    print(result)
    return


def update_player(cursor):
    """
    Updates a player's information
    :param cursor:
    :return:
    """
    print("Please enter the player's name")
    first_name = input("First name: ")
    last_name = input("Last name: ")
    print("Please enter the player's new information")
    new_first_name = input("First name: ")
    new_last_name = input("Last name: ")
    new_team = input("Team: ")
    new_position = input("Position: ")
    new_age = input("Age: ")
    new_height = input("Height: ")
    cursor.callproc('update_player', (
        first_name, last_name, new_first_name, new_last_name, new_team, new_position, new_age,
        new_height))
    print("Player updated")
    return


def delete_player(cursor):
    """
    Deletes a player from the database
    :param cursor:
    :return:
    """
    print("Please enter the player's name")
    first_name = input("First name: ")
    last_name = input("Last name: ")
    cursor.callproc('delete_player', (first_name, last_name))
    print("Player deleted")
    return
