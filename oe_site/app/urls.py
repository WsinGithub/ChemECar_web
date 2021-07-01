from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('get_data', views.get_data),
    path('exp_post', views.exp_post),
    path('data/<path:file_url>', views.data_download, name='data_download'),
]
