# app/migrations/0000000001_create_user_related_tables.py
revision = "0000000001"
down_revision = "0000000000"
def upgrade(migration):
    # Create users table
    migration.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            firstName VARCHAR(255) NOT NULL,
            lastName VARCHAR(255) NOT NULL,
            CompanyName VARCHAR(255) NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            is_verified BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );
    """)
    # Create email_verifications table
    migration.execute("""
        CREATE TABLE IF NOT EXISTS email_verifications (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            token VARCHAR(255) UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL,
            used_at TIMESTAMP NULL DEFAULT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """)
    # Create password_resets table
    migration.execute("""
        CREATE TABLE IF NOT EXISTS password_resets (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            token VARCHAR(255) UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL,
            used_at TIMESTAMP NULL DEFAULT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """)
    # Create failed_logins table
    migration.execute("""
        CREATE TABLE IF NOT EXISTS failed_logins (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """)
    # Create indices for email column and tokens
    migration.execute("""
        CREATE INDEX idx_user_email ON users(email);
    """)
    migration.execute("""
        CREATE INDEX idx_verification_token ON email_verifications(token);
    """)
    migration.execute("""
        CREATE INDEX idx_reset_token ON password_resets(token);
    """)
    # Update version table with current migration
    migration.update_version_table(version=revision)
def downgrade(migration):
    # Drop indices first
    migration.execute("DROP INDEX IF EXISTS idx_reset_token ON password_resets;")
    migration.execute("DROP INDEX IF EXISTS idx_verification_token ON email_verifications;")
    migration.execute("DROP INDEX IF EXISTS idx_user_email ON users;")
    # Drop tables in reverse order
    migration.execute("DROP TABLE IF EXISTS failed_logins;")
    migration.execute("DROP TABLE IF EXISTS password_resets;")
    migration.execute("DROP TABLE IF EXISTS email_verifications;")
    migration.execute("DROP TABLE IF EXISTS users;")
    # Update version table back to previous version
    migration.update_version_table(version=down_revision)














