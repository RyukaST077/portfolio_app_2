from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='gemini_profile')
    gemini_api_key = models.CharField(max_length=200, blank=True, null=True, verbose_name='Gemini API Key')

    def __str__(self):
        return f"{self.user.username}'s Profile"

# User作成時に自動でUserProfileを作成するシグナル
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.gemini_profile.save() # 既存ユーザーの場合も更新時に保存