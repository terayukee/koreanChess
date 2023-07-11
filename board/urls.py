from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    #path('', views.index, name='index'),
    path('', views.ListBoard.as_view()),
    path('upload/', views.upload, name='upload'),
    path('<int:pk>/', views.DetailBoard.as_view()),
]