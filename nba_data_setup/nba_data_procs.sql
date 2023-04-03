# Create nba team with procedure
DROP PROCEDURE IF EXISTS create_nba_team;
CREATE PROCEDURE create_nba_team(
    IN team_id_p INT,
    IN team_name_p VARCHAR(50),
    IN abbreviation_p VARCHAR(3),
    IN nickname_p VARCHAR(50),
    IN city_p VARCHAR(50),
    IN state_p VARCHAR(50),
    IN year_founded_p INT
)
BEGIN
    INSERT INTO teams (team_id, team_name, abbreviation, nickname, city, state, year_founded)
    VALUES (team_id_p, team_name_p, abbreviation_p, nickname_p, city_p, state_p, year_founded_p);
END;


# Create nba player with procedure that inserts a new player and links them to a team
DROP PROCEDURE IF EXISTS create_nba_player;
CREATE PROCEDURE create_nba_player(
    IN player_id_p INT,
    IN first_name_p VARCHAR(50),
    IN last_name_p VARCHAR(50),
    IN birth_date_p DATE,
    IN height_p DECIMAL(4, 2),
    IN position_p VARCHAR(50),
    IN jersey_number_p INT,
    IN is_active_p BOOLEAN,
    IN season_exp_p INT,
    IN team_id_p INT,
    IN season_year_p INT
)
BEGIN
    # Create a handler for error 1452
    DECLARE EXIT HANDLER FOR 1452
        BEGIN
            # Change team id to be -1 if it is null
            SET team_id_p = -1;
        END;

    DECLARE EXIT HANDLER FOR 1048
        BEGIN
            # Change season year to be -1 if it is null
            SET season_year_p = -1;
        END;

    # Insert position into the positions table
    # If the position already exists, it will not be inserted
    IF NOT EXISTS(SELECT * FROM positions WHERE position_name = position_p)
    THEN
        INSERT INTO positions (position_name)
        VALUES (position_p);
    END IF;

    # Insert the player into the nba_players table
    INSERT INTO players (player_id, first_name, last_name, birth_date, height, jersey_number,
                         is_active, season_exp)
    VALUES (player_id_p, first_name_p, last_name_p, birth_date_p, height_p, jersey_number_p,
            is_active_p, season_exp_p);

    # Insert the player into the player_position_link table
    INSERT INTO player_position_link (player_id, position_id)
    VALUES (player_id_p, (SELECT position_id FROM positions WHERE position_name = position_p));

    # Insert the player into the player_team_link table
    INSERT INTO player_team_link (player_id, team_id, season_year)
    VALUES (player_id_p, team_id_p, season_year_p);

END;


#  Create procedure to create a game
DROP PROCEDURE IF EXISTS create_game;
CREATE PROCEDURE create_game(
    IN game_id_p INT,
    IN game_date_p DATE,
    IN team1_id_p INT,
    IN team2_id_p INT,
    IN team1_pts_p INT,
    IN team2_pts_p INT,
    IN winner_id_p INT
)
BEGIN
    # Create a handler for error 1452
    DECLARE EXIT HANDLER FOR 1452
        BEGIN
            # Rollback the transaction
            ROLLBACK;
        END;

    # Insert the game into the games table
    INSERT INTO games (game_id, game_date, team1_id, team2_id, team1_pts, team2_pts, winner_id)
    VALUES (game_id_p, game_date_p, team1_id_p, team2_id_p, team1_pts_p, team2_pts_p, winner_id_p);
END;


# Create procedure to create a player game stat
DROP PROCEDURE IF EXISTS create_player_game_stats;
CREATE PROCEDURE create_player_game_stats(
    IN player_id_p INT,
    IN game_id_p INT,
    IN team_id_p INT,
    IN points_p INT,
    IN assists_p INT,
    IN rebounds_p INT,
    IN steals_p INT,
    IN blocks_p INT,
    IN turnovers_p INT,
    IN fouls_p INT,
    IN minutes_played_p INT
)
BEGIN
    # Create a handler for error 1452
    DECLARE EXIT HANDLER FOR 1452
        BEGIN
            # Rollback the transaction
            ROLLBACK;
        END;

    # Insert the player game stats into the player_game_stats table
    INSERT INTO player_game_stats (player_id, game_id, team_id, points, assists, rebounds,
                                   steals, blocks, turnovers, fouls, minutes_played)
    VALUES (player_id_p, game_id_p, team_id_p, points_p, assists_p, rebounds_p,
            steals_p, blocks_p, turnovers_p, fouls_p, minutes_played_p);
END;