# Create a new player
DROP PROCEDURE IF EXISTS create_player;
CREATE PROCEDURE create_player(
    IN first_name_p VARCHAR(50),
    IN last_name_p VARCHAR(50),
    IN birth_date_p DATE,
    IN height_p DECIMAL(4,2)
    IN position_p VARCHAR(255),
    IN jersey_number_p INT,
    IN is_active_p BOOLEAN,
    IN season_exp_p INT,
    IN team_id_p INT,
    IN season_year_p INT)
BEGIN
    # Create variable to hold player_id_p
    DECLARE player_id_p INT;

    # Find the max player_id plus one
    SELECT MAX(player_id) + 1
    INTO player_id_p
    FROM players;

    # Insert into player table
    INSERT INTO players (player_id,
                         first_name,
                         last_name,
                         birth_date,
                         height,
                         jersey_number,
                         is_active,
                         season_exp)
    VALUES (player_id_p,
            first_name_p,
            last_name_p,
            birth_date_p,
            height_p,
            jersey_number_p,
            is_active_p,
            season_exp_p);

    # Insert into player_position_link table
    INSERT INTO player_position_link (player_id,
                                      position_id)
    VALUES (player_id_p,
            position_p);

    # Insert into player_team_link table
    INSERT INTO player_team_link (player_id,
                                  team_id,
                                  season_year)
    VALUES (player_id_p,
            team_id_p,
            season_year_p);
END;


# View player by name procedure
# DROP PROCEDURE IF EXISTS view_player_by_name;
# CREATE PROCEDURE view_player_by_name(IN first_name_p VARCHAR(255), IN last_name_p VARCHAR(255))
# BEGIN
#     SELECT *
#     FROM players
#     WHERE first_name = first_name_p
#       AND last_name = last_name_p;
# END;

# View player by id procedure
DROP PROCEDURE IF EXISTS view_player_by_id;
CREATE PROCEDURE view_player_by_id(IN player_id_p INT)
BEGIN
    SELECT *
    FROM players,
         player_position_link,
         player_team_link,
         positions,
         teams
    WHERE players.player_id = player_id_p
      AND player_position_link.player_id = player_id_p
      AND player_team_link.player_id = player_id_p
      AND positions.position_id = player_position_link.position_id
      AND teams.team_id = player_team_link.team_id;
END;

# Update player procedure
DROP PROCEDURE IF EXISTS update_player;
CREATE PROCEDURE update_player(
    IN player_id_p INT,
    IN first_name_p VARCHAR(50),
    IN last_name_p VARCHAR(50),
    IN birth_date_p DATE,
    IN height_p DECIMAL(4,2),
    IN position_p VARCHAR(255),
    IN jersey_number_p INT,
    IN is_active_p BOOLEAN,
    IN season_exp_p INT,
    IN team_id_p INT,
    IN season_year_p INT)
BEGIN
    # Update player table
    UPDATE players
    SET first_name = first_name_p,
        last_name = last_name_p,
        birth_date = birth_date_p,
        height = height_p,
        jersey_number = jersey_number_p,
        is_active = is_active_p,
        season_exp = season_exp_p
    WHERE player_id = player_id_p;

    # Update player_position_link table
    UPDATE player_position_link
    SET position_id = position_p
    WHERE player_id = player_id_p;

    # Update player_team_link table
    UPDATE player_team_link
    SET team_id = team_id_p,
        season_year = season_year_p
    WHERE player_id = player_id_p;
END;

# Delete player procedure
DROP PROCEDURE IF EXISTS delete_player;
CREATE PROCEDURE delete_player(IN player_id_p INT)
BEGIN
    # Delete from player table
    DELETE FROM players
    WHERE player_id = player_id_p;

    # Delete from player_position_link table
    DELETE FROM player_position_link
    WHERE player_id = player_id_p;

    # Delete from player_team_link table
    DELETE FROM player_team_link
    WHERE player_id = player_id_p;

    # Delete from player_stats table
    DELETE FROM player_game_stats
    WHERE player_id = player_id_p;
END;

