from django.apps import AppConfig

# django框架默认文件
class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
