import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sports_backend.settings')
django.setup()

from apps.users.models import User

# 验证超级管理员
user = User.objects.filter(username='admin').first()
if user:
    print("=" * 50)
    print("Super Admin Verification")
    print("=" * 50)
    print(f"Username: {user.username}")
    print(f"Email: {user.email}")
    print(f"Real Name: {user.real_name}")
    print(f"Phone: {user.phone}")
    print(f"User Type: {user.user_type}")
    print(f"Is Superuser: {user.is_superuser}")
    print(f"Is Staff: {user.is_staff}")
    print("=" * 50)
    print("Super admin created successfully!")
else:
    print("Admin user not found!")

# 统计所有模型
print("\nDatabase Statistics:")
print("=" * 50)
from apps.events.models import Event
from apps.registrations.models import Registration
from apps.results.models import Result
from apps.announcements.models import Announcement
from apps.interactions.models import Like, Favorite, Comment
from apps.carousel.models import Carousel
from apps.feedback.models import Feedback

print(f"Users: {User.objects.count()}")
print(f"Events: {Event.objects.count()}")
print(f"Registrations: {Registration.objects.count()}")
print(f"Results: {Result.objects.count()}")
print(f"Announcements: {Announcement.objects.count()}")
print(f"Likes: {Like.objects.count()}")
print(f"Favorites: {Favorite.objects.count()}")
print(f"Comments: {Comment.objects.count()}")
print(f"Carousels: {Carousel.objects.count()}")
print(f"Feedbacks: {Feedback.objects.count()}")
print("=" * 50)
