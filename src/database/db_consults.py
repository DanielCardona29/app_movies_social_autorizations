VALIDATE_IF_TABLE_USERS_EXISTS = """
    SELECT EXISTS (
        SELECT 1 FROM information_schema.tables
        WHERE table_name = 'mi_tabla'
    );
"""

CREATE_TABLE_USERS = """
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255),
    twitter_id VARCHAR(255) UNIQUE,
    google_id VARCHAR(255) UNIQUE,
    facebook_id VARCHAR(255) UNIQUE,
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""
INSERT_USER = (
    """INSERT INTO users (name, email, password, twitter_id, google_id, facebook_id) VALUES (%s, %s, %s, %s, %s, %s)"""
)
