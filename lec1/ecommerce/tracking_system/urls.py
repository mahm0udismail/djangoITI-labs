from django.urls import path
from . import views

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('postdata/', views.postdata, name='postdata'),  # Map the URL to the postdata view
#     path('example_view/', views.example_view, name='home'),
# ]
urlpatterns = [
    path('', views.home, name='home'),  # URL pattern for the home view
    path('postdata/', views.postdata, name='postdata'),  # URL pattern for the postdata view
    path('delete_order/', views.delete_order, name='delete_order'),  # URL pattern for the delete_order view
    path('edit_order/', views.edit_order, name='edit_order'),  # URL pattern for the delete_order view

]
