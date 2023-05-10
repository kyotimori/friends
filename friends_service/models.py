from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

# Create your models here.

class ProfileManager(models.Manager):
    def get_all_profiles(self, current_user):
        profiles = Profile.objects.all().exclude(user=current_user)
        # profiles = [profile.user for profile in profiles_]
        return profiles
    
    def get_friends(self, current_user):
        friends = Profile.objects.filter(friends=current_user)
        # friends = [friend_profile.user for friend_profile in friends_profile]
        return friends
    
    def get_friends_num(self, current_user):
        friends = Profile.objects.filter(friends=current_user)
        return friends.count()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    friends = models.ManyToManyField(User, related_name='friends', blank=True)

    objects = ProfileManager()

    def __str__(self):
        return str(self.user.username)

STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted')
)


class RelationshipManager(models.Manager):
    def incoming(self, current_user):
        invitations = Relationship.objects.filter(to_user=current_user)
        senders = [invitation.from_user.user for invitation in invitations if invitation.status == 'send']
        return senders
    
    def outgoing(self, current_user):
        invitations = Relationship.objects.filter(from_user=current_user)
        receivers = [invitation.to_user.user for invitation in invitations if invitation.status == 'send']
        return receivers


class Relationship(models.Model):
    from_user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='to_user')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    objects = RelationshipManager()

    def __str__(self):
        return f'{self.from_user}->{self.to_user} ({self.status})'