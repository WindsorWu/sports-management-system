import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sports_backend.settings')
import django
django.setup()

from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.tokens import AccessToken
from apps.interactions.views import FavoriteViewSet, normalize_interaction_payload
from apps.users.models import User

user = User.objects.filter(is_active=True).first()
print('user', user)
if not user:
    raise SystemExit('no user')
factory = APIRequestFactory()
token = AccessToken.for_user(user)
payload = normalize_interaction_payload({'target_type': 'event', 'target_id': 1})
print('payload', payload)
request = factory.post('/api/interactions/favorites/', payload, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
request.user = user
view = FavoriteViewSet.as_view({'post': 'create'})
response = view(request)
print(response.status_code)
print(response.data)
