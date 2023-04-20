# Procedure to view all positions
DROP PROCEDURE IF EXISTS get_positions;
CREATE PROCEDURE get_positions()
BEGIN
    SELECT *
    FROM positions;
END;

# Procedure to create a new position
DROP PROCEDURE IF EXISTS create_position;
CREATE PROCEDURE create_position(
    IN position_name_p VARCHAR(50)
)
BEGIN
    INSERT INTO positions (position_name)
    VALUES (position_name_p);
END;