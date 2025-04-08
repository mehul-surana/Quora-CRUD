from rest_framework import serializers
from .models import Question, Answer
from django.contrib.auth.models import User
 
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

class QuestionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Question
        fields = '__all__'

class AnswerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        fields = ['id', 'user', 'question', 'content', 'created_at', 'likes_count']
        read_only_fields = ['user', 'question'] 
        
    def get_likes_count(self, obj):
        return obj.likes.count()
