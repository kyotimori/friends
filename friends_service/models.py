from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

# Create your models here.

class ProfileManager(models.Manager):
    def get_all_profiles_to_invite(self, current_user):
        profiles = Profile.objects.all().exclude(user=current_user)
        profile = Profile.objects.get(user=current_user)
        relationships = Relationship.objects.filter(Q(from_user=profile) | Q(to_user=profile))
        print('##########')
        print(relationships)

        accepted = []
        for rel in relationships:
            if rel.status == 'accepted':
                accepted.append(rel.from_user)
                accepted.append(rel.to_user)
        print('##########')
        print(accepted)

        available = [profile for profile in profiles if profile not in accepted]
        print('##########')
        print(available)
        return available

    
    def get_all_profiles(self, current_user):
        profiles = Profile.objects.all().exclude(user=current_user)
        return profiles


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField(User, related_name='friends', blank=True)

    objects = ProfileManager()

    def get_friends(self):
        return self.friends.all()
    
    def get_friends_num(self):
        return self.friends.all().count()
    
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