import pymysql


def add_team(cursor):
    """
    Adds a team to the database
    :param cursor:
    :return:
    """
    print("\nAdd Team")
    try:
        team_name = input("Enter team name: ").title()
        abbreviation = input("Enter team abbreviation (3 letters): ").upper()
        nickname = input("Enter team nickname: ").title()
        city = input("Enter team city: ").title()
        state = input("Enter team state: ").title()
        year_founded = input("Enter year founded: ")

        print("\nTeam Name: %s"
              "\nTeam Abbreviation: %s"
              "\nTeam Nickname: %s"
              "\nTeam City: %s"
              "\nTeam State: %s"
              "\nYear Founded: %s" % (team_name,
                                      abbreviation,
                                      nickname,
                                      city,
                                      state,
                                      year_founded))

        team_add_confirm = input("Do you want to add this team? (Y/N): ").upper()
        if team_add_confirm == "Y":
            cursor.callproc("create_team",
                            (team_name,
                             abbreviation,
                             nickname,
                             city,
                             state,
                             year_founded))
            print("Team added successfully!")
            return
    except pymysql.Error as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
    return print("Team not added")


def view_team(cursor):
    """
    Displays a team from the database
    :param cursor:
    :return:
    """
    print("\nView Team")
    try:
        team_id = input("Enter team ID: ")
        cursor.callproc("view_team_by_id", (team_id,))
        team_result = cursor.fetchone()
        if team_result:
            print("\nTeam ID: %s"
                  "\nTeam Name: %s"
                  "\nAbbreviation: %s"
                  "\nNickname: %s"
                  "\nCity: %s"
                  "\nState: %s"
                  "\nYear Founded: %s" % (team_result['team_id'],
                                          team_result['team_name'],
                                          team_result['abbreviation'],
                                          team_result['nickname'],
                                          team_result['city'],
                                          team_result['state'],
                                          team_result['year_founded']))
            return
    except pymysql.Error as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
    return print("Team not found")


def update_team(cursor):
    """
    Updates a team in the database
    :param cursor:
    :return:
    """
    print("\nUpdate Team")
    try:
        team_id = input("Enter team ID: ")
        cursor.callproc("view_team_by_id", (team_id,))
        team_result = cursor.fetchone()
        if team_result:
            print("\nTeam ID: %s"
                  "\nTeam Name: %s"
                  "\nAbbreviation: %s"
                  "\nNickname: %s"
                  "\nCity: %s"
                  "\nState: %s"
                  "\nYear Founded: %s" % (team_result['team_id'],
                                          team_result['team_name'],
                                          team_result['abbreviation'],
                                          team_result['nickname'],
                                          team_result['city'],
                                          team_result['state'],
                                          team_result['year_founded']))

            team_name = input("Enter team name: ").title() or team_result['team_name']
            abbreviation = input("Enter team abbreviation (3 letters): ").upper() or team_result['abbreviation']
            nickname = input("Enter team nickname: ").title or team_result['nickname']
            city = input("Enter team city: ").title() or team_result['city']
            state = input("Enter team state: ").title() or team_result['state']
            year_founded = input("Enter year founded: ") or team_result['year_founded']

            print("\nTeam Name: %s"
                  "\nTeam Abbreviation: %s"
                  "\nTeam Nickname: %s"
                  "\nTeam City: %s"
                  "\nTeam State: %s"
                  "\nYear Founded: %s" % (team_name,
                                          abbreviation,
                                          nickname,
                                          city,
                                          state,
                                          year_founded))

            team_update_confirm = input("Do you want to update this team? (Y/N): ").upper()
            if team_update_confirm == "Y":
                cursor.callproc("update_team",
                                (team_id,
                                 team_name,
                                 abbreviation,
                                 nickname,
                                 city,
                                 state,
                                 year_founded))
                print("Team updated successfully!")
                return
        else:
            print("Team not found")
            return
    except pymysql.Error as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
    return print("Team not updated")


def delete_team(cursor):
    """
    Deletes a team from the database
    :param cursor:
    :return:
    """
    print("\nDelete Team")
    print("WARNING: This will delete all data associated with this team!")
    try:
        team_id = input("Enter team ID: ")
        cursor.callproc("view_team_by_id", (team_id,))
        team_result = cursor.fetchone()
        if team_result:
            print("\nTeam ID: %s"
                  "\nTeam Name: %s"
                  "\nAbbreviation: %s"
                  "\nNickname: %s"
                  "\nCity: %s"
                  "\nState: %s"
                  "\nYear Founded: %s" % (team_result['team_id'],
                                          team_result['team_name'],
                                          team_result['abbreviation'],
                                          team_result['nickname'],
                                          team_result['city'],
                                          team_result['state'],
                                          team_result['year_founded']))

            team_delete_confirm = input("Are you sure you want to delete this team? (Y/N): ").upper()
            if team_delete_confirm == "Y":
                cursor.callproc("delete_team", (team_id,))
                print("Team deleted successfully!")
                return
        else:
            return print("Team not found")
    except pymysql.Error as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
    return print("Team not deleted")
