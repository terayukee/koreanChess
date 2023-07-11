from rest_framework import serializers
from gameusers.models import GameUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameUser
        fields = ('user_id', 'created_at', 'matched', 'match_id')
