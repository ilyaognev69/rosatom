import os
import django
import random
from django.contrib.auth import get_user_model
from chat.models import Channel, Message

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')
django.setup()

User = get_user_model()

def create_test_users():
    users = []
    usernames = ['alice', 'bob', 'carol', 'dave', 'eve']
    for username in usernames:
        user, created = User.objects.get_or_create(
            username=username,
            defaults={'password': 'testpassword123'}
        )
        users.append(user)
    print(f'Создано {len(users)} пользователей.')
    return users

def create_test_channels(users):
    channels = []
    channel_names = ['general', 'random', 'news', 'tech', 'music']
    for name in channel_names:
        channel, created = Channel.objects.get_or_create(name=name, slug=name)
        participants = random.sample(users, k=random.randint(2, len(users)))
        channel.participants.add(*participants)
        channels.append(channel)
    print(f'Создано {len(channels)} каналов.')
    return channels

def create_test_messages(channels, users):
    messages_count = 0
    sample_messages = [
        "Hello everyone!", "How's it going?", "Did you hear the news?", 
        "What's your favorite song?", "Any recommendations for a good movie?", 
        "I'm learning Django!", "This project is cool!", "Let's have a meeting at 5."
    ]
    for channel in channels:
        for _ in range(random.randint(5, 15)):
            user = random.choice(users)
            message_text = random.choice(sample_messages)
            Message.objects.create(channel=channel, user=user, content=message_text)
            messages_count += 1
    print(f'Создано {messages_count} сообщений.')

def run():
    users = create_test_users()
    channels = create_test_channels(users)
    create_test_messages(channels, users)
    print("Тестовые данные успешно созданы.")
