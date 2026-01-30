import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sports_backend.settings')
django.setup()

from apps.users.models import User

# 创建超级管理员
try:
    if not User.objects.filter(username='admin').exists():
        user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin',
            real_name='管理员',
            phone='13800138000',
            user_type='admin'
        )
        print(f"超级管理员创建成功！")
        print(f"用户名: admin")
        print(f"密码: admin")
        print(f"真实姓名: {user.real_name}")
        print(f"手机号: {user.phone}")
    else:
        print("超级管理员已存在！")
except Exception as e:
    print(f"创建失败: {e}")
