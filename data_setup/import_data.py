import time
import pandas as pd
import pymysql
from nba_api.stats.endpoints import commonplayerinfo, PlayerGameLog
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.library.parameters import SeasonTypeAllStar
from nba_api.stats.static.players import *
from nba_api.stats.static.teams import *


# create player
def import_players(cursor):
    """
    Pulls from NBA API to update players
    :param cursor:
    :return:
    """
    # Find all player_ids from players table
    print("Updating Players from API...")
    cursor.callproc('get_players')
    existing_player_ids = cursor.fetchall()
    existing_player_ids = [player['player_id'] for player in existing_player_ids]

    # Get all active players from nba_api
    player_info = get_active_players()
    players_added = 0
    for player in player_info:
        if player['id'] not in existing_player_ids:
            try:
                players_added += 1
                playerCommonInfo = commonplayerinfo.CommonPlayerInfo(player['id'])
                player_api = playerCommonInfo.get_dict()
                keys = player_api['resultSets'][0]['headers']
                values = player_api['resultSets'][0]['rowSet'][0]
                if len(keys) != len(values):
                    players_added -= 1
                    continue
                player_dict = dict(zip(keys, values))
                if player_dict['DRAFT_ROUND'] == 'Undrafted':
                    players_added -= 1
                    continue

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
                else:
                    cursor.callproc('get_positions')
                    existing_positions = cursor.fetchall()
                    existing_positions = [position['position_name'] for position in
                                          existing_positions]
                    if player_dict['POSITION'] not in existing_positions:
                        cursor.callproc('create_position',
                                        (player_dict['POSITION'],))
                    else:
                        player_dict.update(
                            {'POSITION': existing_positions.index(player_dict['POSITION'])})
                cursor.callproc('create_player_api',
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
                time.sleep(1)
                print("Creating player: %s on the %s" % (
                    player_dict['DISPLAY_FIRST_LAST'], player_dict['TEAM_NAME']))
            except pymysql.Error as e:
                print("Error %d: %s" % (e.args[0], e.args[1]))
                players_added -= 1
                continue
    return print("Added %s players to the database." % players_added)


def import_teams(cursor):
    """
    Pulls from NBA API to update teams
    :param cursor:
    :return:
    """
    print("Updating Teams from API...")
    cursor.callproc('get_teams')
    existing_team_ids = cursor.fetchall()
    existing_team_ids = [team['team_id'] for team in existing_team_ids]

    team_info = get_teams()
    teams_added = 0
    for team in team_info:
        if team['id'] not in existing_team_ids:
            try:
                teams_added += 1
                print("Created team: %s (%s)" % (team['full_name'],
                                                 team['id']))
                cursor.callproc('create_team',
                                (team['full_name'],
                                 team['abbreviation'],
                                 team['nickname'],
                                 team['city'],
                                 team['state'],
                                 team['year_founded']))
            except pymysql.Error as e:
                print("Error %d: %s" % (e.args[0], e.args[1]))
                teams_added -= 1
                continue

    return print("Added %s teams to the database." % teams_added)


def combine_team_games(df, keep_method='home'):
    """Combine a TEAM_ID-GAME_ID unique table into rows by game. Slow.

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
    """
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


def import_games(cursor, season):
    """
    Pulls from NBA API to update games
    :param cursor:
    :param season:
    :return:
    """
    # Get list of existing game IDs
    cursor.callproc('get_games')
    existing_game_ids = cursor.fetchall()
    existing_game_ids = [game['game_id'] for game in existing_game_ids]

    # Create list of new game IDs
    new_game_ids = []

    # Get list of teams
    cursor.callproc('get_teams')
    team_results = cursor.fetchall()
    team_results.pop(0)
    for team in team_results:
        print("Checking for new games for %s in %s Season" % (team['team_name'], season))
        for season_type in [SeasonTypeAllStar.regular, SeasonTypeAllStar.playoffs]:
            time.sleep(1)
            game_finder = leaguegamefinder.LeagueGameFinder(team_id_nullable=team['team_id'],
                                                            season_nullable=season,
                                                            season_type_nullable=season_type)
            games = game_finder.get_dict()

            keys = games['resultSets'][0]['headers']
            values = games['resultSets'][0]['rowSet']
            for value in values:
                if len(value) == len(keys):
                    game_dict = dict(zip(keys, value))
                    game_id = int(game_dict['GAME_ID'])
                    if game_id not in existing_game_ids and game_id not in new_game_ids:
                        print("Found new game: %s" % game_dict['GAME_ID'])
                        new_game_ids.append(game_dict['GAME_ID'])

    if len(new_game_ids) == 0:
        return print("No new games found for %s Season" % season)
    else:
        games_added = 0
        for season_type in [SeasonTypeAllStar.regular, SeasonTypeAllStar.playoffs]:
            result = leaguegamefinder.LeagueGameFinder(season_nullable=season,
                                                       season_type_nullable=season_type)
            all_games = result.get_data_frames()[0]
            for game in new_game_ids:
                try:
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

                        cursor.callproc('create_game_api',
                                        (GAME_ID,
                                         TEAM_ID_A,
                                         TEAM_ID_B,
                                         PTS_A,
                                         PTS_B,
                                         DATE,
                                         WINNER))
                        print("Created game with game id %s" % GAME_ID)
                        games_added += 1
                except pymysql.Error as e:
                    print("Error %d: %s" % (e.args[0], e.args[1]))

    return print("Created %s new games" % games_added)


def import_player_stats(cursor, season):
    """
    Imports player stats for a given season
    :param cursor:
    :param season:
    :return:
    """
    cursor.callproc('get_players')
    all_players = cursor.fetchall()
    all_players = [player for player in all_players if player['is_active'] == 1]
    player_stats_added = 0
    for player in all_players:
        print("Checking stats for: %s %s (%s)" % (player['first_name'],
                                                  player['last_name'],
                                                  player['player_id']))
        for season_type in [SeasonTypeAllStar.regular, SeasonTypeAllStar.playoffs]:
            # Gets the game log for each season
            player_game_log = PlayerGameLog(player_id=player['player_id'],
                                            season=season,
                                            season_type_all_star=season_type).get_data_frames()[0]
            for i in range(len(player_game_log)):
                cursor.callproc('get_stat',
                                (player['player_id'], player_game_log['Game_ID'].iloc[i]))
                stat = cursor.fetchone()
                if stat is None:
                    game_id = player_game_log['Game_ID'].iloc[i]
                    points = player_game_log['PTS'].iloc[i]
                    assists = player_game_log['AST'].iloc[i]
                    rebounds = player_game_log['REB'].iloc[i]
                    steals = player_game_log['STL'].iloc[i]
                    blocks = player_game_log['BLK'].iloc[i]
                    turnovers = player_game_log['TOV'].iloc[i]
                    fouls = player_game_log['PF'].iloc[i]
                    minutes_played = player_game_log['MIN'].iloc[i]

                    try:
                        cursor.callproc('create_player_game_stats',
                                        (player['player_id'],
                                         game_id,
                                         points,
                                         assists,
                                         rebounds,
                                         steals,
                                         blocks,
                                         turnovers,
                                         fouls,
                                         minutes_played))
                    except pymysql.Error as e:
                        print("Error %d: %s" % (e.args[0], e.args[1]))
                        continue
                    print("Updated player stats for %s %s (%s)" % (player['first_name'],
                                                                   player['last_name'],
                                                                   player['player_id']))
                    player_stats_added += 1
        time.sleep(0.25)

    return print("Updated stats for %s players" % player_stats_added)
