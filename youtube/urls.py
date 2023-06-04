from django.urls import path
from .views import Home, comment

urlpatterns = [
    path('', Home, name='home'),
    path('comment/<int:pk>/', comment, name='comment'),
]