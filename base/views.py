from django.shortcuts import render
from .models import Category, Tag, Post, Comment
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .serializers import CategorySerializer, TagSerializer, PostSerializer, UserSerializer, LoginSerializer, CommentSerializer

# Create your views here.
class CategoryApiView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagApiView(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    


class PostApiView(GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['category', 'tags']
    search_fields = ['title', 'content']


    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self,request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user) # author is automatically set
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def destroy(self, request, pk):
        queryset = self.get_object()  
        queryset.delete()
        return Response()

    def partial_update(self, request, pk):
        query_set = self.get_object()

        serializer = self.get_serializer(query_set, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class UserApiView(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [] #empty cuz no need of permission

    def register(self,request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save() # author is automatically set
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():   #validate whether user information is being sent or not
            username = request.data.get("username")
            password = request.data.get("password")

            user = authenticate(username=username, password=password)  #passing username and password is authenticate to check whether it matches with any user or not, if matheces it returns user object data if not it returns none.  
            if user == None:  # if authenticate returns None, responding with invalid credentials response.
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED,)
            else:
                token, _ = Token.objects.get_or_create(user=user) 
                return Response({"token": token.key})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

    def list(self,request):
        queryset = self.get_queryset()
        Serializer = self.get_serializer(queryset,many=True)
        return Response(Serializer.data)
    
    def create(self,request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request,pk):
        # try:
        #     queryset = Department.objects.get(id=pk)
        # except:
        #     return Response({"error": "No mactching data found"})

        queryset = self.get_object()
        
        serializer = self.get_serializer(queryset, data=request.data) #By default dictonary is converted into json by response class
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def partial_update(self, request, pk):
        queryset = self.get_object()
        
        serializer = self.get_serializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    
    def retrieve(self, request, pk):
        queryset = self.get_object()

        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, pk):
        queryset = self.get_object()

        queryset.delete()
        return Response()

class CommentApiView(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
