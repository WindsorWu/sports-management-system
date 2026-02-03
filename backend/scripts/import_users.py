"""Import athlete users from user.csv into the sports database."""
import csv
import logging
import os
import sys
from pathlib import Path

import django

BASE_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = BASE_DIR.parent
sys.path.append(str(PROJECT_ROOT))
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sports_backend.settings')
django.setup()

from django.db import IntegrityError
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
logger.addHandler(handler)

User = get_user_model()
DATA_FILE = PROJECT_ROOT / 'user.csv'
PASSWORD = '888888'
EXPECTED_ROLE = 'referee'


def normalize(value: str) -> str:
    return value.strip() if value else ''


def main() -> None:
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Missing data file at {DATA_FILE}")

    inserted = 0
    skipped = []

    with DATA_FILE.open(newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            username = normalize(row.get('username', ''))
            phone = normalize(row.get('phone', ''))
            if not username or not phone:
                skipped.append((row, '缺失用户名或手机号'))
                continue

            if User.objects.filter(username=username).exists():
                skipped.append((row, '用户名已存在'))
                continue

            if User.objects.filter(phone=phone).exists():
                skipped.append((row, '手机号已存在'))
                continue

            defaults = {
                'username': username,
                'email': normalize(row.get('email', '')),
                'real_name': normalize(row.get('real_name', username)),
                'phone': phone,
                'user_type': normalize(row.get('user_type', EXPECTED_ROLE)) or EXPECTED_ROLE,
                'first_name': normalize(row.get('first_name', '')),
                'last_name': normalize(row.get('last_name', '')),
                'is_active': True,
            }

            try:
                User.objects.create_user(**defaults, password=PASSWORD)
            except IntegrityError as exc:
                skipped.append((row, f'数据库约束失败: {exc}'))
                continue

            inserted += 1
            logger.info('已创建用户: %s', username)

    logger.info('插入完成：%d 条，跳过 %d 条', inserted, len(skipped))
    if skipped:
        logger.info('跳过详情：')
        for row, reason in skipped:
            logger.info('- %s -> %s', row.get('username') or row.get('phone'), reason)


if __name__ == '__main__':
    main()
