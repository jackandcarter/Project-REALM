import pymysql

def create_auth_database(connection):
    """Create the Authentication database and its tables."""
    with connection.cursor() as cursor:
        # Create the Authentication database
        cursor.execute("CREATE DATABASE IF NOT EXISTS auth_db;")
        connection.select_db("auth_db")
        
        # Create Accounts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                is_banned BOOLEAN DEFAULT FALSE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_login DATETIME NULL,
                permission_level INT DEFAULT 0
            );
        """)

        # Create Bans table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bans (
                id INT AUTO_INCREMENT PRIMARY KEY,
                account_id INT,
                ip_address VARCHAR(255) NULL,
                reason TEXT NOT NULL,
                banned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (account_id) REFERENCES accounts(id)
            );
        """)

        # Create Login Attempts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS login_attempts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                account_id INT NULL,
                ip_address VARCHAR(255) NOT NULL,
                status ENUM('success', 'failure') NOT NULL,
                attempted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (account_id) REFERENCES accounts(id)
            );
        """)

        # Create Sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                account_id INT NOT NULL,
                session_key VARCHAR(255) UNIQUE NOT NULL,
                ip_address VARCHAR(255) NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                expires_at DATETIME NOT NULL,
                FOREIGN KEY (account_id) REFERENCES accounts(id)
            );
        """)

        connection.commit()
    print("Authentication database and tables created successfully.")

if __name__ == "__main__":
    # Prompt for MySQL credentials
    host = input("Enter MySQL host (default: localhost): ") or "localhost"
    user = input("Enter MySQL user (default: root): ") or "root"
    password = input("Enter MySQL password: ")

    # Connect to MySQL server
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password
    )

    try:
        create_auth_database(connection)
    finally:
        connection.close()
