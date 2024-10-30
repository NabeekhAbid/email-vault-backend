import bcrypt

class Utils:
    """Utility class for handling password operations."""

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt."""
        # Generate a salt and hash the password
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a hashed password against a plain password."""
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
