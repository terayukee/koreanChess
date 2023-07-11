from collections import deque
import json
import uuid
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import MatchingQueue, MatchGroup
from asgiref.sync import sync_to_async
from channels.layers import get_channel_layer
from django.core.cache import cache
from django.contrib.auth import get_user_model
import asyncio

class MatchConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        userId = self.scope['url_route']['kwargs']['userId']
        await self.accept()
        await self.add_to_matching_queue(userId)
        
        # 사용자가 최초로 접속했을 때만 매칭 시도
        if await self.is_first_user():
            # try_matching 함수를 백그라운드에서 실행
            loop = asyncio.get_event_loop()
            loop.create_task(self.try_matching())

    async def disconnect(self):
        await self.remove_exited_user()

    async def receive(self, text_data):
        print('receive 동작')
        try:
            text_data_json = json.loads(text_data)
            
            if 'type' not in text_data_json or 'userId' not in text_data_json:
                raise ValueError("Message does not contain 'type' or 'userId' field")

            if text_data_json['type'] == 'matchInfoRequest':
                print('receive : matchInfoRequest')
                userId = text_data_json['userId']
                await self.responseMatchInfo(userId)
            elif text_data_json['type'] == 'test' :
                print('receive : test')
                
        except json.JSONDecodeError:
            print('Received message is not valid JSON')
            
        except ValueError as e:
            print(str(e))
            
        except Exception as e:
            print('An unexpected error occurred:', str(e))


    # 주기적으로 매칭큐 확인 및 매칭 시도 함수
    async def try_matching(self):
        
        while True:
            print('매칭 시도 중 ...')
            # 매칭큐에서 사용자 수 확인
            matching_queue_count = await sync_to_async(MatchingQueue.objects.count)()

            # 사용자 수가 2명 이상이면 매칭 수행
            if matching_queue_count >= 2:
                # 매칭큐의 'waiting' 상태인 사용자들을 가져옴
                matching_queue_users = await sync_to_async(
                    lambda: list(MatchingQueue.objects.filter(status='waiting').order_by('created_at').values_list('user_id', flat=True))
                )()
                
                # 만약 사용자 수가 홀수면 가장 마지막 유저 제외
                if len(matching_queue_users) % 2 == 1 :
                    matching_queue_users.pop()
                    
                matched_users_list = deque(matching_queue_users)
                    
                num_groups = len(matched_users_list) // 2
                
                # MatchGroup에 2명씩 추가
                for _ in range(num_groups) :
                    user1 = matched_users_list.popleft()
                    user2 = matched_users_list.popleft()

                    # 그룹 생성
                    match_id = str(uuid.uuid4())  # 매칭 ID 생성
                    print('매치 그룹 생성 : ',match_id)
                    match_group = await sync_to_async(MatchGroup.objects.create)(
                        match_id=match_id,
                        user_id1=user1,
                        user_id2=user2,
                    )

                    # users 필드 업데이트
                    User = get_user_model()
                    users = await sync_to_async(User.objects.filter)(user_id__in=matching_queue_users)
                    await sync_to_async(match_group.users.set)(users)
                    
                # 매칭된 사용자들의 상태 변경
                for user_id in matching_queue_users:
                    matching_queue = await sync_to_async(MatchingQueue.objects.get)(user_id=user_id)
                    matching_queue.status = "matched"
                    matching_queue.match_id = match_id
                    await sync_to_async(matching_queue.save)()
                    
                # response_message = {
                #     'type': 'checkMatch',
                #     'message': 'Matches are created!',
                # }
                # await self.send(text_data=json.dumps(response_message))
            else :
                print('Not enough matching users')
                
            await asyncio.sleep(10)  # 일정 시간 대기

    # 매칭큐에 사용자 추가 (userId 이용) 함수
    async def add_to_matching_queue(self, userId):
        matching_queue = MatchingQueue(user_id=userId)
        await sync_to_async(matching_queue.save)()
          
    # 매칭 정보 전달
    async def responseMatchInfo(self, userId):
        # userId로 match_id 가져오기
        matching_queue = await sync_to_async(MatchingQueue.objects.get)(user_id=userId)
        match_id = matching_queue.match_id
        print('매칭 정보 전달, match_id:', match_id)
        
        # 같은 match_id 사용자들 가져오기
        #matched_users = await sync_to_async(MatchingQueue.objects.filter)(match_id=match_id).order_by('created_at')
        matched_users = await sync_to_async(
                    lambda: list(MatchingQueue.objects.filter(match_id=match_id).order_by('created_at').values_list('user_id', flat=True))
                )()
        
        channel_layer = get_channel_layer()
        channel_name = f'match_{match_id}'  # 채널 이름 생성

        # 같은 채널의 사용자들(2명)에게 매칭 정보 전달
        await channel_layer.group_add(channel_name, self.channel_name)
        await channel_layer.group_send(channel_name, {
            'type': 'matchSuccess',
            'matchId': match_id,
            'users': [matched_users[0], matched_users[1]]
        })

        # 매칭 대기큐에서 사용자들 제거
        await self.remove_user_from_matching_queue(match_id)


    # 매칭된 유저들에게 매칭 정보 전달
    async def matchSuccess(self, event):
        print('matchSuccess !!')
        # matchSuccess 메시지 유형 처리 코드
        matchId = event['matchId']
        users = event['users']

        response_message = {
            'type': 'matchSuccess',
            'message': 'Matched with another user!',
            'matchId': matchId,
            'users': users
        }
        await self.send(text_data=json.dumps(response_message))
        
    
    # 매칭큐에서 사용자 제거 (match_id 이용) 함수
    async def remove_user_from_matching_queue(self, match_id):
        try:
            matching_queue = await sync_to_async(MatchingQueue.objects.get)(match_id=match_id)
            await sync_to_async(matching_queue.delete)()
        except MatchingQueue.DoesNotExist:
            pass

    # 매치 그룹에서 사용자 제거 함수
    async def remove_exited_user(self, userId):
        try:
            matching_queue = await sync_to_async(MatchingQueue.objects.get)(user_id=userId)
            await sync_to_async(matching_queue.delete)()
        except MatchingQueue.DoesNotExist:
            pass
      
    # 이미 매칭 시도 중인 사용자가 있는지 확인  
    async def is_first_user(self):  
        key = 'match_system_is_trying'
        is_trying = cache.get(key)
        if not is_trying:
            cache.set(key, True)
            return True
        return False