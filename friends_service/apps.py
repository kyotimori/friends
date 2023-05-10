from django.apps import AppConfig


class FriendsServiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'friends_service'

    def ready(self):
        import friends_service.signals
