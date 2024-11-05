from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.text import slugify
# Create your models here.

class CustomUser(AbstractUser):
	is_moderator = models.BooleanField(default=False)
	
class Channel(models.Model):
	name = models.CharField(max_length=100)
	participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="channels")
	blocked_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='blocked_channels', blank=True)
	slug = models.SlugField(unique=True, blank=True)
	
	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		super().save(*args, **kwargs)
	
class Message(models.Model):
	channel = models.ForeignKey(Channel, related_name="messages", on_delete=models.CASCADE)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	content = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)
	
	