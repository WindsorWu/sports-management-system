from django.test import Client
from django.contrib.auth import get_user_model

client = Client()
User = get_user_model()
user = User.objects.first()
assert user is not None, 'No users found'
client.force_login(user)
response = client.post('/api/interactions/favorites/', {'target_type': 'event', 'target_id': 1})
print('status', response.status_code)
print('content', response.content)
