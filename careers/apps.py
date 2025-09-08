from django.apps import AppConfig


class CareersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'careers'
    verbose_name = 'Карьера и вакансии'
    
    def ready(self):
        try:
            import careers.translation  # noqa
        except ImportError:
            pass
