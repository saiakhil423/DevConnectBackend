from django.urls import path
from .views import UserProfileViewSet, PostViewSet, CommentViewSet, FollowViewSet, NotificationViewSet,MyPostViewSet,IsFollowingView
from .views import my_profile, update_profile
urlpatterns = [
    path('profiles/', UserProfileViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-profile-list'),
    path('profiles/<int:pk>/', UserProfileViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='user-profile-detail'),
    path('my-profile/', my_profile, name='my-profile'),  # Fetch or create profile
    path('update-profile/', update_profile, name='update-profile'),  # Update profile
    
    
    path('posts/', PostViewSet.as_view({'get': 'list', 'post': 'create'}), name='post-list'),
    # path('posts/', PostViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='post-detail'),
    path('my-posts/', MyPostViewSet.as_view({'get': 'list'}), name='my-posts'),
    path('my-posts/<int:pk>/', MyPostViewSet.as_view({'get': 'list', 'put': 'update', 'delete': 'destroy'}), name='my-post'),  # New endpoint for user-specific posts

    
    path('comments/', CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='comment-list'),
    
    # Retrieve, update, or delete a specific comment by ID
    path('comments/<int:pk>/', CommentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='comment-detail'),
    
    # Add a comment to a specific post
    # path('comments/<int:post_id>/add/', CommentViewSet.as_view({'post': 'create_comment'}), name='create-comment'),
    path('comments/<int:pk>/add/', CommentViewSet.as_view({'post': 'create_comment'}), name='create-comment'),

    # Retrieve all comments for a specific post
    path('posts/<int:pk>/comments/', CommentViewSet.as_view({'get': 'list'}), name='post-comments'),

    path('follow/', FollowViewSet.as_view({'post': 'create'}), name='follow'),
    path('follow/<int:pk>/', FollowViewSet.as_view({'delete': 'destroy'}), name='unfollow'),
    path('follow/status/', FollowViewSet.as_view({'get': 'is_following'}), name='follow-status'),
    path('follow/is_following/', IsFollowingView.as_view(), name='is-following'), 
    
    path('notifications/', NotificationViewSet.as_view({'get': 'list'}), name='notification-list'),
    path('notifications/<int:pk>/', NotificationViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'}), name='notification-detail'),
]