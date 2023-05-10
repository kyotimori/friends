from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Relationship


@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Relationship)
def post_save_add_friend(sender, instance, created, **kwargs):
    from_user = instance.from_user
    to_user = instance.to_user
    if instance.status == 'accepted':
        from_user.friends.add(to_user.user)
        to_user.friends.add(from_user.user)
        from_user.save()
        to_user.save()


@receiver(pre_delete, sender=Relationship)
def pre_delete_remove_from_friends(sender, instance, **kwargs):
    from_user = instance.from_user
    to_user = instance.to_user
    from_user.friends.remove(to_user.user)
    to_user.friends.remove(from_user.user)
    from_user.save()
    to_user.save()