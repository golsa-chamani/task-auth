from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.Login.as_view(), name='instagram-login'),
    path('profile/', views.Profile.as_view(), name='instagram-profile'),
]
