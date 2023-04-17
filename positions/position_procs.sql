# Procedure to view all positions
DROP PROCEDURE IF EXISTS get_positions;
CREATE PROCEDURE get_positions()
BEGIN
    SELECT *
    FROM positions;
END;