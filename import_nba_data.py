import time

import pandas as pd
from nba_api.stats.static.players import *
from nba_api.stats.static.teams import *
from nba_api.stats.endpoints import playercareerstats, commonplayerinfo, teamgamelog, \
    LeagueGameFinder, PlayerGameLogs, PlayerGameLog
import os
import pymysql.cursors
from dotenv import load_dotenv


# create player
def update_players(cursor):
    # Find all player_id from nba_players table
    cursor.execute("SELECT player_id FROM nba_players")
    player_ids = cursor.fetchall()
    player_ids = [player['player_id'] for player in player_ids]

    # Get all active players from nba_api
    player_info = get_active_players()
    i = 0
    for player in player_info:
        if player['id'] not in player_ids:
            i += 1
            time.sleep(0.25)
            playerCommonInfo = commonplayerinfo.CommonPlayerInfo(player['id'])
            player_api = playerCommonInfo.get_dict()
            keys = player_api['resultSets'][0]['headers']
            values = player_api['resultSets'][0]['rowSet'][0]
            if len(keys) == len(values):
                player_dict = dict(zip(keys, values))

                if len(player_dict['JERSEY']) > 2:
                    player_dict.update({'JERSEY': re.split(r'\D', player_dict['JERSEY'])[-1]})

                if player_dict['JERSEY'] == '':
                    player_dict.update({'JERSEY': None})

                if player_dict['HEIGHT'] == '':
                    player_dict.update({'HEIGHT': None})

                if player_dict['HEIGHT'] is not None:
                    feet, inches = player_dict['HEIGHT'].split('-')
                    player_dict.update({'HEIGHT': float(feet) + (float(inches) / 100)})

                if player_dict['POSITION'] == '' or player_dict['POSITION'] is None:
                    player_dict.update({'POSITION': 'Unknown'})

                cursor.callproc('create_nba_player',
                                (player_dict['PERSON_ID'],
                                 player_dict['FIRST_NAME'],
                                 player_dict['LAST_NAME'],
                                 player_dict['BIRTHDATE'],
                                 player_dict['HEIGHT'],
                                 player_dict['POSITION'],
                                 player_dict['JERSEY'],
                                 True if player_dict['ROSTERSTATUS'] == 'Active' else False,
                                 player_dict['SEASON_EXP'],
                                 player_dict['TEAM_ID'],
                                 player_dict['TO_YEAR']))

                print("Created player %s: %s (%s)" % (i,
                                                      player_dict['DISPLAY_FIRST_LAST'],
                                                      player_dict['PERSON_ID']))

            else:
                print("Error: keys and values are not the same length")
                print(keys)
                print(values)

        # else:
        #     print("Player %s (%s) already exists" % (player['full_name'],
        #                                              player['id']))
    return print("Created %s new players" % i)


def update_teams(cursor):
    cursor.execute("SELECT team_id FROM nba_teams")
    team_ids = cursor.fetchall()
    team_ids = [team['team_id'] for team in team_ids]

    team_info = get_teams()
    i = 0
    for team in team_info:
        if team['id'] not in team_ids:
            i += 1
            print("Created team %s: %s (%s)" % (i,
                                                team['full_name'],
                                                team['id']))
            cursor.callproc('create_nba_team',
                            (team['id'],
                             team['full_name'],
                             team['abbreviation'],
                             team['nickname'],
                             team['city'],
                             team['state'],
                             team['year_founded']))
        # else:
        #     print("Team %s (%s) already exists" % (team['full_name'],
        #                                            team['id']))

    return print("Created %s new teams" % i)


def combine_team_games(df, keep_method='home'):
    '''Combine a TEAM_ID-GAME_ID unique table into rows by game. Slow.

        Parameters
        ----------
        df : Input DataFrame.
        keep_method : {'home', 'away', 'winner', 'loser', ``None``}, default 'home'
            - 'home' : Keep rows where TEAM_A is the home team.
            - 'away' : Keep rows where TEAM_A is the away team.
            - 'winner' : Keep rows where TEAM_A is the losing team.
            - 'loser' : Keep rows where TEAM_A is the winning team.
            - ``None`` : Keep all rows. Will result in an output DataFrame the same
                length as the input DataFrame.

        Returns
        -------
        result : DataFrame
    '''
    # Join every row to all others with the same game ID.
    joined = pd.merge(df, df, suffixes=['_A', '_B'],
                      on=['SEASON_ID', 'GAME_ID', 'GAME_DATE'])
    # Filter out any row that is joined to itself.
    result = joined[joined.TEAM_ID_A != joined.TEAM_ID_B]
    # Take action based on the keep_method flag.
    if keep_method is None:
        # Return all the rows.
        pass
    elif keep_method.lower() == 'home':
        # Keep rows where TEAM_A is the home team.
        result = result[result.MATCHUP_A.str.contains(' vs. ')]
    elif keep_method.lower() == 'away':
        # Keep rows where TEAM_A is the away team.
        result = result[result.MATCHUP_A.str.contains(' @ ')]
    elif keep_method.lower() == 'winner':
        result = result[result.WL_A == 'W']
    elif keep_method.lower() == 'loser':
        result = result[result.WL_A == 'L']
    else:
        raise ValueError(f'Invalid keep_method: {keep_method}')
    return result


def update_games(cursor, season):
    # Get list of existing game IDs
    cursor.execute("SELECT game_id FROM games")
    existing_game_ids = cursor.fetchall()
    existing_game_ids = [game['game_id'] for game in existing_game_ids]

    # Create list of new game IDs
    new_game_ids = []

    # Get list of teams
    cursor.execute("SELECT team_id, team_name FROM nba_teams")
    nba_teams = cursor.fetchall()
    nba_teams = [team for team in nba_teams if team['team_id'] != -1]

    for team in nba_teams:
        time.sleep(0.5)
        print("Checking for new games for %s in %s Season" % (team['team_name'], season))
        game_finder = LeagueGameFinder(team_id_nullable=team['team_id'],
                                       season_nullable=season,
                                       season_type_nullable='Regular Season')
        games = game_finder.get_dict()

        keys = games['resultSets'][0]['headers']
        values = games['resultSets'][0]['rowSet']

        if len(keys) == len(values):
            game_dict = dict(zip(keys, values))
            if game_dict['GAME_ID'] not in existing_game_ids:
                print("Found new game: %s" % game_dict['GAME_ID'])
                new_game_ids.append(game_dict['GAME_ID'])

    if len(new_game_ids) == 0:
        return print("No new games found for %s Season" % season)
    else:
        i = 0
        result = LeagueGameFinder()
        all_games = result.get_data_frames()[0]
        for game in new_game_ids:
            full_game = all_games[all_games['GAME_ID'] == game]
            game_df = combine_team_games(full_game)
            if not game_df['WL_A'].empty and not game_df['WL_B'].empty:
                if game_df['WL_A'].iloc[0] == 'W':
                    game_df['WINNER'] = game_df['TEAM_ID_A']
                elif game_df['WL_B'].iloc[0] == 'W':
                    game_df['WINNER'] = game_df['TEAM_ID_B']
                else:
                    game_df['WINNER'] = None
                GAME_ID = game_df['GAME_ID'].iloc[0]
                DATE = game_df['GAME_DATE'].iloc[0]
                TEAM_ID_A = game_df['TEAM_ID_A'].iloc[0]
                TEAM_ID_B = game_df['TEAM_ID_B'].iloc[0]
                PTS_A = game_df['PTS_A'].iloc[0]
                PTS_B = game_df['PTS_B'].iloc[0]
                WINNER = game_df['WINNER'].iloc[0]

                cursor.callproc('create_game',
                                (GAME_ID,
                                 DATE,
                                 TEAM_ID_A,
                                 TEAM_ID_B,
                                 PTS_A,
                                 PTS_B,
                                 WINNER))
                print("Created game %s with game id %s" % (game_df['MATCHUP'], GAME_ID))
                i += 1

    return print("Created %s new games" % i)


def update_player_stats(cursor, player_id, team_id, season):
    # Gets the game log for each season
    # TODO: Can be used to get the game log for each player for each game
    player_game_log = PlayerGameLog(player_id=player_id,
                                    season=season,
                                    season_type_all_star='Regular Season').get_data_frames()[0]

    for i in range(len(player_game_log)):
        game_id = player_game_log['Game_ID'].iloc[i]
        points = player_game_log['PTS'].iloc[i]
        assists = player_game_log['AST'].iloc[i]
        rebounds = player_game_log['REB'].iloc[i]
        steals = player_game_log['STL'].iloc[i]
        blocks = player_game_log['BLK'].iloc[i]
        turnovers = player_game_log['TOV'].iloc[i]
        fouls = player_game_log['PF'].iloc[i]
        minutes_played = player_game_log['MIN'].iloc[i]

        cursor.callproc('create_player_game_stats',
                        (player_id,
                         game_id,
                         team_id,
                         points,
                         assists,
                         rebounds,
                         steals,
                         blocks,
                         turnovers,
                         fouls,
                         minutes_played))


def create_all_player_stats(cursor):
    cursor.execute("SELECT player_id FROM nba_players")
    all_players = cursor.fetchall()
    player_ids = [player['player_id'] for player in all_players]

    i = 0
    for player in player_ids:
        cursor.execute("SELECT * FROM player_team_link WHERE player_id = %s", (player,))
        result = cursor.fetchone()
        if result is not None:
            team_id = result['team_id']
            seasonStart = result['season_year']
            seasonEnd = abs(seasonStart + 1) % 100
            season = str(seasonStart) + '-' + str(seasonEnd)
            update_player_stats(cursor, player, team_id, season)
            print("Updated player stats for player %s" % player)
            i += 1

    return print("Updated stats for %s players" % i)


def main():
    load_dotenv()
    DB_HOST = os.getenv('DB_HOST') if os.getenv('DB_HOST') is not None else input(
        "Enter your host: ")
    DB_USER = os.getenv('DB_USER') if os.getenv('DB_USER') is not None else input(
        "Enter your username: ")
    DB_PASS = os.getenv('DB_PASS') if os.getenv('DB_PASS') is not None else input(
        "Enter your password: ")
    DB_NAME = os.getenv('DB_NAME') if os.getenv('DB_NAME') is not None else input(
        "Enter your database name: ")
    try:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASS,
                                     db=DB_NAME,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        connection.autocommit(True)
        cursor = connection.cursor()

        # if input("Update all teams to current status? (y/n): ") == 'y':
        #     update_teams(cursor)
        # if input("Update all players to current status? (y/n): ") == 'y':
        #     update_players(cursor)
        # if input("Update all games to current status? (y/n): ") == 'y':
        #     season = input("Enter season to update (e.g. 2022-23): ")
        #     update_games(cursor, season)
        # if input("Update all player stats to current status? (y/n): ") == 'y':
        #     update_player_stats(cursor)

        create_all_player_stats(cursor)

        cursor.close()
        connection.close()

    except pymysql.Error as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))


if __name__ == '__main__':
    main()
