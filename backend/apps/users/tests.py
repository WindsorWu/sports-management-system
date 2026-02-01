from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APIClient


User = get_user_model()


class StaffUserDeletionTests(TestCase):
    def setUp(self):
        self.staff_owner = User.objects.create_user(
            username='staff-owner',
            password='pass1234',
            real_name='场馆管理员',
            phone='13800000001',
            is_staff=True
        )
        self.staff_target = User.objects.create_user(
            username='staff-target',
            password='pass1234',
            real_name='赛场管理',
            phone='13800000002',
            is_staff=True
        )
        self.normal_user = User.objects.create_user(
            username='athlete',
            password='pass1234',
            real_name='普通用户',
            phone='13800000003'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.staff_owner)

    def test_staff_can_delete_other_staff(self):
        response = self.client.delete(reverse('user-detail', args=[self.staff_target.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.staff_target.id).exists())

    def test_staff_cannot_delete_non_staff(self):
        response = self.client.delete(reverse('user-detail', args=[self.normal_user.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(User.objects.filter(id=self.normal_user.id).exists())


class AdminRefereeDeletionTests(TestCase):
    def test_admin_can_delete_referee(self):
        admin_user = User.objects.create_user(
            username='admin-user',
            password='pass1234',
            real_name='平台管理员',
            phone='13800000004',
            user_type='admin',
            is_staff=True
        )
        referee_user = User.objects.create_user(
            username='referee-user',
            password='pass1234',
            real_name='裁判',
            phone='13800000005',
            user_type='referee'
        )
        client = APIClient()
        client.force_authenticate(user=admin_user)

        response = client.delete(reverse('user-detail', args=[referee_user.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=referee_user.id).exists())
