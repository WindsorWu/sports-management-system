import os
import sys
import random
import uuid
from datetime import date, datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sports_backend.settings')
import django

django.setup()

from apps.users.models import User
from apps.events.models import Event
from apps.registrations.models import Registration

TARGET_USER_IDS = [
    12, 15, 18, 21, 23, 26, 29, 30, 33, 35, 37, 39, 41, 42, 44, 46, 48, 50,
    52, 53, 55, 57, 59, 61, 62, 64, 66, 68, 70, 72, 74, 75, 77, 79, 80, 82,
    84, 86, 88, 89, 91, 93, 95, 96, 97, 98, 100, 13, 19, 27
]

EMERGENCY_CONTACTS = [
    "赵浩然", "苏雨桐", "王梓涵", "陈俊豪", "李沐宸", "刘语桐", "黄奕辰", "周玥",
    "吴泽宇", "孙一诺", "徐思琪", "马凯", "朱静怡", "胡博文", "林晓雅", "郭宇轩",
    "何欣悦", "高梓琪", "罗俊峰", "郑雨欣", "梁沐阳", "谢一诺", "宋思彤", "唐宇辰",
    "韩雨桐", "曹俊豪", "邓沐宸", "彭语桐", "曾奕辰", "肖玥", "田泽宇", "袁一诺",
    "董思琪", "潘凯", "于静怡", "叶博文", "蒋晓雅", "蔡宇轩", "余欣悦", "杜梓琪",
    "程俊峰", "傅雨欣", "魏沐阳", "薛一诺", "白思彤", "温宇辰", "江雨桐", "雷俊豪",
    "方沐宸", "石语桐"
]

EVENT_ID = 5


def generate_random_chinese_mobile() -> str:
    prefixes = [
        '134', '135', '136', '137', '138', '139', '150', '151', '152', '157', '158', '159',
        '178', '182', '183', '184', '187', '188', '198'
    ]
    return random.choice(prefixes) + ''.join(str(random.randint(0, 9)) for _ in range(8))


def calculate_check_digit(base17: str) -> str:
    weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    mapping = '10X98765432'
    total = sum(int(base17[i]) * weights[i] for i in range(17))
    return mapping[total % 11]


def build_unique_id_card(birth: date) -> str:
    while True:
        area_code = '110105'
        birth_str = birth.strftime('%Y%m%d')
        sequence = f"{random.randint(0, 999):03d}"
        base = f"{area_code}{birth_str}{sequence}"
        candidate = base + calculate_check_digit(base)
        if not User.objects.filter(id_card=candidate).exists():
            return candidate


def extract_birth_from_id(id_number: str) -> date:
    return datetime.strptime(id_number[6:14], '%Y%m%d').date()


def build_registration_number(event_id: int) -> str:
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    return f"REG-{event_id}-{timestamp}-{uuid.uuid4().hex[:8].upper()}"


def create_registration(user: User, event: Event, emergency_name: str, emergency_phone: str) -> Registration:
    birth_date = user.birth_date or date(1995, 1, 1)
    if not user.birth_date:
        birth_date = date(random.randint(1990, 2004), random.randint(1, 12), random.randint(1, 28))

    if not user.id_card or len(user.id_card) != 18:
        id_card = build_unique_id_card(birth_date)
        user.id_card = id_card
        user.birth_date = birth_date
        user.save(update_fields=['id_card', 'birth_date'])
    else:
        try:
            birth_date = extract_birth_from_id(user.id_card)
        except ValueError:
            birth_date = date(random.randint(1990, 2004), random.randint(1, 12), random.randint(1, 28))
            user.id_card = build_unique_id_card(birth_date)
            user.birth_date = birth_date
            user.save(update_fields=['id_card', 'birth_date'])

    return Registration.objects.create(
        event=event,
        user=user,
        registration_number=build_registration_number(event.id),
        participant_name=user.real_name,
        participant_phone=user.phone,
        participant_id_card=user.id_card,
        participant_gender=user.gender or 'M',
        participant_birth_date=birth_date,
        emergency_contact=emergency_name,
        emergency_phone=emergency_phone,
        payment_status='unpaid'
    )


def main():
    event = Event.objects.filter(id=EVENT_ID).first()
    if not event:
        print(f"Event {EVENT_ID} not found.")
        return

    random.shuffle(EMERGENCY_CONTACTS)
    if len(EMERGENCY_CONTACTS) < len(TARGET_USER_IDS):
        raise RuntimeError("Contact list is too short for the target users.")

    created = 0
    for idx, user_id in enumerate(TARGET_USER_IDS):
        user = User.objects.filter(id=user_id).first()
        if not user:
            print(f"User {user_id} missing; skipping.")
            continue

        if Registration.objects.filter(event=event, user=user).exists():
            print(f"User {user_id} already registered; skipping.")
            continue

        emergency_name = EMERGENCY_CONTACTS[idx]
        try:
            emergency_phone = generate_random_chinese_mobile()
            create_registration(user, event, emergency_name, emergency_phone)
            created += 1
        except Exception as exc:
            print(f"Failed for user {user_id}: {exc}")

    print(f"Created {created} registrations for event {EVENT_ID}.")


if __name__ == '__main__':
    main()
