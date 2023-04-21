USE nba_db;
# Create procedure to create a new user
DROP PROCEDURE IF EXISTS create_user;
CREATE PROCEDURE create_user(
    IN username_p VARCHAR(50),
    IN password_p VARCHAR(60),
    IN admin_p BOOLEAN
)
BEGIN
    INSERT INTO users (username,
                       password_hash,
                       admin)
    VALUES (username_p,
            password_p,
            admin_p);
END;

# Create procedure to check if username is taken
DROP PROCEDURE IF EXISTS check_username;
CREATE PROCEDURE check_username(
    IN username_p VARCHAR(50)
)
BEGIN
    SELECT 1 FROM users WHERE username = username_p;
END;


# Create procedure to get password hash
DROP PROCEDURE IF EXISTS get_password_hash;
CREATE PROCEDURE get_password_hash(
    IN username_p VARCHAR(50)
)
BEGIN
    SELECT password_hash FROM users WHERE username = username_p;
END;

# Create procedure to get user
DROP PROCEDURE IF EXISTS get_user;
CREATE PROCEDURE get_user(
    IN username_p VARCHAR(50)
)
BEGIN
    SELECT * FROM users WHERE username = username_p;
END;





