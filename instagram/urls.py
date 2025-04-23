from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.Login.as_view(), name='instagram-login'),
    path('logout/', views.Logout.as_view(), name='instagram-logout'),
    path('profile/', views.Profile.as_view(), name='instagram-profile'),
    path('profile/edit',views.ProfileEdit.as_view(),name = 'instagram-profile-edit'),
]
