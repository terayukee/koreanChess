from django.contrib import admin
from gameusers.models import GameUser

@admin.register(GameUser)
class GameUserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'created_at', 'matched', 'match_id')
    list_filter = ('matched',)
    search_fields = ('user_id', 'match_id')
