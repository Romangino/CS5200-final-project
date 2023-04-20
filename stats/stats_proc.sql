# Procedure to create a new players stats record in player_game_stats table
DROP PROCEDURE IF EXISTS create_player_game_stats;
CREATE PROCEDURE create_player_game_stats(
    IN player_id_p INT,
    IN game_id_p INT,
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
    # Handle player_id not being in the players table
    IF NOT EXISTS (SELECT * FROM players WHERE player_id = player_id_p) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Player ID does not exist in players table';
    END IF;

    # Handle game_id not being in the games table
    IF NOT EXISTS (SELECT * FROM games WHERE game_id = game_id_p) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Game ID does not exist in games table';
    END IF;

    # Handle player_id and game_id being in the player_game_stats table
    IF EXISTS (SELECT *
               FROM player_game_stats
               WHERE player_id = player_id_p
                 AND game_id = game_id_p) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Player ID and Game ID already exist in player_game_stats table';
    END IF;

    # Handle points being less than 0
    IF points_p < 0 OR
       assists_p < 0 OR
       rebounds_p < 0 OR
       steals_p < 0 OR
       blocks_p < 0 OR
       turnovers_p < 0 OR
       fouls_p < 0 OR
       minutes_played_p < 0
    THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Values cannot be less than 0';
    END IF;

    INSERT INTO player_game_stats (player_id,
                                   game_id,
                                   points,
                                   assists,
                                   rebounds,
                                   steals,
                                   blocks,
                                   turnovers,
                                   fouls,
                                   minutes_played)
    VALUES (player_id_p,
            game_id_p,
            points_p,
            assists_p,
            rebounds_p,
            steals_p,
            blocks_p,
            turnovers_p,
            fouls_p,
            minutes_played_p);
END;

# Procedure to find player game stats by player_id and game_id
DROP PROCEDURE IF EXISTS get_stat;
CREATE PROCEDURE get_stat(
    IN player_id_p INT,
    IN game_id_p INT
)
BEGIN
    SELECT *
    FROM player_game_stats
    WHERE player_id = player_id_p
      AND game_id = game_id_p;
END;

# Procedure to get games for player
DROP PROCEDURE IF EXISTS get_games_for_player;
CREATE PROCEDURE get_games_for_player(
    IN player_id_p INT
)
BEGIN
    SELECT *
    FROM player_game_stats
    WHERE player_id = player_id_p;
END;

# Procedure to get players that don't have stats for a game
DROP PROCEDURE IF EXISTS get_stats;
CREATE PROCEDURE get_stats()
BEGIN
    SELECT *
    FROM player_game_stats;
END;