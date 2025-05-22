from datetime import timezone
from rest_framework import serializers
from .models import UserProfile, Post, Comment, Follow, Notification
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile

from rest_framework import serializers

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'full_name', 'bio', 'avatar_url']
        read_only_fields = ['id', 'user'] 
    # def create(self, validated_data):
    #     user = self.context['request'].user
    #     return UserProfile.objects.create(user=user, **validated_data)


from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(source='user.id', read_only=True)  # Custom field for user ID
    username = serializers.CharField(source='user.username', read_only=True)  # Include username
    class Meta:
        model = Post
        fields = ['id', 'userId','username', 'text', 'image', 'timestamp']  # Include userId in fields
    # def get_timeAgo(self, obj):
    #     # Calculate the time difference
    #     time_difference = timezone.now() - obj.created_at
        
    #     # Convert the time difference to hours
    #     hours = time_difference.total_seconds() // 3600
        
    #     return f"{int(hours)} hours ago" if hours > 0 else "Just now"
        

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'post']

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'follower', 'followed']
        read_only_fields = ['follower']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['user', 'type', 'post', 'timestamp']