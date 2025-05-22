from rest_framework import viewsets
from .models import UserProfile, Post, Comment, Follow, Notification
from .serializers import UserProfileSerializer, PostSerializer, CommentSerializer, FollowSerializer, NotificationSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return UserProfile.objects.all()  # Default: Return all profiles

    @action(detail=False, methods=['get'], url_path='my-profile')
    def my_profile(self, request):
        # Check if a profile exists for the logged-in user
        user_profile = UserProfile.objects.filter(user=request.user).first()
        if user_profile:
            serializer = self.get_serializer(user_profile)
            return Response(serializer.data)
        # Return 404 if no profile exists
        return Response({"detail": "Profile not found."}, status=404)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Automatically associate with the logged-in user
        
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Ensure the user is set when creating a post
        serializer.save(user=self.request.user)

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer

class MyPostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return only posts created by the logged-in user
        return Post.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except Exception as e:
            print(f"Error saving post: {e}")

    def update(self, request, *args, **kwargs):
        post = self.get_object()
        if post.user != request.user:
            return Response({"detail": "You do not have permission to edit this post."}, status=status.HTTP_403_FORBIDDEN)
        return super(MyPostViewSet, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        if post.user != request.user:
            return Response({"detail": "You do not have permission to delete this post."}, status=status.HTTP_403_FORBIDDEN)
        return super(MyPostViewSet, self).destroy(request, *args, **kwargs)  # Corrected line
    
    
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    def list(self, request, pk=None):
        # Get the specific post
        post = get_object_or_404(Post, pk=pk)
        
        # Fetch only comments related to this post
        comments = post.comments.all()  # Assuming a reverse relation named 'comments' exists
        #print(comments)
        # Serialize the comments
        serializer = CommentSerializer(comments, many=True)
        
        return Response(serializer.data)
    

    def perform_create(self, serializer):
        serializer.save(commentor=self.request.user, user=self.request.user)

    @action(detail=True, methods=['post'], url_path='add')
    def create_comment(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post, commentor=request.user, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @action(detail=True, methods=['get'], url_path='comments')
    def get_comment(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        comments = post.comments.all()  # Assuming Post model has a related_name 'comments' for its comments
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

from rest_framework.views import APIView
class AddCommentView(APIView):
    def post(self, request, post_id):
        user = request.data.get('user')  # Assuming user is passed
        post = Post.objects.get(id=post_id)  # Get the post by post_id
        text = request.data.get('text')

        if not user or not text:
            return Response({"error": "Both user and text fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        comment = Comment.objects.create(user=user, post=post, text=text)
        return Response({"message": "Comment added successfully", "comment": comment.id}, status=status.HTTP_201_CREATED)
    
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from .models import Follow
from .serializers import FollowSerializer
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        follower = request.user
        print("Request Data:", request.data)
        followed_id = request.data.get('followed')
        print(f"Followed ID: {followed_id}")
        
        
        if follower.id == followed_id:
            return Response({"error": "You cannot follow yourself"}, status=400)
        if not User.objects.filter(id=followed_id).exists():
            return JsonResponse({"error": "User not found"}, status=404)
        followed_user = User.objects.get(id=followed_id)

        
        if Follow.objects.filter(follower=follower, followed=followed_user).exists():
            return Response({"message": "Already following"}, status=400)

        follow = Follow.objects.create(follower=follower, followed=followed_user)
        return Response(FollowSerializer(follow).data, status=201)

    def destroy(self, request, pk=None):
        follower = request.user
        try:
            follow = Follow.objects.get(follower=follower, followed_id=pk)
            follow.delete()
            return Response({"message": "Unfollowed successfully"}, status=200)
        except Follow.DoesNotExist:
            return Response({"error": "Follow relationship not found"}, status=400)

    @action(detail=False, methods=['get'])
    def is_following(self, request):
        follower = request.user
        followed_id = request.query_params.get('followed')
    
        print(f"Follower ID: {follower.id}, Followed ID: {followed_id}")  # Debugging line
    
        if Follow.objects.filter(follower=follower, followed_id=followed_id).exists():
            return Response({"is_following": True})
        return Response({"is_following": False})
class IsFollowingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        followed_id = request.GET.get('followed')
        if not followed_id:
            return JsonResponse({"error": "Followed user ID is required"}, status=400)

        try:
            followed_user = User.objects.get(id=followed_id)
        except User.DoesNotExist:
            return JsonResponse({"error": "User  not found"}, status=404)

        is_following = request.user.following.filter(id=followed_id).exists()
        return JsonResponse({"is_following": is_following})
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return notifications for the authenticated user
        return Notification.objects.filter(user=self.request.user)
from rest_framework.decorators import api_view,permission_classes  
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def my_profile(request):
    """Fetch or create user profile"""
    try:
        profile = UserProfile.objects.get(user=request.user)
        if request.method == 'GET':
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data)
    except UserProfile.DoesNotExist:
        if request.method == 'GET':
            return Response({"detail": "Profile not found"}, status=404)
        elif request.method == 'POST':
            serializer = UserProfileSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """Update an existing user profile"""
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return Response({"detail": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserProfileSerializer(profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)