from django.contrib import admin
from matching.models import MatchingQueue, MatchGroup, MatchUser

class MatchUserInline(admin.TabularInline):
    model = MatchGroup.users.through
    extra = 0
    verbose_name_plural = 'Users'

@admin.register(MatchingQueue)
class MatchingAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'created_at', 'updated_at', 'status', 'match_id')

@admin.register(MatchGroup)
class MatchGroupAdmin(admin.ModelAdmin):
    list_display = ('match_id', 'created_at', 'updated_at', 'user_id1', 'user_id2', 'additional_info', 'get_users')
    inlines = [MatchUserInline]

    def get_users(self, obj):
        return ', '.join([str(user) for user in obj.users.all()])
    
    get_users.short_description = 'Users'