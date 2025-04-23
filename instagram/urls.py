from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.Login.as_view(), name='instagram-login'),
    path('profile/', views.Profile.as_view(), name='instagram-profile'),
    path('bio/',views.GetBio.as_view(),name = 'instagram-bio'),
    path('editbio/',views.EditBio.as_view(),name = 'instagram-editbio'),
]
