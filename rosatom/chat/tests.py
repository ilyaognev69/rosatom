from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Channel, Message

User = get_user_model()

class ChatAPITests(APITestCase):

	def setUp(self):
		self.user1 = User.objects.create_user(username="user1", password="password123")
		self.user2 = User.objects.create_user(username="user2", password="password123")
		self.moderator = User.objects.create_user(username="moderator", password="password123", is_moderator=True)

		self.channel = Channel.objects.create(name="general", slug="general")
		self.channel.participants.add(self.user1, self.user2, self.moderator)

		self.register_url = reverse("register")
		self.token_url = reverse("token_obtain_pair")
		self.token_refresh_url = reverse("token_refresh")
		self.block_user_url = reverse("block_user", kwargs={"channel_id": self.channel.id, "user_id": self.user2.id})
		self.unblock_user_url = reverse("unblock_user", kwargs={"channel_id": self.channel.id, "user_id": self.user2.id})
		self.message_history_url = reverse("message_history", kwargs={"channel_name": "general"})

	def authenticate_user(self, username, password):
		"""Helper function to authenticate a user and return an access token."""
		response = self.client.post(self.token_url, {"username": username, "password": password})
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		return response.data["access"]

	def test_user_registration(self):
		"""Тест регистрации нового пользователя"""
		response = self.client.post(self.register_url, {
			"username": "new_user",
			"password": "new_password123",
			"email": "new_user@example.com"
		})
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_user_authentication(self):
		"""Тест аутентификации пользователя и получения токена"""
		token = self.authenticate_user("user1", "password123")
		self.assertIsNotNone(token)

	def test_block_user(self):
		"""Тест блокировки пользователя модератором"""
		token = self.authenticate_user("moderator", "password123")
		self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

		response = self.client.post(self.block_user_url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

		self.channel.refresh_from_db()
		self.assertIn(self.user2, self.channel.blocked_users.all())

	def test_unblock_user(self):
		"""Тест разблокировки пользователя модератором"""
		token = self.authenticate_user("moderator", "password123")
		self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
		self.client.post(self.block_user_url)

		response = self.client.post(self.unblock_user_url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

		self.channel.refresh_from_db()
		self.assertNotIn(self.user2, self.channel.blocked_users.all())

	def test_get_message_history(self):
		"""Тест получения истории сообщений из канала"""
		# Создаем несколько сообщений напрямую в базе данных
		Message.objects.create(channel=self.channel, user=self.user1, content="Message 1")
		Message.objects.create(channel=self.channel, user=self.user2, content="Message 2")

		# Аутентифицируемся и запрашиваем историю
		token = self.authenticate_user("user1", "password123")
		self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
		response = self.client.get(self.message_history_url)

		# Проверка успешного статуса и количества сообщений
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data), 2)

		# Проверка содержания сообщений
		self.assertEqual(response.data[0]["content"], "Message 1")
		self.assertEqual(response.data[1]["content"], "Message 2")

