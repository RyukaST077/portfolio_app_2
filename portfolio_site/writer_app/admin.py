from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'has_api_key') # APIキー自体は表示しない方が良い

    def has_api_key(self, obj):
        return bool(obj.gemini_api_key)
    has_api_key.boolean = True
    has_api_key.short_description = 'API Key Set?'