from django.apps import AppConfig

# Import the Tweet class so we can create an instance when the app starts
from .functions.tweet import Tweet

class YourAppNameConfig(AppConfig):
    # Default field type for primary keys in the database
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Name of this Django app — change 'your_app' to your actual app name
    name = 'your_app'

    # This method runs automatically when Django starts the app
    def ready(self):
        # Create the Tweet instance once at startup, so we can authenticate with Twitter early
        Tweet()
