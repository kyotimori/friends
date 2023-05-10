from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

# Create your models here.

class ProfileManager(models.Manager):
    def get_all_profiles(self, current_user):
        profiles = Profile.objects.all().exclude(user=current_user)
        return profiles
    
    def get_friends(self, current_user):
        friends = Profile.objects.filter(friends=current_user)
        return friends
    
    def get_friends_num(self):
        return self.friends.all().count()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField(User, related_name='friends', blank=True)

    objects = ProfileManager()

    def __str__(self):
        return str(self.user.username)

STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted')
)


class RelationshipManager(models.Manager):
    def received(self, to_user):
        invitations = Relationship.objects.filter(to_user=to_user, status='send')
        return invitations


class Relationship(models.Model):
    from_user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='to_user')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    objects = RelationshipManager()

    def __str__(self):
        return f'{self.from_user}->{self.to_user} ({self.status})'