# Procedure to create game in games table
DROP PROCEDURE IF EXISTS create_game;
CREATE PROCEDURE create_game(
    IN team1_id_p INT,
    IN team2_id_p INT,
    IN team1_pts_p INT,
    IN team2_pts_p INT,
    IN game_date_p DATE,
    IN winner_id_p INT)
BEGIN
    DECLARE game_id_p INT;

    # Create game_id with the max game_id + 1
    SELECT MAX(game_id) + 1
    INTO game_id_p
    FROM games;


    INSERT INTO games (game_id,
                       team1_id,
                       team2_id,
                       team1_pts,
                       team2_pts,
                       game_date,
                       winner_id)
    VALUES (game_id_p,
            team1_id_p,
            team2_id_p,
            team1_pts_p,
            team2_pts_p,
            game_date_p,
            winner_id_p);
END;

# Procedure to view game by game_id
DROP PROCEDURE IF EXISTS view_game_by_id;
CREATE PROCEDURE view_game_by_id(
    IN game_id_p INT)
BEGIN
    SELECT *
    FROM games
    WHERE game_id = game_id_p;
END;

# Procedure to update game by game_id
DROP PROCEDURE IF EXISTS update_game;
CREATE PROCEDURE update_game(
    IN game_id_p INT,
    IN team1_id_p INT,
    IN team2_id_p INT,
    IN team1_pts_p INT,
    IN team2_pts_p INT,
    IN game_date_p DATE,
    IN winner_id_p INT)
BEGIN
    UPDATE games
    SET team1_id = team1_id_p,
        team2_id = team2_id_p,
        team1_pts = team1_pts_p,
        team2_pts = team2_pts_p,
        game_date = game_date_p,
        winner_id = winner_id_p
    WHERE game_id = game_id_p;
END;


