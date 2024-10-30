import os
from dotenv import load_dotenv
from flask import create_app

# Load environment variable
load_dotenv()
load_dotenv('.env.secrets')

# Determine the configuration from the environment variables
flask_env = os.get_env('FLASK_ENV', 'development')

# Create the app with specified configuration 
app = create_app(flask_env)

# Run the application
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=(flask_env == "development"))