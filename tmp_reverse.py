from django.urls import reverse, NoReverseMatch
try:
    print('reverse:', reverse('refereeaccess-list'))
except Exception as exc:
    print('error:', exc)
