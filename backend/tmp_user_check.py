from apps.users.models import User
user = User.objects.first()
print(user.username if user else 'no users')
