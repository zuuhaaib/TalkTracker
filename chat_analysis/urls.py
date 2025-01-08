from django.urls import path
from . import views

urlpatterns = [
    path('', views.reverse_lines_view, name='index'),
    path('analysis/', views.analyze_chat_view, name='analysis'),
    #path('analyze/', views.analyze_chat_view_test, name='analyze_chat_view'),
]
