from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from .models import Event


User = get_user_model()


class EventStatusTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='admin',
            password='password123',
            real_name='管理员',
            phone='13800000000'
        )

    def _create_event(self, **kwargs):
        base_time = timezone.now()
        defaults = {
            'title': '测试赛事',
            'description': '描述',
            'location': '北京',
            'event_type': 'athletics',
            'start_time': base_time - timedelta(days=2),
            'end_time': base_time + timedelta(days=1),
            'registration_start': base_time - timedelta(days=3),
            'registration_end': base_time + timedelta(days=5),
            'status': 'published',
            'organizer': self.user,
            'contact_person': '张三',
            'contact_phone': '13900000000'
        }
        defaults.update(kwargs)
        return Event.objects.create(**defaults)

    def test_display_status_becomes_finished_after_end(self):
        event = self._create_event(
            start_time=timezone.now() - timedelta(days=3),
            end_time=timezone.now() - timedelta(hours=1),
            registration_end=timezone.now() - timedelta(hours=2),
            status='published'
        )
        self.assertEqual(event.display_status, 'finished')

    def test_status_filter_returns_combined_finished(self):
        now = timezone.now()
        finished_event = self._create_event(
            end_time=now - timedelta(hours=1),
            status='published'
        )
        already_finished_event = self._create_event(
            end_time=now - timedelta(days=1),
            status='finished'
        )
        ongoing_event = self._create_event(
            end_time=now + timedelta(days=1),
            status='published'
        )

        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.get(reverse('event-list'), {'status': 'finished'})
        self.assertEqual(response.status_code, 200)
        ids = {item['id'] for item in response.json().get('results', [])}
        self.assertSetEqual(ids, {finished_event.id, already_finished_event.id})
