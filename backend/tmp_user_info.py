import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sports_backend.settings')
import django
django.setup()
from apps.users.models import User
from apps.users.serializers import UserSerializer
user = User.objects.filter(is_superuser=True).first()
print(user.username, user.is_staff)
print(UserSerializer(user).data)
