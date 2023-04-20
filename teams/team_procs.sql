# Create a new team in the teams table
DROP PROCEDURE IF EXISTS create_team;
CREATE PROCEDURE create_team(
    IN team_name_p VARCHAR(50),
    IN abbreviation_p VARCHAR(3),
    IN nickname_p VARCHAR(50),
    IN city_p VARCHAR(50),
    IN state_p VARCHAR(50),
    IN year_founded_p INT)
BEGIN
    DECLARE team_exists INT;
    DECLARE team_id_p INT;

    # Check if team already exists
    SELECT COUNT(*)
    INTO team_exists
    FROM teams
    WHERE team_name = team_name_p
       OR abbreviation = abbreviation_p
       OR nickname = nickname_p;

    IF team_exists > 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Team already exists';
    END IF;

    # Find the next team_id
    SELECT MAX(team_id) + 1
    INTO team_id_p
    FROM teams;


    INSERT INTO teams (team_id,
                       team_name,
                       abbreviation,
                       nickname,
                       city,
                       state,
                       year_founded)
    VALUES (team_id_p,
            team_name_p,
            abbreviation_p,
            nickname_p,
            city_p,
            state_p,
            year_founded_p);
END;


# Get all teams currently in teams table
DROP PROCEDURE IF EXISTS get_teams;
CREATE PROCEDURE get_teams()
BEGIN
    SELECT *
    FROM teams;
END;

# Get a specific team by team_id
DROP PROCEDURE IF EXISTS view_team_by_id;
CREATE PROCEDURE view_team_by_id(
    IN team_id_p INT)
BEGIN
    SELECT *
    FROM teams
    WHERE team_id = team_id_p;
END;

# Update a team's information
DROP PROCEDURE IF EXISTS update_team;
CREATE PROCEDURE update_team(
    IN team_id_p INT,
    IN team_name_p VARCHAR(50),
    IN abbreviation_p VARCHAR(3),
    IN nickname_p VARCHAR(50),
    IN city_p VARCHAR(50),
    IN state_p VARCHAR(50),
    IN year_founded_p INT)
BEGIN
    UPDATE teams
    SET team_name    = team_name_p,
        abbreviation = abbreviation_p,
        nickname     = nickname_p,
        city         = city_p,
        state        = state_p,
        year_founded = year_founded_p
    WHERE team_id = team_id_p;
END;

# Delete a team from the teams table
DROP PROCEDURE IF EXISTS delete_team;
CREATE PROCEDURE delete_team(
    IN team_id_p INT)
BEGIN
    DELETE
    FROM teams
    WHERE team_id = team_id_p;
END;


