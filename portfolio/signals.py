from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile, PersonalInfo


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Auto-create UserProfile and empty PersonalInfo on registration
        UserProfile.objects.get_or_create(
            user=instance,
            defaults={'username_slug': instance.username.lower()}
        )
        PersonalInfo.objects.get_or_create(
            user=instance,
            defaults={
                'full_name': instance.get_full_name() or instance.username,
                'email':     instance.email,
                'tagline':   '',
                'bio':       '',
            }
        )