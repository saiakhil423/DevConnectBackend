from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile, Post

class UserProfileModelTests(TestCase):
    def test_user_profile_creation(self):
        user = User.objects.create_user(username='testuser', password='password')
        profile = UserProfile.objects.create(user=user, bio='This is a test bio.')
        self.assertEqual(profile.bio, 'This is a test bio.')

class PostModelTests(TestCase):
    def test_post_creation(self):
        user = User.objects.create_user(username='testuser', password='password')
        post = Post.objects.create(user=user, text='This is a test post.')
        self.assertEqual(post.text, 'This is a test post.')