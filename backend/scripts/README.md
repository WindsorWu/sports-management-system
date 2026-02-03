# Event 5 Bulk Registration Script

This script creates registrations for event ID `5` using the specified user IDs and emergency contacts.

## Usage

Make sure the virtualenv where Django is installed is active, then run:

```sh
python backend/scripts/bulk_register_event5.py
```

## Behavior

- It reuses each user's `real_name` and `phone` values.
- It generates a unique Chinese `participant_id_card` whose birth segment (digits 7–14) matches the recorded birth date.
- It picks a unique emergency contact name from the provided list and generates a valid Chinese mobile number for the contact.
- Registration numbers follow the same `REG-{event}-{timestamp}-{random8}` pattern the app uses elsewhere.

If a user already has a registration for event 5 or is missing, the script skips that entry and reports it.
