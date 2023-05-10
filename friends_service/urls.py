from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('profiles_list/', views.ProfileListView.as_view(), name='profiles_list'),
    path('friends/', views.friends_list, name='friends'),
    path('incoming/', views.incoming_list, name='incoming'),
    path('outgoing/', views.outgoing_list, name='outgoing'),
    path('send_invite/', views.send_invitation, name='send_invite'),
    path('accept_invite/', views.accept_invitation, name='accept_invite'),
    path('reject_invite/', views.reject_invitation, name='reject_invite'),
    path('delete_friend/', views.remove_from_friends, name='delete_friend')
]