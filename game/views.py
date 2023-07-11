from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import GameInfoSerializer
from .models import Game
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.sessions.backends.db import SessionStore
from .models import Game
import uuid

class GameInfoView(APIView):
    def post(self, request):
        serializer = GameInfoSerializer(data=request.data)
        if serializer.is_valid():
            position = serializer.validated_data['position']
            game_id = serializer.validated_data['game_id']
            
            # DB에 저장
            game = Game(game_id=game_id, cho_position=position, han_position=position)
            game.save()
            
            # Game 모델의 모든 필드 값을 가져와서 응답 데이터로 전송
            fields = game._meta.get_fields()
            response_data = {
                'gameId': game_id
            }
            for field in fields:
                if field.name != 'game_id':
                    response_data[field.name] = getattr(game, field.name)
            
            return Response(response_data)
        else:
            return Response(serializer.errors, status=400)
        
def establish_session(request, match_id):
    # match_id를 사용하여 세션 생성
    session = SessionStore()
    session['match_id'] = match_id
    session.create()

    # 세션 키를 JSON 응답으로 반환
    return JsonResponse({
        'session_key': session.session_key
    })
        