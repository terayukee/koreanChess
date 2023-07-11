from django.shortcuts import render, redirect
from .forms import BoardForm
from rest_framework import generics

from .models import Board
from .serializers import BoardSerializer

# Create your views here.
def index(request):
    context = {'board_list' : '인자 전달 테스트'}
    return render(request, 'board/index.html', context)

def upload(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # 등록 후 리디렉션할 URL을 지정합니다.
    else:
        form = BoardForm()
    return render(request, 'board/upload.html', {'form': form})

class ListBoard(generics.ListCreateAPIView) :
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    
class DetailBoard(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer