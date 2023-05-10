from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('invites/', views.accept_request, name='invites'),
    path('profiles_list/', views.ProfileListView.as_view(), name='profiles_list'),
    path('to_invite/', views.invite_profile_list, name='to_invite'),
    path('send_invite/', views.send_invitation, name='send_invite'),
    path('delete_friend/', views.remove_from_friends, name='delete_friend')
]