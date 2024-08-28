from django.urls import path
from . import views

urlpatterns = [
    path('get-data/', views.get_data, name='get_data'),
    path('add-data/', views.add_data, name='add_data'),
]