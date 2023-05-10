from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Relationship, Profile
from django.views.generic import ListView
from django.db.models import Q

# Create your views here.

@login_required
def profile(request):
    user_profile = Profile.objects.get(user=request.user)
    context = {'profile': user_profile}

    return render(request, 'friends_service/profile.html', context)


# @login_required
# def send_request(request, user_id):
#     from_user = request.user
#     to_user = User.objects.get(id=user_id)
#     request, sent = Relationship.objects.get_or_create(from_user=from_user, to_user=to_user)


# @login_required
# def accept_request(request):
#     profile = Profile.objects.get(user=request.user)
#     invitations = Relationship.objects.received(profile)
#     context = {'profiles': invitations}

#     return render(request, 'friends_service/invitations.html', context)

def friends_list(request):
    user = request.user
    profiles = Profile.objects.get_friends(user)

    context = {'profiles': profiles}

    return render(request, 'friends_service/friends.html', context)


def incoming_list(request):
    to_user = Profile.objects.get(user=request.user)
    senders = Relationship.objects.filter(to_user=to_user)

    context = {'profiles': senders}

    return render(request, 'friends_service/incoming.html', context)


def outgoing_list(request):
    from_user = Profile.objects.get(user=request.user)
    invitations = Relationship.objects.filter(from_user=from_user)
    receivers = []
    for invitation in invitations:
        receivers.append(invitation.to_user)

    context = {'profiles': receivers}

    return render(request, 'friends_service/outgoing.html', context)


class ProfileListView(ListView):
    model = Profile
    template_name = 'friends_service/profiles_list.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        profiles = Profile.objects.get_all_profiles(self.request.user)
        return profiles
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_from = Relationship.objects.filter(from_user=profile)
        rel_to = Relationship.objects.filter(to_user=profile)
        receivers = []
        senders = []
        for item in rel_from:
            receivers.append(item.to_user.user)
        for item in rel_to:
            senders.append(item.from_user.user)
        context['receivers'] = receivers
        context['senders'] = senders

        return context  
    

def send_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        from_user = Profile.objects.get(user=user)
        to_user = Profile.objects.get(pk=pk)

        relationship = Relationship.objects.create(from_user=from_user, to_user=to_user, status='send')
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profile')


def accept_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        from_user = Profile.objects.get(pk=pk)
        to_user = Profile.objects.get(user=user)

        relationship = Relationship.objects.get(from_user=from_user, to_user=to_user)
        relationship.status = 'accepted'
        relationship.save()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profile')


def reject_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        from_user = Profile.objects.get(pk=pk)
        to_user = Profile.objects.get(user=user)

        relationship = Relationship.objects.get(Q(from_user=from_user) & Q(to_user=to_user))
        relationship.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profile')


def remove_from_friends(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        from_user = Profile.objects.get(user=user)
        to_user = Profile.objects.get(pk=pk)

        relationship = Relationship.objects.get(
            (Q(from_user=from_user) & Q(to_user=to_user)) | (Q(from_user=to_user) & Q(to_user=from_user))
        )
        relationship.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profile')