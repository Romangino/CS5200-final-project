# Get all teams currently in teams table
DROP PROCEDURE IF EXISTS get_teams;
CREATE PROCEDURE get_teams()
BEGIN
    SELECT *
    FROM teams;
END;
