from django.shortcuts import get_object_or_404, render, redirect
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Question, Answer, AnswerLike
from .serializers import QuestionSerializer, AnswerSerializer, RegisterSerializer
from django.views import View
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User

def get_user_from_request(request):
    access_token = request.COOKIES.get("access")
    if not access_token:
        return None
    try:
        token = AccessToken(access_token)
        user_id = token['user_id']
        return User.objects.get(id=user_id)
    except Exception:
        return None


class RegisterView(View):
    def get(self, request):
        return render(request, 'core/register.html')

    def post(self, request):
        serializer = RegisterSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, "User registered. Please login.")
            return redirect('login_page')
        return render(request, 'core/register.html', {'errors': serializer.errors})


class LoginView(View):
    def get(self, request):
        return render(request, 'core/login.html')

    @method_decorator(csrf_protect)
    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            response = redirect('question_list')
            response.set_cookie('access', str(refresh.access_token), httponly=True)
            response.set_cookie('refresh', str(refresh), httponly=True)
            return response

        messages.error(request, "Invalid username or password")
        return render(request, 'core/login.html')

class LogoutView(View):
    def get(self, request):
        refresh_token = request.COOKIES.get("refresh")
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                pass
        response = redirect('login_page')
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        return response


class QuestionListCreateView(View):
    def get(self, request):
        questions = Question.objects.all().order_by('-created_at')
        return render(request, 'core/question_list.html', {'questions': questions})

    def post(self, request):
        user = get_user_from_request(request)
        if not user:
            return redirect('login_page')
        serializer = QuestionSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save(user=user)
        return redirect('question_list')


class AnswerListCreateView(View):
    def get(self, request, question_id):
        question = get_object_or_404(Question, id=question_id)
        answers = Answer.objects.filter(question=question)
        return render(request, 'core/answer_list.html', {'question': question, 'answers': answers})

    def post(self, request, question_id):
        user = get_user_from_request(request)
        if not user.is_authenticated:
            return redirect('login_page')
        question = get_object_or_404(Question, id=question_id)
        serializer = AnswerSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save(user=user, question=question)
        return redirect('answer_list', question_id=question.id)

class LikeAnswerView(View):
    def post(self, request, answer_id):
        user = get_user_from_request(request)
        if not user.is_authenticated:
            return redirect('login_page')
        answer = get_object_or_404(Answer, id=answer_id)
        like, created = AnswerLike.objects.get_or_create(user=user, answer=answer)
        if not created:
            like.delete()
        return redirect('answer_list', question_id=answer.question.id)
