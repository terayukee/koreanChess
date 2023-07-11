from rest_framework import serializers

class GameInfoSerializer(serializers.Serializer):
    position = serializers.CharField()
    game_id = serializers.CharField()