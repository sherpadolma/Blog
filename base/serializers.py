from rest_framework import serializers
from .models import Category, Tag, Post, Comment
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True) # Make author read-only so it can be set automatically
    class Meta:
        model = Post
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'content', 'author', 'created_at']
        read_only_fields = ['author', 'created_at']

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

    def create(self, validated_data):
        password = validated_data.pop('password') #create a new user object with the remaining validated data
        user = User(**validated_data)  # Use Django's built-in set_password method to hash the password instead of saving it as plain text
        user.set_password(password)  # properly hash password for Django
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()    


    