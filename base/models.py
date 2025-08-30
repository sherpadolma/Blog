from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=300)

class Tag(models.Model):
    name = models.CharField(max_length=300)

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')  #OTM - one user can have many post
    title = models.CharField(max_length=300)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts') #OTM
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')  #MTM - a post can have many tags
    created_at = models.DateTimeField(auto_now_add=True)  # automatically set when object is created
    updated_at = models.DateTimeField(auto_now=True)      # automatically updated on save


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments') # OTM - many comments for one post
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')  # OTM - user who wrote the comment
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # approved = models.BooleanField(default=True)