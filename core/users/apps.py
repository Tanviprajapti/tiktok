from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # Correct import for BigAutoField
    name = 'core.users'
    label = 'users'
