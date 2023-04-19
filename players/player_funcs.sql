USE project_testdb;
DROP FUNCTION IF EXISTS get_player_id;
delimiter $$
CREATE FUNCTION get_player_id(first_name_p VARCHAR(50), last_name_p VARCHAR(50))
	RETURNS INT DETERMINISTIC READS SQL DATA
    BEGIN
		DECLARE ret_int INT DEFAULT NULL;
        SELECT player_id INTO ret_int FROM players
			WHERE first_name = first_name_p
            AND last_name = last_name_p;
        RETURN(ret_int);
	END$$
delimiter ;