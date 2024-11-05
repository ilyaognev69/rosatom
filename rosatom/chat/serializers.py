from rest_framework import serializers
from .models import CustomUser
from .models import Message

class RegisterSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)
	
	class Meta:
		model = CustomUser
		fields = ('username', 'password', 'email')
		
	def create(self, validated_data):
		user = CustomUser.objects.create_user(
			username=validated_data['username'],
			password=validated_data['password'],
			email=validated_data.get('email', '')
		)
		return user
	
class MessageSerializer(serializers.ModelSerializer):
	username = serializers.CharField(source='user.username', read_only=True)
	
	class Meta:
		model = Message
		fields = ['id', 'username', 'content', 'timestamp']