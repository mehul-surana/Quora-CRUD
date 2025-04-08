from django.urls import path
from core.views import (
    RegisterView, LoginView, LogoutView,
    QuestionListCreateView, AnswerListCreateView, LikeAnswerView
)

urlpatterns = [
    path('', QuestionListCreateView.as_view(), name='question_list'),
    
    path('register/', RegisterView.as_view(), name='register_page'),
    path('login/', LoginView.as_view(), name='login_page'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('questions/<int:question_id>/answers/', AnswerListCreateView.as_view(), name='answer_list'),
    path('answers/<int:answer_id>/like/', LikeAnswerView.as_view(), name='like_answer'),
]
