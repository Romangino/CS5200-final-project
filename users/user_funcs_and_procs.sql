USE project_testdb;

DROP FUNCTION IF EXISTS get_player_id;
delimiter $$
CREATE FUNCTION get_player_id(first_name_p VARCHAR(50), last_name_p VARCHAR(50))
	RETURNS INT DETERMINISTIC READS SQL DATA
    BEGIN
		DECLARE ret_int INT;
        SELECT player_id INTO ret_int FROM players
			WHERE first_name = first_name_p
            AND last_name = last_name_p;
        RETURN(ret_int);
	END$$
delimiter ;

DROP FUNCTION IF EXISTS get_team_id;
delimiter $$
CREATE FUNCTION get_team_id(city_p VARCHAR(50), name_p VARCHAR(50))
	RETURNS INT DETERMINISTIC READS SQL DATA
    BEGIN
		DECLARE ret_int INT;
        SELECT team_id INTO ret_int FROM teams
			WHERE city = city_p
            AND nickname = name_p;
        RETURN(ret_int);
	END$$
delimiter ;

DROP PROCEDURE IF EXISTS get_player_info;
delimiter $$
CREATE PROCEDURE get_player_info(player_id_p INT)
    BEGIN
		SELECT first_name, last_name, team_name, position_name, birth_date, height, jersey_number, is_active, season_exp FROM players
			NATURAL JOIN player_team_link
            NATURAL JOIN teams
			NATURAL JOIN player_position_link
            NATURAL JOIN positions
				WHERE player_id = player_id_p;
	END$$
delimiter ;

DROP PROCEDURE IF EXISTS get_player_stats;
delimiter $$
CREATE PROCEDURE get_player_stats(player_id_p INT)
    BEGIN
		SELECT ROUND(AVG(points), 1) AS avg_ppg, ROUND(AVG(assists), 1) AS avg_apg, ROUND(AVG(rebounds), 1) AS avg_rpg, 
        ROUND(AVG(steals), 1) AS avg_spg, ROUND(AVG(blocks), 1) AS avg_bpg, ROUND(AVG(turnovers), 1) AS avg_tpg, 
        ROUND(AVG(fouls), 1) AS avg_fpg, ROUND(AVG(minutes_played), 1) AS avg_mpg FROM player_game_stats
        NATURAL JOIN games
			WHERE player_id = player_id_p;
	END$$
delimiter ;

DROP PROCEDURE IF EXISTS get_team_info;
delimiter $$
CREATE PROCEDURE get_team_info(team_id_p INT)
    BEGIN
		DECLARE wins INT;
        DECLARE losses INT;
        
		SELECT COUNT(*) INTO wins FROM games AS g
		INNER JOIN teams AS t ON t.team_id = g.winner_id
			WHERE t.team_id = team_id_p
				GROUP BY winner_id;
		
        SELECT COUNT(*) INTO losses FROM games AS g
		INNER JOIN teams AS t ON t.team_id = g.team1_id
		OR t.team_id = g.team2_id
			WHERE t.team_id != g.winner_id
            AND t.team_id = team_id_p
				GROUP BY team_name;
		
		SELECT team_name, abbreviation, state, year_founded, wins, losses FROM teams
			WHERE team_id = team_id_p;
	END$$
delimiter ;

DROP PROCEDURE IF EXISTS get_team_stats;
delimiter $$
CREATE PROCEDURE get_team_stats(team_id_p INT)
    BEGIN
		DECLARE partial_total1 INT;
        DECLARE partial_total2 INT;
        DECLARE total_games INT;
        
		SELECT SUM(team1_pts) INTO partial_total1 FROM games
			WHERE team1_id = team_id_p;
		
        SELECT SUM(team2_pts) INTO partial_total2 FROM games
			WHERE team2_id = team_id_p;
		
        SELECT COUNT(*) INTO total_games FROM games
			WHERE team1_id = team_id_p
            OR team2_id = team_id_p;
            
		SELECT ROUND((partial_total1 + partial_total2) / total_games, 1) AS avg_ppg;
	END$$
delimiter ;

DROP PROCEDURE IF EXISTS get_highest_scoring_games;
delimiter $$
CREATE PROCEDURE get_highest_scoring_games()
    BEGIN
		SELECT game_date, t1.team_name AS team1, team1_pts, t2.team_name AS team2, team2_pts, team1_pts + team2_pts AS tot_pts FROM games AS g
			INNER JOIN teams AS t1 ON g.team1_id = t1.team_id
			INNER JOIN teams AS t2 ON g.team2_id = t2.team_id
				ORDER BY tot_pts DESC
					LIMIT 5;
	END$$
delimiter ;

DROP PROCEDURE IF EXISTS get_lowest_scoring_games;
delimiter $$
CREATE PROCEDURE get_lowest_scoring_games()
    BEGIN
		SELECT game_date, t1.team_name AS team1, team1_pts, t2.team_name AS team2, team2_pts, team1_pts + team2_pts AS tot_pts FROM games AS g
			INNER JOIN teams AS t1 ON g.team1_id = t1.team_id
			INNER JOIN teams AS t2 ON g.team2_id = t2.team_id
				ORDER BY tot_pts ASC
					LIMIT 5;
	END$$
delimiter ;

DROP PROCEDURE IF EXISTS get_most_recent_games;
delimiter $$
CREATE PROCEDURE get_most_recent_games()
    BEGIN
		SELECT game_date, t1.team_name AS team1, team1_pts, t2.team_name AS team2, team2_pts, t3.team_name AS winner FROM games AS g
			INNER JOIN teams AS t1 ON g.team1_id = t1.team_id
			INNER JOIN teams AS t2 ON g.team2_id = t2.team_id
			INNER JOIN teams AS t3 ON g.winner_id = t3.team_id
				ORDER BY game_date DESC
					LIMIT 5;
	END$$
delimiter ;

DROP PROCEDURE IF EXISTS get_teams_tot_pts;
delimiter $$
CREATE PROCEDURE get_teams_tot_pts()
    BEGIN
		SELECT tot1.team_name, home_team_pts + away_team_pts AS tot_pts FROM (
			SELECT team_name, SUM(team1_pts) AS home_team_pts FROM teams AS t1
				INNER JOIN games AS g1 ON t1.team_id = g1.team1_id
					GROUP BY team_name
		) AS tot1
			INNER JOIN (
				SELECT team_name, SUM(team2_pts) AS away_team_pts FROM teams AS t2
					INNER JOIN games AS g2 ON t2.team_id = g2.team2_id
						GROUP BY team_name
				) AS tot2 ON tot1.team_name = tot2.team_name
					GROUP BY team_name;
	END$$
delimiter ;

DROP PROCEDURE IF EXISTS get_pos_stats;
delimiter $$
CREATE PROCEDURE get_pos_stats()
    BEGIN
		SELECT position_name, SUM(points) AS points, SUM(assists) AS assists, SUM(rebounds) AS rebounds, 
		SUM(steals) AS steals, SUM(blocks) AS blocks, SUM(turnovers) AS turnovers, 
		SUM(fouls) AS fouls, SUM(minutes_played) AS minutes FROM positions AS p
			INNER JOIN player_position_link AS ppl ON p.position_id = ppl.position_id
			INNER JOIN player_game_stats AS pgs ON ppl.player_id = pgs.player_id
				GROUP BY position_name;
	END$$
delimiter ;

DROP PROCEDURE IF EXISTS get_pos_stats_pct;
delimiter $$
CREATE PROCEDURE get_pos_stats_pct()
    BEGIN
		SELECT position_name, points, assists, rebounds, steals, blocks, turnovers, fouls, minutes_played FROM positions AS p
			INNER JOIN player_position_link AS ppl ON p.position_id = ppl.position_id
			INNER JOIN player_game_stats AS pgs ON ppl.player_id = pgs.player_id;
	END$$
delimiter ;