from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('loaddata/', views.load_data, name='loader'),
    path('ask/', views.get_info, name='ask')
]
