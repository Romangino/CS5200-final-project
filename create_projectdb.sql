DROP DATABASE IF EXISTS project_testdb;
CREATE DATABASE project_testdb;

USE project_testdb;

# Create a nba player table with the following columns:
# player_id, first_name, last_name, is_active
DROP TABLE IF EXISTS players;
CREATE TABLE players
(
    player_id     INT         NOT NULL,
    first_name    VARCHAR(50) NOT NULL,
    last_name     VARCHAR(50) NOT NULL,
    birth_date    DATE        NOT NULL,
    height        DECIMAL(4, 2) DEFAULT NULL,
    jersey_number INT           DEFAULT NULL,
    is_active     BOOLEAN     NOT NULL,
    season_exp    INT         NOT NULL,
    PRIMARY KEY (player_id)
);

# Create a nba team table with the following columns:
# team_id, team_name, abbreviation, nickname, city, state, year_founded
DROP TABLE IF EXISTS teams;
CREATE TABLE teams
(
    team_id      INT         NOT NULL,
    team_name    VARCHAR(50) NOT NULL ,
    abbreviation VARCHAR(3)  NOT NULL ,
    nickname     VARCHAR(50) NOT NULL ,
    city         VARCHAR(50) NOT NULL ,
    state        VARCHAR(50) NOT NULL ,
    year_founded INT         NOT NULL ,
    PRIMARY KEY (team_id)
);

DROP TABLE IF EXISTS positions;
CREATE TABLE positions
(
    position_id   INT NOT NULL AUTO_INCREMENT,
    position_name VARCHAR(50) DEFAULT 'Unknown',
    PRIMARY KEY (position_id)
);

DROP TABLE IF EXISTS player_position_link;
CREATE TABLE player_position_link
(
    player_id   INT NOT NULL,
    position_id INT NOT NULL,
    PRIMARY KEY (player_id, position_id),
    FOREIGN KEY (player_id) REFERENCES players (player_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (position_id) REFERENCES positions (position_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

DROP TABLE IF EXISTS player_team_link;
CREATE TABLE player_team_link
(
    player_id   INT NOT NULL,
    team_id     INT NOT NULL,
    season_year INT DEFAULT -1,
    PRIMARY KEY (player_id, team_id, season_year),
    FOREIGN KEY (player_id) REFERENCES players (player_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (team_id) REFERENCES teams (team_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

# Create table for games
DROP TABLE IF EXISTS games;
CREATE TABLE games
(
    game_id   INT  NOT NULL,
    game_date DATE NOT NULL,
    team1_id  INT  NOT NULL,
    team2_id  INT  NOT NULL,
    team1_pts INT  NOT NULL,
    team2_pts INT  NOT NULL,
    winner_id INT DEFAULT -1,
    FOREIGN KEY (team1_id) REFERENCES teams (team_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (team2_id) REFERENCES teams (team_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (winner_id) REFERENCES teams (team_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    PRIMARY KEY (game_id)
);

DROP TABLE IF EXISTS player_game_stats;
CREATE TABLE player_game_stats
(
    player_id      INT NOT NULL,
    game_id        INT NOT NULL,
    team_id        INT NOT NULL,
    points         INT NOT NULL,
    assists        INT NOT NULL,
    rebounds       INT NOT NULL,
    steals         INT NOT NULL,
    blocks         INT NOT NULL,
    turnovers      INT NOT NULL,
    fouls          INT NOT NULL,
    minutes_played INT NOT NULL,
    PRIMARY KEY (player_id, game_id),
    FOREIGN KEY (player_id) REFERENCES players (player_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (game_id) REFERENCES games (game_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (team_id) REFERENCES teams (team_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

# Create table for users, passwords, and account_types
DROP TABLE IF EXISTS users;
CREATE TABLE users
(
    user_id       INT         NOT NULL AUTO_INCREMENT,
    username      VARCHAR(50) NOT NULL,
    password_hash VARCHAR(60) NOT NULL,
    admin         BOOLEAN     NOT NULL DEFAULT FALSE,
    PRIMARY KEY (user_id)
);